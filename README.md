# Number Guessing Game API

A full-stack web application featuring a RESTful API that powers an interactive number guessing game. The backend is built with Python and Flask, while the frontend uses JavaScript, HTML, and CSS.

## Live Demo

[Play the Number Guessing Game](https://sachinsutar.pythonanywhere.com/)

## Features

- **Interactive Gameplay**: Guess a number between 1-100 with helpful hints
- **RESTful API Architecture**: Well-structured endpoints for game management
- **Session Management**: Maintains game state between requests
- **Responsive Design**: Works on both desktop and mobile devices
- **Real-time Feedback**: Immediate responses to player actions

## Technologies Used

- **Backend**: Python, Flask, Flask-CORS
- **Frontend**: JavaScript, HTML, CSS
- **Deployment**: PythonAnywhere
- **Development Tools**: Git, GitHub

## API Documentation

The game provides the following API endpoints:

### Create a New Game
- **URL**: `/game/new`
- **Method**: `POST`
- **Response**: 
  ```json
  {
    "game_id": "unique-uuid",
    "message": "New game started! I'm thinking of a number between 1 and 100.",
    "attempts_remaining": 10,
    "status": "active"
  }
