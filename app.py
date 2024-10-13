from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

users = {}
typing_users = set()


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def handle_connect():
    username = f"User_{random.randint(1000,9999)}"
    gender = "boy"
    avatar_url = f"https://avatar.iran.liara.run/public/{gender}?username={username}"

    users[request.sid] = {"username": username, "avatar": avatar_url, "gender": gender}

    emit(
        "user_joined",
        {"username": username, "avatar": avatar_url, "online_users": len(users)},
        broadcast=True,
    )
    emit("set_username", {"username": username})


@socketio.on("disconnect")
def handle_disconnect():
    user = users.pop(request.sid, None)
    if user:
        typing_users.discard(user["username"])
        emit(
            "user_left",
            {"username": user["username"], "online_users": len(users)},
            broadcast=True,
        )
        emit(
            "typing", {"username": user["username"], "isTyping": False}, broadcast=True
        )


@socketio.on("send_message")
def handle_message(data):
    user = users.get(request.sid)
    if user:
        emit(
            "new_message",
            {
                "username": user["username"],
                "avatar": user["avatar"],
                "message": data["message"],
            },
            broadcast=True,
        )


@socketio.on("update_username")
def handle_update_username(data):
    old_username = users[request.sid]["username"]
    new_username = data["username"]
    users[request.sid]["username"] = new_username
    users[request.sid]["avatar"] = (
        f"https://avatar.iran.liara.run/public/{users[request.sid]['gender']}?username={new_username}"
    )

    if old_username in typing_users:
        typing_users.remove(old_username)
        typing_users.add(new_username)

    emit(
        "username_updated",
        {"old_username": old_username, "new_username": new_username},
        broadcast=True,
    )


@socketio.on("update_gender")
def handle_update_gender(data):
    users[request.sid]["gender"] = data["gender"]
    new_avatar = f"https://avatar.iran.liara.run/public/{data['gender']}?username={users[request.sid]['username']}"
    users[request.sid]["avatar"] = new_avatar
    emit(
        "new_avatar",
        {"username": users[request.sid]["username"], "avatar": new_avatar},
        broadcast=True,
    )


@socketio.on("typing")
def handle_typing(data):
    username = users[request.sid]["username"]
    typing_users.add(username)
    emit("typing", {"username": username, "isTyping": True}, broadcast=True)


@socketio.on("stop_typing")
def handle_stop_typing():
    username = users[request.sid]["username"]
    typing_users.discard(username)
    emit("typing", {"username": username, "isTyping": False}, broadcast=True)


if __name__ == "__main__":
    socketio.run(app)
