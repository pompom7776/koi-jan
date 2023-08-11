import eventlet
import eventlet.wsgi
import socketio

from socket_manager.room import on_room
from socket_manager.waiting_room import on_waiting_room
from socket_manager.game import on_game


if __name__ == "__main__":
    eventlet.monkey_patch()
    socket_io = socketio.Server(cors_allowed_origins="http://localhost:5173")
    app = socketio.WSGIApp(socket_io)

    @socket_io.on("connect")
    def on_connect(socket_id, environ):
        print(f"connected : {socket_id}")

    rooms = []
    players = []

    on_room(socket_io, rooms, players)
    on_waiting_room(socket_io, rooms, players)
    on_game(socket_io, rooms, players)

    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 8888)), app)
