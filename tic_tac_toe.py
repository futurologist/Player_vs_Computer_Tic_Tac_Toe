"""
Created on Sat Aug 10 01:10:46 2019
@author: Futurologist

Tic Tac Toe game between a player and a computer. Computer minimizes 
its chance to lose by traversing the binary tree of space of states of the game.
In the process, at every mive the computer tries to maximize its win function and 
to minimize the player's win function
"""

# Object describeing the state of the game, together with relevant methods, among which
# is the method  weigh_state(self, turn), performing a minimax traversal of the space of states 
# of the game and the calculation of 
# the computer's and the player's win functions
class State(object):
    def __init__(self):
        self.board = [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]]
        self.P1 = []
        self.P2 = []
        self.available = [(1,1), (1,2), (1,3),
                          (2,1), (2,2), (2,3),
                          (3,1), (3,2), (3,3)]
        self.weights = {(1,1): 0, (1,2): 0, (1,3): 0,
                        (2,1): 0, (2,2): 0, (2,3): 0,
                        (3,1): 0, (3,2): 0, (3,3): 0} 
    def make_copy(self):
        '''
        position is a tuple (i,j) of cooridnates
        mark is an integer, either 1 or 2
        
        Return: a copy of the State
        '''
        copy = State()
        for i in range(3):
            #for j in range(3):
            #    copy.board[i][j] = self.board[i][j]
            copy.board[i] = self.board[i].copy()
        copy.P1 = self.P1.copy()
        copy.P2 = self.P2.copy()
        copy.available = self.available.copy()
        copy.weights = self.weights.copy()
        return copy
    def position_is_available(self, position):
        if position in self.available:
            return True
        return False
    def make_a_move(self, position, turn):
        '''
        position is a tuple (i,j) of cooridnates
        turn is an integer, either 0 or 1
        '''
        self.board[position[0]-1][position[1]-1] = turn
        if turn == 1:
            self.P1.append(position)
        elif turn == 2:
            self.P2.append(position)
        self.available.remove(position)
        del self.weights[position]  
        return None
    def game_is_over(self):
        for i in range(3):
            p = self.board[i][0] * self.board[i][1] * self.board[i][2]
            if p == 1:
                return 1
            elif p == 8:
                return 2
            p = self.board[0][i] * self.board[1][i] * self.board[2][i]
            if p == 1:
                return 1
            elif p == 8:
                return 2
        p = self.board[0][0] * self.board[1][1] * self.board[2][2]
        if p == 1:
            return 1
        elif p == 8:
            return 2
        p = self.board[2][0] * self.board[1][1] * self.board[0][2]
        if p == 1:
            return 1
        elif p == 8:
            return 2
        if len(self.available) == 0:
            return 0
        return -1 
    def weigh_state(self, turn):
        game_over = self.game_is_over()
        if game_over == 1:
            return -10
        elif game_over == 2:
            return 10
        elif game_over == 0:
            return 0
        else: 
            copy = State()
            if turn == 1: #turn = turn %2 + 1 == 1
                value = 10
                for position in self.available:
                    copy = self.make_copy()
                    copy.make_a_move(position, 1)
                    value = min(value, copy.weigh_state(2))
                return value
            else:
                value = -10
                for position in self.available:
                    copy = self.make_copy()
                    copy.make_a_move(position, 2)
                    value = max(value, copy.weigh_state(1))
                return value
    def weigh_moves(self, turn):  
        '''
        turn = 1 or 2, where 1 is player, 2 is computer
        ''' 
        copy = State()
        for position in self.available:
            copy = self.make_copy()
            copy.make_a_move(position, turn)
            self.weights[position] = copy.weigh_state(turn % 2 + 1)
        return None
    def make_calc_move(self):
        max_value = - 100
        position_max = (0,0) 
        for position in self.available:
            if self.weights[position] >= max_value:
                position_max = position
                max_value = self.weights[position]
        self.make_a_move(position_max, 2)
    def display_state(self):
        board = [['   ', ' 1 ', ' 2 ', ' 3 '],
                 ['   ', '---', '---', '---'],
                 ['1| ', '[ ]', '[ ]', '[ ]'],
                 ['2| ', '[ ]', '[ ]', '[ ]'],
                 ['3| ', '[ ]', '[ ]', '[ ]']]                
        for position in self.P1:
            board[position[0]+1][position[1]] = ' X '
        for position in self.P2:
            board[position[0]+1][position[1]] = ' O '
        for i in range(5):
            row = ''
            for j in range(4):
                row += board[i][j]
            print(row)
        return None    



import random

# Exectution of the game:
# To play the game, fist compile the whole code and then 
# simply type tic_tac_toe() in python's console
def tic_tac_toe():
    digits = '123'
    sep = ",./ ;:'|"
    S = State()
    #S.make_a_move((1,1), 2)
    turn = 1 
    S.display_state()
    start = input('Do you want to go first or second: (type 1 or 2)')
    if start == '2':
       S.make_a_move((random.randint(1, 3), random.randint(1, 3)), 2) 
       S.display_state()
    while True:
        p = input(f'Please make a move in the format: row,column ')
        while len(p) < 3 or not(p[0] in digits and p[2] in digits and p[1] in sep):
            print(' ')
            print('The position is improperly formatted! Try again.')
            print(' ')
            p = input(f'Please make a move in the format: row,column ')    
        position = (int(p[0]), int(p[2]))   
        while not S.position_is_available(position):
            print(' ')
            print('The position is not available! Choose another one.')
            print(' ')
            p = input(f'Please make a move in the format: row,column ')
            while len(p) < 3 or not(p[0] in digits and p[2] in digits and p[1] in sep):
                print(' ')
                print('The position is improperly formatted! Try again.')
                print(' ')
                p = input(f'Please make a move in the format: row,column ')
            position = (int(p[0]), int(p[2]))
        S.make_a_move(position, turn)
        S.display_state()
        print(' ')
        print(' ')
        if S.game_is_over() == turn:
            print('You win!')
            break
        elif S.game_is_over() == 0:
            print('The game is tied!')
            break
        turn = turn % 2 + 1
        S.weigh_moves(turn)
        #print(S.weights)
        S.make_calc_move()
        S.display_state()
        if S.game_is_over() == turn:
            print(' ')
            print('Computer wins!')
            break
        elif S.game_is_over() == 0:
            print('The game is tied!')
            break
        turn = turn % 2 + 1
    return None
