import eventlet
import eventlet.wsgi
import socketio

from presenter import controller


if __name__ == "__main__":
    eventlet.monkey_patch()
    socket_io = socketio.Server(cors_allowed_origins="http://localhost:5173")
    app = socketio.WSGIApp(socket_io)

    @socket_io.on("connect")
    def on_connect(socket_id, environ):
        print(f"connected : {socket_id}")

    controller.room.set(socket_io)

    eventlet.wsgi.server(eventlet.listen(("0.0.0.0", 8888)), app)
