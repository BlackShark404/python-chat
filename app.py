import eventlet
eventlet.monkey_patch()  # Add this to enable eventlet monkey patching

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')  # Explicitly set eventlet as async mode

# Store connected users. Key is socket id, value is username and avatarUrl
users = {}

@app.route("/")
def index():
    return render_template("index.html")

# We're listening for the connect event
@socketio.on("connect")
def handle_connect():
    username = f"User_{random.randint(1000,9999)}"
    gender = random.choice(["girl", "boy"])
    avatar_url = f"https://avatar.iran.liara.run/public/{gender}?username={username}"  # Fixed the extra space in the URL

    users[request.sid] = {"username": username, "avatar": avatar_url}

    # Notify other users that someone joined
    emit("user_joined", {"username": username, "avatar": avatar_url}, broadcast=True)

    # Send the new user their username
    emit("set_username", {"username": username})

@socketio.on("disconnect")
def handle_disconnect():
    user = users.pop(request.sid, None)
    if user:
        # Notify others when a user leaves
        emit("user_left", {"username": user["username"]}, broadcast=True)

@socketio.on("send_message")
def handle_message(data):
    user = users.get(request.sid)
    if user:
        message = data.get("message", "")
        if message:  # Ensure there's a message to send
            emit(
                "new_message",
                {
                    "username": user["username"],
                    "avatar": user["avatar"],
                    "message": message,
                },
                broadcast=True,
            )

@socketio.on("update_username")
def handle_update_username(data):
    old_username = users[request.sid]["username"]
    new_username = data.get("username", old_username)  # Default to old username if none provided
    users[request.sid]["username"] = new_username

    # Notify others of the username change
    emit(
        "username_updated",
        {"old_username": old_username, "new_username": new_username},
        broadcast=True,
    )

if __name__ == "__main__":
    socketio.run(app)
