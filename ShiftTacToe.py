###########################################################################
# File: ShiftTacToe.py
# Author: Tim Wylie
# Date: 7/2023
# Description: A class that implements a shift-tac-toe game that can have
#   any number of rows, columns, or extra columns (shift). There are two
#   versions that differ in the data structure used. 
#   
#   - ShiftTacToe only stores r x c, which also eliminates some annoying
#       math. 
#   Has a ToString method to easily use the objects in a cmd line.
###########################################################################


class ShiftTacToe:
    
    def __init__(self, r=6, c=7, s=2, ist=0):
        #fix ist > s
        ist = ist if ist <= s else s
        self.Set(r,c,s,ist)

    
    #rows, cols are playable area
    #shift is how much it can shift outside the playable area (standard is 2)
    def Set(self, rows, cols, shift,initshift):
        self.MAX_ROW_DIGITS=3
        self.MAX_COL_DIGITS=3
        self.EMPTYSPOT = ' '
        self.ROWS = rows
        self.COLS = cols
        self.SHIFT = shift
        #for badly set initial shifts
        if initshift > self.SHIFT:
            initshift = self.SHFIFT
        
        #set up board memory
        self.BOARD = [[' ' for i in range(cols)] for j in range(rows)]
        
        #shift positions
        self.POSITIONS = [int(initshift) for i in range(rows)]
        
    #adds a piece to column
    def Add(self, col, piec):
        if col >= self.COLS or col < 0:
            return False
        
        if self.BOARD[0][col] != self.EMPTYSPOT:
            return False
        else:
            self.BOARD[0][col] = piec
        
        self.Compact()
        return True
    
    #moves a row left or right
    #direc is either 1 or -1
    def Shift(self, row, direc):
        #valid direction
        if direc != 1 and direc != -1:
            return False
        #valid row
        if row < 0 or row >= self.ROWS:
            return False
        #valid shift    
        if self.POSITIONS[row] + direc < 0 or self.POSITIONS[row] + direc > self.SHIFT:
            return False
        #apply
        self.POSITIONS[row] = self.POSITIONS[row] + direc
        
        #move elements in row
        colrange = range(self.COLS-1) if direc == 1 else range(self.COLS-1, -1, -1)
        
        for i in colrange:
            self.BOARD[row][i] = self.BOARD[row][i+direc]
            
        #the last cell needs to be deleted (because the thing moved)
        blankindex = 0 if direc == -1 else self.COLS-1
        self.BOARD[row][blankindex]=self.EMPTYSPOT

       
        self.Compact()
        return True
    
    #enforces gravity and removes pieces outside board area
    def Compact(self):
        #should be rewritten to go by columns
        for i in range(self.ROWS):
            for c in range(self.COLS):
                for r in range(self.ROWS-1, 0, -1):
                    if self.BOARD[r-1][c] != self.EMPTYSPOT and self.BOARD[r][c] == self.EMPTYSPOT:
                            self.BOARD[r][c] = self.BOARD[r-1][c]
                            self.BOARD[r-1][c] = self.EMPTYSPOT
                            
    
    def ToString(self):
        rtemp = "{:"+ str(self.MAX_ROW_DIGITS) +"}"
        ctemp = "{:"+ str(self.MAX_COL_DIGITS) +"}"
        fmtr = lambda x: rtemp.format(x)
        fmtc = lambda x: ctemp.format(x)
        #assume we need shift area on both sides of board
        #col labels
        print(fmtr(' '),end='') #for row label
        #shift spaces
        [print(fmtc(' '),end='') for i in range(self.SHIFT)]
        #board bar |
        print(' ',end='') 
        [print(fmtc(str(i)),end='') for i in range(self.COLS)]
        #board bar
        print(' ',end='') 
        #[print(' ',end='')) for i in range(self.SHIFT)]
        print(' ') #newline
        
        #print(self.BOARD)
        for r in range(self.ROWS):
            print(fmtr(r),end='')
            #make space if no shift
            for i in range(self.SHIFT):
                if self.POSITIONS[r] + i < self.SHIFT:
                    print(fmtc(' '), end='')
                else:
                    print(fmtc('-'), end='')
            print('|', end='')
            #print main board area
            for c in range(self.COLS):
                o = '-' if self.BOARD[r][c] == self.EMPTYSPOT else self.BOARD[r][c]
                print(fmtc(o), end='')
            print('|', end='')
            #print after board
            for i in range(self.SHIFT):
                if self.POSITIONS[r] + i < self.SHIFT:
                    print(fmtc('-'), end='')
                else:
                    print(fmtc(' '), end='')
                

            print(' ') #for newline