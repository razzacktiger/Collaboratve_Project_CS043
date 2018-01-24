import random
class TTT:
    def __init__(self, board):
        self.board = board
    def drawBoard(self, board):
        # This function prints out the board that it was passed.
        # "board" is a list of 10 strings representing the board (ignore index 0)
        boardpage = '''<form style="line-height:5px"><pre>         |    |<br>
         ''' + board[7] + ''' | ''' + board[8] + ''' | ''' + board[9] + '''<br>
         |    |<br>
        -----------------<br>
         |    |<br>
         ''' + board[4] + ''' | ''' + board[5] + ''' | ''' + board[6] + '''<br>
         |    |<br>
        -----------------<br>
         |    |<br>
         ''' + board[1] + ''' | ''' + board[2] + ''' | ''' + board[3] + '''<br>
         |    |</pre><br>
         <input type="submit" value="Make Move"></form>
        '''
        return boardpage

    def whoGoesFirst(self):
        # Randomly choose the player who goes first.
        if random.randint(0, 1) == 0:
            return 'X'
        else:
            return 'O'

    def playAgain(self):
        # This function returns True if the player wants to play again, otherwise it returns False.
        print('Do you want to play again? (yes or no)')
        return input().lower().startswith('y')

    def makeMove(self, board, letter, move):
        board[int(move)] = letter
        return board

    def isWinner(self, bo, le):
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

    def isSpaceFree(self, board, move):
        # Return true if the passed move is free on the passed board.
        return board[move] == ' '
    def isBoardFull(self, board, move):
        def isSpaceFree(board, move):
            # Return true if the passed move is free on the passed board.
            return board[move] == ' '
        # Return True if every space on the board has been taken. Otherwise return False.
        for move in range(1, 10):
            if isSpaceFree(board, move):
                return False
        return True
