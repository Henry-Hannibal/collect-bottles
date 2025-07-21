import base64
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
    
    # Place characters
    for bottle in bottles:
        x, y = bottle['coordinates']['x'], bottle['coordinates']['y']
        grid[y][x] = bottle['character']
    
    # Render message
    message = '\n'.join(''.join(row) for row in grid)
    print("message = "+message)
    return jsonify({'message': message})

app.run(host="0.0.0.0", port=8080)
