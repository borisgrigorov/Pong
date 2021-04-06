const socket = require("socket.io")(3001);
const uuid = require("uuid");

var games = [];

socket.on("connect", async (socket) => {
    socket.on("join", (msg) => {
        if (msg.gameId) {
            var found = false;
            var foundId;
            for (var i in games) {
                if (games[i].id == msg.gameId) {
                    found = true;
                    foundId = i;
                }
            }
            if (!found) {
                socket.to(socket.id).emit({
                    status: "ERROR",
                    msg: "Game not found",
                });
            } else {
                socket.to(socket.id).emit({
                    status: "OK",
                    game: foundId
                });
            }
        }
    });
    socket.on("create", async (msg) => {
        if (msg.name) {
            var newId = uuid.v1();
            games.push({
                id: newId,
                players: [
                    {
                        id: socket.id,
                        name: msg.name,
                    },
                ],
            });
            socket.to(socket.id).emit("CREATED", {
                status: "OK",
                message: "OK",
                game: newId
            });
        } else {
            socket.to(socket.id).emit({
                status: "ERROR",
                message: "Name can not be empty",
            });
        }
    });
    socket.on("gamedata", msg => {
        socket.to(msg.game).emit({
            "pos": msg.pos,
        });
    });
});
