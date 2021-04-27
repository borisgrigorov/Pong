const socket = require("socket.io")(3001);
const uuid = require("uuid");

console.log("Launching pong server...");

socket.on("connect", async (socket) => {
    socket.on("join", (msg) => {
        if (msg.gameId && msg.name) {
            console.log("Joining game with ID " + msg.gameId);
            socket.to(msg.gameId).emit("JOINED", {
                status: "JOINED",
                game: msg.gameId,
                name: msg.name,
            });
            socket.emit("JOIN", {
                game: msg.gameId,
            });
            socket.join(msg.gameId);
        }
    });
    socket.on("create", async (msg) => {
        if (msg.name) {
            var newId = uuid.v1();
            console.log("New game with ID " + newId);
            socket.join(newId);
            socket.emit("CREATED", {
                status: "OK",
                game: newId,
            });
        }
    });
    socket.on("gamedata", (msg) => {
        console.log(msg);
        if (msg.game) {
            socket.to(msg.game).emit("GAMEDATA", {
                pos: msg.pos,
                name: msg.name,
                ball_x: msg.ball_x,
                ball_y: msg.ball_y,
            });
        }
    });
});
