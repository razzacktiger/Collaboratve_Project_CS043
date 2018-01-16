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
            return ['Account successfully created. </br><a href="/">Login</a>'.encode()]

    elif path == '/login' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()
        if user:
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            start_response('200 OK', headers)
            return ['User {} successfully logged in. </br><a href="/account">Account</a>'.format(un).encode()]
        else:
            start_response('200 OK', headers)
            return ['Incorrect username or password'.encode()]

    elif path == '/logout':
        headers.append(('Set-Cookie', 'session=0; expires=Thu, 01 Jan 1970 00:00:00 GMT'))
        start_response('200 OK', headers)
        return ['Logged out. <a href="/">Login</a>'.encode()]

    elif path == '/account':
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
            page='<!DOCTYPE html><html><head><title>TTT Game</title></head><body><h1>TEST</h1>'
            game=TTT
            # Reset the board
            theBoard = [' '] * 10
            playerLetter, computerLetter = game.inputPlayerLetter()
            turn = game.whoGoesFirst()
            print('The ' + turn + ' will go first.')
            gameIsPlaying = True

            while gameIsPlaying:
                if turn == 'player':
                    # Player's turn.
                    page+=game.drawBoard(theBoard)
                    move = game.getPlayerMove(theBoard)
                    game.makeMove(theBoard, playerLetter, move)

                    if game.isWinner(theBoard, playerLetter):
                        game.drawBoard(theBoard)
                        print('Hooray! You have won the game!')
                        gameIsPlaying = False
                    else:
                        if game.isBoardFull(theBoard):
                            game.drawBoard(theBoard)
                            print('The game is a tie!')
                            break
                        else:
                            turn = 'computer'

                else:
                    # Computer's turn.
                    move = game.getComputerMove(theBoard, computerLetter)
                    game.makeMove(theBoard, computerLetter, move)

                    if game.isWinner(theBoard, computerLetter):
                        game.drawBoard(theBoard)
                        print('The computer has beaten you! You lose.')
                        gameIsPlaying = False
                    else:
                        if game.isBoardFull(theBoard):
                            game.drawBoard(theBoard)
                            print('The game is a tie!')
                            break
                        else:
                            turn = 'player'

                if not game.playAgain():
                    break
            page+='</body></html>'
            return [page.encode()]
        else:
            return ['Not logged in. <a href="/">Login</a>'.encode()]

    elif path == '/':
        start_response('200 OK', headers)

        register_or_login = '''<!DOCTYPE html><html><head><title>Register/Login</title></head>
        <body>
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
