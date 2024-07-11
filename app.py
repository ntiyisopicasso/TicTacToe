from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def init_board():
    return [[' ' for _ in range(3)] for _ in range(3)]

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != ' ' or board[2][0] == board[1][1] == board[0][2] != ' ':
        return board[1][1]
    return None

def is_stuck(board):
    return all(cell != ' ' for row in board for cell in row)

@app.route('/')
def index():
    if 'board' not in session:
        session['board'] = init_board()
        session['player'] = 1
        session['p1'] = None
        session['p2'] = None
        session['game_init'] = False
    return render_template('index.html', board=session['board'], player=session['player'], p1=session['p1'], p2=session['p2'], game_init=session['game_init'])

@app.route('/start', methods=['POST'])
def start():
    session['p1'] = request.form['p1']
    session['p2'] = request.form['p2']
    session['game_init'] = True
    return redirect(url_for('index'))

@app.route('/play', methods=['POST'])
def play():
    if not session['game_init']:
        return redirect(url_for('index'))
    x = int(request.form['x'])
    y = int(request.form['y'])
    if session['board'][x][y] == ' ':
        session['board'][x][y] = 'X' if session['player'] == 1 else 'O'
        winner = check_winner(session['board'])
        if winner:
            return render_template('index.html', board=session['board'], player=session['player'], p1=session['p1'], p2=session['p2'], game_init=session['game_init'], winner=winner)
        if is_stuck(session['board']):
            return render_template('index.html', board=session['board'], player=session['player'], p1=session['p1'], p2=session['p2'], game_init=session['game_init'], winner='Nobody')
        session['player'] = 2 if session['player'] == 1 else 1
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
