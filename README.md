# Python Chat Application

This is a real-time chat application built with Python, Flask, and Socket.IO. It provides a simple interface for users to join a chat room, send messages, and interact with other users.

## Features

- Real-time messaging
- Dynamic username generation and updating
- User avatars based on gender
- Online user count
- Typing indicators
- Gender selection (Male/Female)

## Technologies Used

- Backend:
  - Python
  - Flask
  - Flask-SocketIO
  - Gunicorn (for deployment)
- Frontend:
  - HTML
  - JavaScript (assumed, for Socket.IO client)
- Avatar Service:
  - https://avatar.iran.liara.run

## Setup and Installation

1. Clone the repository (assuming you have one)
2. Install the required Python packages:
   ```
   pip install flask flask-socketio gunicorn
   ```
3. For development, run the application using:
   ```
   python wsgi.py
   ```
4. For production deployment, use Gunicorn:
   ```
   gunicorn --worker-class eventlet -w 1 wsgi:app
   ```
5. Open a web browser and navigate to `http://localhost:5000` (or the appropriate address where your app is running)

## How It Works

1. When a user connects, they are assigned a random username and avatar.
2. Users can send messages, which are broadcast to all connected users.
3. Users can update their username and gender, which updates their avatar.
4. The application tracks online users and displays the count.
5. Typing indicators show when users are composing messages.

## File Structure

- `app.py`: The main Flask application with Socket.IO event handlers
- `wsgi.py`: WSGI entry point for running the app, especially in production
- `index.html`: The frontend HTML template (located in a `templates` folder)

## Deployment

The application uses a WSGI (Web Server Gateway Interface) setup for deployment. The `wsgi.py` file serves as the entry point for WSGI servers like Gunicorn.

For production deployment:
1. Ensure Gunicorn is installed: `pip install gunicorn`
2. Use Gunicorn to run the application: `gunicorn --worker-class eventlet -w 1 wsgi:app`

Note: The `--worker-class eventlet` option is important for proper functioning of Socket.IO with Gunicorn.

## Development

For development purposes, you can run the application directly using Python:

```
python wsgi.py
```

This will start the application in debug mode, which is suitable for development but should not be used in production.

## Contributing

We welcome contributions to this project! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and test them.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a Pull Request.