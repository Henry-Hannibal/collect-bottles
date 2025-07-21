import base64
import os
import csv
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello():
    hostname = request.host.split(':')[0]
    hello = "SEVMTE9fV09STEQ="
    aloha = "QUxPSEFfR1JFRVRJTkc="
    if 'aloha' in hostname:
        aloha_byte = base64.b64decode(aloha)
        return aloha_byte.decode('utf-8')
    else: 
        hello_byte = base64.b64decode(hello)
        return hello_byte.decode('utf-8')

@app.route('/collect-bottles', methods=['POST'])
def collect_bottles():
    bottles = request.get_json()
    
    # Find grid dimensions
    max_x = max(bottle['coordinates']['x'] for bottle in bottles)
    max_y = max(bottle['coordinates']['y'] for bottle in bottles)
    
    # Create grid
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    print(f"max_x = {max_x}")
    print(f"max_y = {max_y}")
    # Place characters
    for bottle in bottles:
        x, y = bottle['coordinates']['x'], bottle['coordinates']['y']
        grid[y][x] = bottle['character']
        print(f"grid[y][x] = {grid[y][x]}")
    
    # Render message
    message = '\n'.join(''.join(row) for row in grid)
    print(f"message = {message}")
    return jsonify({'message': message})

# Load morse code mapping from ConfigMap
morse_map = {}
config_path = os.environ.get('MORSE_CONFIG_PATH', 'morse_code.csv')

try:
    with open(config_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:
                character, morse = row[0], row[1]
                morse_map[morse] = character
except FileNotFoundError:
    print(f"Warning: Morse code mapping file not found at {config_path}")
    # Fallback to basic mapping if file not found
    morse_map = {
        ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E",
        "..-.": "F", "--.": "G", "....": "H", "..": "I", ".---": "J",
        "-.-": "K", ".-..": "L", "--": "M", "-.": "N", "---": "O",
        ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T",
        "..-": "U", "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y",
        "--..": "Z", ".----": "1", "..---": "2", "...--": "3", "....-": "4",
        ".....": "5", "-....": "6", "--...": "7", "---..": "8", "----.": "9",
        "-----": "0", ".-.-.-": ".", "--..--": ",", "..--..": "?",
        "-..-.": "/", "-.--.": "(", "-.--.-": ")", ".-...": "&",
        "---...": ":", "-.-.-.": ";", "-...-": "=", ".-.-.": "+",
        "-....-": "-", "..--.-": "_", ".-..-.": "\"", "...-..-": "$",
        ".--.-": "@", "...-.-": "END"
    }

def decode_morse(morse_code):
    """Decode a morse code message to text"""
    words = morse_code.split('/')
    decoded_message = []
    
    for word in words:
        letters = word.strip().split(' ')
        decoded_word = ''
        
        for letter in letters:
            if letter:  # Skip empty strings
                decoded_word += morse_map.get(letter, '?')
        
        decoded_message.append(decoded_word)
    
    return ' '.join(decoded_message)

@app.route('/decode-morse', methods=['POST'])
def decode_morse_endpoint():
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({'error': 'Invalid request. Please provide a message.'}), 400
    
    morse_message = data['message']
    decoded_message = decode_morse(morse_message)
    
    print(f"Decoded message: {decoded_message}")
    
    return jsonify({
        'original': morse_message,
        'decoded': decoded_message
    })


app.run(host="0.0.0.0", port=8080)
