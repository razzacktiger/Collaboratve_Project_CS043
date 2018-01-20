import random
class TTT:
    def drawBoard(self, board):
        # This function prints out the board that it was passed.
        # "board" is a list of 10 strings representing the board (ignore index 0)
        boardpage = '''<form style="line-height:5px"><pre>         |    |</br>
         ''' + board[7] + ''' | ''' + board[8] + ''' | ''' + board[9] + '''</br>
         |    |</br>
        -----------------</br>
         |    |</br>
         ''' + board[4] + ''' | ''' + board[5] + ''' | ''' + board[6] + '''</br>
         |    |</br>
        -----------------</br>
         |    |</br>
         ''' + board[1] + ''' | ''' + board[2] + ''' | ''' + board[3] + '''</br>
         |    |</pre></br>
         <input type="submit" value="Make Move"></form>
        '''
        return boardpage

#    def inputPlayerLetter(self, letter):
#        # Lets the player type which letter they want to be.
#        letter = ''
#        while not (letter == 'X' or letter == 'O'):
#            page = '''<h1>Player one: pick a letter to play with</h1>'''
#            letter = '''<form action="/play/game"><br>
#            X<input type="radio" name="playerLetter" value="X"><br>
#            O<input type="radio" name="playerLetter" value="O"><br>
#            <input type="submit" value="Choose Letter"></form>'''
#            letter = parameters['playerLetter'][0] if 'playerLetter' in parameters else None
#            if letter == 'X':
#                return ['X', 'O', page]
#            elif letter == 'O':
#                return ['X', 'O', page]

    def whoGoesFirst(self):
        # Randomly choose the player who goes first.
        if random.randint(0, 1) == 0:
            return 'player1'
        else:
            return 'player2'

    def playAgain(self):
        # This function returns True if the player wants to play again, otherwise it returns False.
        print('Do you want to play again? (yes or no)')
        return input().lower().startswith('y')

    def makeMove(board, letter, move):
        board[int(move)] = letter

    def isWinner(bo, le):
        # Given a board and a player's letter, this function returns True if that player has won.
        # We use bo instead of board and le instead of letter so we don't have to type as much.
        return ((bo[7] == le and bo[8] == le and bo[9] == le) or  # across the top
                (bo[4] == le and bo[5] == le and bo[6] == le) or  # across the middle
                (bo[1] == le and bo[2] == le and bo[3] == le) or  # across the bottom
                (bo[7] == le and bo[4] == le and bo[1] == le) or  # down the left side
                (bo[8] == le and bo[5] == le and bo[2] == le) or  # down the middle
                (bo[9] == le and bo[6] == le and bo[3] == le) or  # down the right side
                (bo[7] == le and bo[5] == le and bo[3] == le) or  # diagonal
                (bo[9] == le and bo[5] == le and bo[1] == le))  # diagonal

    def getBoardCopy(board):
        # Make a duplicate of the board list and return it the duplicate.
        dupeBoard = []

        for i in board:
            dupeBoard.append(i)

        return dupeBoard

    def isSpaceFree(board, move):
        # Return true if the passed move is free on the passed board.
        return board[move] == ' '

    def chooseRandomMoveFromList(board, movesList):
        # Returns a valid move from the passed list on the passed board.
        # Returns None if there is no valid move.
        possibleMoves = []
        for i in movesList:
            if isSpaceFree(board, i):
                possibleMoves.append(i)

        if len(possibleMoves) != 0:
            return random.choice(possibleMoves)
        else:
            return None

    def isBoardFull(board):
        # Return True if every space on the board has been taken. Otherwise return False.
        for i in range(1, 10):
            if isSpaceFree(board, i):
                return False
        return True


#            page = ('<!DOCTYPE html><html><head><title>TTT Game</title></head><body style="text-align:center;">' +
#                    '<h1>Tic-Tac-Toe</h1>')
#            page += '''<h1>Player one: pick a letter to play with</h1>
#                                <form><br>
#                                X<input type="radio" name="playerLetter1" value="X"><br>
#                                O<input type="radio" name="playerLetter1" value="O"><br>
#                                <input type="submit" value="Choose Letter"></form>'''
#            page += '</body></html>'
#            if 'playerLetter1' in params:
#                letter = params['playerLetter1'][0]
#                if letter == 'X':
#                    game.playerLetter1 = 'X'
#                    game.playerLetter2 = 'O'
#                    return ['Player one is X, player two is O. </br><a href="/play?playerLetter1=X>Play the game</a>']
#                elif letter == 'O':
#                    game.playerLetter1 = 'X'
#                    game.playerLetter2 = 'O'
#                    return ['Player one is O, player two is X. </br><a href="/play?playerLetter1=O>Play the game</a>']
