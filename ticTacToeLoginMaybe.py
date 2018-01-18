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
            page = str('<!DOCTYPE html><html><head><title>TTT Game</title></head><body style="text-align:center;">' +
                    '<h1>Tic-Tac-Toe</h1>')
            game = TTT
            # Reset the board
            theBoard = ['', '<input type="radio" name="playerMove" value="1">',
                        '<input type="radio" name="playerMove" value="2">',
                        '<input type="radio" name="playerMove" value="3">',
                        '<input type="radio" name="playerMove" value="4">',
                        '<input type="radio" name="playerMove" value="5">',
                        '<input type="radio" name="playerMove" value="6">',
                        '<input type="radio" name="playerMove" value="7">',
                        '<input type="radio" name="playerMove" value="8">',
                        '<input type="radio" name="playerMove" value="9">']
            playerMove = params['playerMove'][0] if 'playerMove' in params else None
            # ---- erase this later ---- #
            page += TTT.drawBoard(game, theBoard)
            page += ('<br>' + playerMove)
            return [page.encode()]
            # ---- erase this later ---- #
            playerLetter1, playerLetter2 = game.inputPlayerLetter()
            turn = game.whoGoesFirst()
            print('The ' + turn + ' will go first.') #HTML
            gameIsPlaying = True

            while gameIsPlaying:
                if turn == 'player1': #***update program name defs
                    # Player's turn.
                    page+=game.drawBoard(theBoard)   #We should add an input box or create a hyperlink system like 
                    #                                 we did with the last unit 5 project to click on the box that we want 
                    #                                 the player to make a move in.
                    move = game.getPlayerMove(theBoard)
                    game.makeMove(theBoard, playerLetter1, move) #***update program name defs

                    if game.isWinner(theBoard, playerLetter1): #***update program name defs
                        game.drawBoard(theBoard)
                        print('Hooray! You have won the game!') #HTML
                        gameIsPlaying = False 
                    else:
                        if game.isBoardFull(theBoard):
                            game.drawBoard(theBoard)
                            print('The game is a tie!') #HTML page+= stuff... you know
                            break     #End of game replace with some HTML and link to restart
                        else:
                            turn = 'player2'  #***again update program name def
             
                if turn == 'player2': #***update program name defs
                    # Computer's turn(Testing purposes). #Really player2's turn but for now we are testing with an AI
                    # We will eventually later convert all this code back to almost the same identicle stuff as player 1's turn
                    move = game.getComputerMove(theBoard, playerLetter1)   #We will proabably take out Computermove function 
                                                                           #and replace it with player2move or sometime 
                    game.makeMove(theBoard, playerLetter1, move)

                    if game.isWinner(theBoard, playerLetter1):
                        game.drawBoard(theBoard)
                        print('The computer has beaten you! You lose.')    #change this stuff up along with the phrase
                        gameIsPlaying = False
                    else:
                        if game.isBoardFull(theBoard):
                            game.drawBoard(theBoard)
                            print('The game is a tie!')  #HTML fix this stuff
                            break
                        else:
                            turn = 'player1'

                if not game.playAgain():
                    break      #update this stuff with hyperlink s not "break"
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
