import eventlet
import eventlet.wsgi
import socketio

import presenter.controller.room as room
import presenter.controller.game as game


if __name__ == "__main__":
    eventlet.monkey_patch()
    socket_io = socketio.Server(cors_allowed_origins="http://localhost:5173")
    app = socketio.WSGIApp(socket_io)

    room.set(socket_io)
    game.set(socket_io)

    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 8888)), app)
