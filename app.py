from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

board = [' ' for _ in range(9)]

winning_combinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]

human_marker = 'X'
ai_marker = 'O'

def ai_move():
    for i in range(9):
        if board[i] == ' ':
            board[i] = ai_marker
            if is_winner(ai_marker):
                return
            board[i] = ' '

    for i in range(9):
        if board[i] == ' ':
            board[i] = human_marker
            if is_winner(human_marker):
                board[i] = ai_marker
                return
            board[i] = ' '

    empty_cells = [i for i, cell in enumerate(board) if cell == ' ']
    if empty_cells:
        move = random.choice(empty_cells)
        board[move] = ai_marker

def is_winner(marker):
    for combo in winning_combinations:
        if all(board[i] == marker for i in combo):
            return True
    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cell = int(request.form['cell'])
        if board[cell] == ' ':
            board[cell] = human_marker
            if not is_winner(human_marker):
                ai_move()
        else:
            return redirect(url_for('index'))

    winner = None
    if is_winner(human_marker):
        winner = 'Human'
    elif is_winner(ai_marker):
        winner = 'AI'
    elif ' ' not in board:
        winner = 'Tie'

    return render_template('index.html', board=board, winner=winner)

if __name__ == '__main__':
    app.run(debug=True)
