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