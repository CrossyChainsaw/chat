import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send, join_room
import random
app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = 'your-secret-key'  # Important for session handling

# Global variables to store connected users and messages
users = []
messages = []  # Store chat messages
fruits = [
    "Apple", "Apricot", "Avocado", "Banana", "Blackberry", "Blueberry", "Cherry", "Clementine", "Coconut", 
    "Cranberry", "Currant", "Date", "Dragonfruit", "Elderberry", "Fig", "Grape", "Grapefruit", "Guava", 
    "Honeydew Melon", "Jackfruit", "Kiwi", "Lemon", "Lime", "Lychee", "Mango", "Mulberry", "Nectarine", 
    "Orange", "Papaya", "Passionfruit", "Peach", "Pear", "Pineapple", "Plum", "Pomegranate", "Raspberry", 
    "Red currant", "Starfruit", "Tangerine", "Watermelon", "Zucchini", "Acai Berry", "Alfalfa Sprout", 
    "Apple Pear", "Aprium", "Asian Pear", "Atemoya", "Banana Passionfruit", "Barbados Cherry", "Bing Cherry", 
    "Black Currant", "Black Grapes", "Black Plum", "Blood Orange", "Boquila", "Buddha's Hand", "Cabelluda", 
    "Cactoid Cactus", "Canistel", "Capulin Cherry", "Carambola", "Chayote", "Cherimoya", "Chokecherry", 
    "Clementine Tangerine", "Cranberry Apple", "Damson Plum", "Date Palm", "Durian", "Elephant Apple", 
    "Emu Apple", "Farkleberry", "Feijoa", "Finger Lime", "Goji Berry", "Golden Apple", "Gooseberry", 
    "Grapes (Red)", "Grumichama", "Hala Fruit", "Hawthorn", "Horned Melon", "Indian Fig", "Indian Gooseberry", 
    "Jabuticaba", "Jameo", "Jatoba", "Jelly Palm", "Jujube", "Kaffir Lime", "Kiwifruit", "Kumquat", 
    "Langsat", "Longan", "Mamey", "Mango Steen", "Mango Papaya", "Marula", "Monkey Orange", "Muscadine", 
    "Nance", "Olives", "Oregon Grape", "Pawpaw", "Persimmon", "Pitanga", "Pluot", "Pineberry", "Plumcot", 
    "Prickly Pear", "Quince", "Rambutan", "Red Banana", "Salak", "Salvia", "Soursop", "Sugar Apple", 
    "Surinam Cherry", "Tamarillo", "Tamarind", "Uva Ursi", "Yunnan Hackberry", "Zinfandel Grape"
]
def generate_username():
    random_fruit = random.choice(fruits)
    random_fruit = random_fruit.replace(' ', '_')
    randint = random.choice(range(1, 54))
    username = f"{random_fruit}_{randint}"
    return username

# Route to render the homepage with the name form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print('post request')
        name = generate_username()
        session['username'] = name
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
    print(data['username'])
    if data['username'] == session['username']:
        message_content = f"{data['username']}: {data['message']}"  # Format the message
        messages.append(message_content)  # Store the formatted message
        send(message_content, broadcast=True)  # Broadcast the formatted message
    else:
        send({'redirect': 'https://www.youtube.com/watch?v=xvFZjo5PgG0'}, broadcast=False)


if __name__ == '__main__':
    print("Starting the Flask server...")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    
