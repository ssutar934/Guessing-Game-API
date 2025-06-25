from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
import uuid
import os

# Create application
application = Flask(__name__)
CORS(application)

# Store game sessions
games = {}

# Simple health check route that EB uses
@application.route('/health')
def health_check():
    return "OK"

# Serve the static HTML file
@application.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')

@application.route('/game/new', methods=['POST'])
def new_game():
    """Start a new game and return the game ID"""
    # Get difficulty from request, default to 'medium'
    difficulty = request.json.get('difficulty', 'medium') if request.json else 'medium'

    # Set range based on difficulty
    if difficulty == 'easy':
        number_range = (1, 50)
    elif difficulty == 'hard':
        number_range = (1, 200)
    else:  # medium
        number_range = (1, 100)

    game_id = str(uuid.uuid4())
    games[game_id] = {
        'secret_number': random.randint(number_range[0], number_range[1]),
        'guesses': [],
        'max_attempts': 10,
        'game_over': False,
        'won': False,
        'range': number_range,
        'difficulty': difficulty
    }

    return jsonify({
        'game_id': game_id,
        'message': f'New {difficulty} game started! I\'m thinking of a number between {number_range[0]} and {number_range[1]}.',
        'attempts_remaining': games[game_id]['max_attempts'],
        'status': 'active',
        'difficulty': difficulty,
        'range': number_range
    })

@application.route('/game/<game_id>/guess', methods=['POST'])
def make_guess(game_id):
    """Process a guess for a specific game"""
    # Check if the game exists
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404

    # Get the current game state
    game = games[game_id]

    # Check if the game is already over
    if game['game_over']:
        return jsonify({
            'error': 'Game is already over',
            'won': game['won'],
            'secret_number': game['secret_number']
        }), 400

    # Get the guess from the request
    try:
        guess = int(request.json.get('guess', 0))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid guess. Please provide a number.'}), 400

    # Record the guess
    game['guesses'].append(guess)

    # Check if the guess is correct
    if guess == game['secret_number']:
        game['game_over'] = True
        game['won'] = True
        return jsonify({
            'message': f'Congratulations! You guessed the number in {len(game["guesses"])} attempts!',
            'game_over': True,
            'won': True,
            'attempts_made': len(game['guesses']),
            'attempts_remaining': game['max_attempts'] - len(game['guesses'])
        })

    # Give a hint
    hint = 'Too low! Try a higher number.' if guess < game['secret_number'] else 'Too high! Try a lower number.'

    # Check if the player has run out of attempts
    if len(game['guesses']) >= game['max_attempts']:
        game['game_over'] = True
        return jsonify({
            'message': f'Game over! You\'ve used all {game["max_attempts"]} attempts. The secret number was {game["secret_number"]}.',
            'game_over': True,
            'won': False,
            'secret_number': game['secret_number'],
            'attempts_made': len(game['guesses']),
            'attempts_remaining': 0
        })

    # Return the current game state
    return jsonify({
        'message': hint,
        'attempts_made': len(game['guesses']),
        'attempts_remaining': game['max_attempts'] - len(game['guesses']),
        'status': 'active'
    })

@application.route('/game/<game_id>', methods=['GET'])
def game_status(game_id):
    """Get the current status of a game"""
    # Check if the game exists
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404

    # Get the current game state
    game = games[game_id]

    return jsonify({
        'game_id': game_id,
        'attempts_made': len(game['guesses']),
        'attempts_remaining': game['max_attempts'] - len(game['guesses']),
        'guesses': game['guesses'],
        'game_over': game['game_over'],
        'won': game['won'],
        'status': 'completed' if game['game_over'] else 'active',
        'secret_number': game['secret_number'] if game['game_over'] else None
    })

@application.route('/test')
def test_static():
    return send_from_directory('static', 'test.html')

# For local development compatibility
app = application