import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'  # Replace 'secret!' with a secure key in production
socketio = SocketIO(app)

# Global variables to store connected users and messages
users = []
messages = []  # Store chat messages

# Route to render the homepage with the name form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the name from the form
        name = request.form['name']
        if name:
            users.append(name)  # Add the name to the users list
            return redirect(url_for('chat', name=name))
    return render_template('index.html')

# Route for the public chat page
@app.route('/chat/<name>')
def chat(name):
    if name not in users:
        return redirect(url_for('index'))  # Redirect if user is not in the list
    return render_template('chat.html', name=name, messages=messages)

# WebSocket event to handle messages
@socketio.on('message')
def handle_message(data):
    messages.append(data)  # Store the new message in the list
    send(data, broadcast=True)  # Broadcast the message to all connected users

if __name__ == '__main__':
    socketio.run(app, debug=True)
