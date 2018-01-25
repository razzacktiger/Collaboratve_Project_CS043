import wsgiref.simple_server
import urllib.parse
import sqlite3
import http.cookies
import random
from ticTacToeClass import TTT

connection = sqlite3.connect('TTT-Users.db')
stmt = "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
cursor = connection.cursor()
result = cursor.execute(stmt)
r = result.fetchall()
if r == []:
    exp = 'CREATE TABLE users (username,password)'
    connection.execute(exp)

theBoard = ['', '<input type="radio" name="playerMove" value="1">',
                '<input type="radio" name="playerMove" value="2">',
                '<input type="radio" name="playerMove" value="3">',
                '<input type="radio" name="playerMove" value="4">',
                '<input type="radio" name="playerMove" value="5">',
                '<input type="radio" name="playerMove" value="6">',
                '<input type="radio" name="playerMove" value="7">',
                '<input type="radio" name="playerMove" value="8">',
                '<input type="radio" name="playerMove" value="9">']
game = TTT(theBoard)
game.turn = 'new game'

def application(environ, start_response):
    headers = [('Content-Type', 'text/html; charset=utf-8')]

    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    un = params['username'][0] if 'username' in params else None
    pw = params['password'][0] if 'password' in params else None

    if path == '/register' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ?', [un]).fetchall()
        if user:
            start_response('200 OK', headers)
            return ['Sorry, username "{}" is taken'.format(un).encode()]
        else:
            connection.execute('INSERT INTO users VALUES (?,?)', (un, pw))
            connection.commit()
            start_response('200 OK', headers)
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            return ['Account successfully created. <br><a href="/">Login</a>'.encode()]

    elif path == '/login' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()
        if user:
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            start_response('200 OK', headers)
            return ['User {} successfully logged in. <br><a href="/play">Play Tic-Tac-Toe</a>'.format(un).encode()]
        else:
            start_response('200 OK', headers)
            return ['Incorrect username or password'.encode()]

    elif path == '/logout':
        headers.append(('Set-Cookie', 'session=0; expires=Thu, 01 Jan 1970 00:00:00 GMT'))
        start_response('200 OK', headers)
        return ['Logged out. <a href="/">Login</a>'.encode()]

    elif path == '/play':
        start_response('200 OK', headers)

        if 'HTTP_COOKIE' not in environ:
            return ['Not logged in <a href="/">Login</a>'.encode()]

        cookies = http.cookies.SimpleCookie()
        cookies.load(environ['HTTP_COOKIE'])
        if 'session' not in cookies:
            return ['Not logged in <a href="/">Login</a>'.encode()]

        [un, pw] = cookies['session'].value.split(':')
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()

        # This is where the game begins. This section of is code only executed if the login form works, and if the user
        # is successfully logged in.
        # ------------------------------------------------------------------------------------------------------------ #
        if user:
            page = str('<!DOCTYPE html><html><head><title>TTT Game</title></head><body style="text-align:center;">' +
                       '<h2>Tic-Tac-Toe</h2>')

            if game.turn == 'new game':
                game.turn = game.whoGoesFirst()

            if game.turn == 'X':
                page += '<br>It is O\'s turn<br>' # this looks like the opposite of what it should be, but it works
                if 'playerMove' not in params:
                    page += TTT.drawBoard(game, game.board)
                    return [page.encode()]
                else:
                    playerMove = params['playerMove'][0]
                    game.board = game.makeMove(game.board, 'X', playerMove)
                    page += game.drawBoard(game.board)
                    game.turn = 'O'
                    if game.isWinner(game.board, 'X'):
                        page = ('<!DOCTYPE html><html><head><title>TTT Game</title></head>' +
                                '<body style="text-align:center;"><h2>Tic-Tac-Toe</h2>')
                        page += '<br>Player X wins!<br>' # Add hyperlinks here for "play again" and "quit/logout".
                        game.board = theBoard
                        game.turn = 'new game'
                        return [page.encode()]
                    elif game.isBoardFull(game.board, playerMove):
                        page = ('<!DOCTYPE html><html><head><title>TTT Game</title></head>' +
                                '<body style="text-align:center;"><h2>Tic-Tac-Toe</h2>')
                        page += '<br>The game is a tie.<br>'
                        # Add hyperlinks here for "play again" and "quit/logout".
                        game.board = theBoard
                        game.turn = 'new game'
                        return [page.encode()]
                    else:
                        return [page.encode()]

            if game.turn == 'O':
                page += '<br>It is X\'s turn<br>' # this looks like the opposite of what it should be, but it works
                if 'playerMove' not in params:
                    page += TTT.drawBoard(game, game.board)
                    return [page.encode()]
                else:
                    playerMove = params['playerMove'][0]
                    game.board = game.makeMove(game.board, 'O', playerMove)
                    page += game.drawBoard(game.board)
                    game.turn = 'X'
                    if game.isWinner(game.board, 'O'):
                        page = ('<!DOCTYPE html><html><head><title>TTT Game</title></head>' +
                                '<body style="text-align:center;"><h2>Tic-Tac-Toe</h2>')
                        page += '<br>Player O wins!<br>' # Add hyperlinks here for "play again" and "quit/logout".
                        game.board = theBoard
                        game.turn = 'new game'
                        return [page.encode()]
                    elif game.isBoardFull(game.board, playerMove):
                        page = ('<!DOCTYPE html><html><head><title>TTT Game</title></head>' +
                                '<body style="text-align:center;"><h2>Tic-Tac-Toe</h2>')
                        page += '<br>The game is a tie.<br>' # Add hyperlinks here for "play again" and "quit/logout".
                        game.board = theBoard
                        game.turn = 'new game'
                        return [page.encode()]
                    else:
                        return [page.encode()]
        else:
            return ['Not logged in. <a href="/">Login</a>'.encode()]

    elif path == '/':
        start_response('200 OK', headers)
        register_or_login = '''<!DOCTYPE html><html><head><title>Register/Login</title></head>
        <body style="text-align:center">
        <h1>Welcome to Tic-Tac-Toe</h1>
        <form action="/login">
        <h1>Login</h1><br>
        Username<input type="text" name="username"><br>
        Password<input type="password" name="password"><br>
        <input type="submit" value="Log in"><br>
        </form>
        <form action="/register">
        <h1>Register</h1><br>
        Username<input type="text" name="username"><br>
        Password<input type="password" name="password"><br>
        <input type="submit" value="Register">
        </form>
        </body>
        </html>'''
        return [register_or_login.encode()]

    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()
