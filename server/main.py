import eventlet
import eventlet.wsgi
import socketio

import controller.room
import controller.waiting_room


if __name__ == "__main__":
    eventlet.monkey_patch()
    socket_io = socketio.Server(cors_allowed_origins="http://localhost:5173")
    app = socketio.WSGIApp(socket_io)

    @socket_io.on("connect")
    def on_connect(socket_id, environ):
        print(f"connected : {socket_id}")

    rooms = []
    players = []

    controller.room.set(socket_io, rooms, players)
    controller.waiting_room.set(socket_io, rooms, players)

    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 8888)), app)
