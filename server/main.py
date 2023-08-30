import eventlet
import eventlet.wsgi
import socketio

import interfaces.controller.room as room_controller
import interfaces.controller.game as game_controller
import interfaces.controller.chat as chat_controller
import interfaces.controller.reaction as reaction_controller


if __name__ == "__main__":
    eventlet.monkey_patch()
    socket_io = socketio.Server(cors_allowed_origins="http://localhost:5173")
    app = socketio.WSGIApp(socket_io)

    room_controller.set(socket_io)
    game_controller.set(socket_io)
    chat_controller.set(socket_io)
    reaction_controller.set(socket_io)

    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 8888)), app)
