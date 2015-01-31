# coding: utf-8


class Tetris(object):

    """
        俄罗斯方块游戏Python终端版
    """

    # 盘面存储list
    board = None  # 这是一个一维数组可以模拟二维数组　或者更高维
    row = 20 # 行数
    col = 10 # 列数
    score = 0  # 得分
    block_list = [] #方块集合

    def __init__(self):
        self.reset()
        self.create_block()

    def reset(self):
        self.board = ['0' for _ in range(self.row * self.col)]
        self.score = 0

    def create_block(self):
        """创建方块积木集合"""
        self.block_list = []

        deviation = self.col / 2 - 2

        I_piece = Block()
        I_piece.name = 'I'
        I_piece.piece = [0 + deviation, 1 + deviation, 2 + deviation, 3 + deviation, 4 + deviation]

        J_piece = Block()
        J_piece.name = 'J'
        J_piece.piece = [0 + deviation, self.col + deviation + 0, self.col + deviation + 1, self.col + deviation + 2]

        L_piece = Block()
        L_piece.name = 'L'
        L_piece.piece = [2 + deviation, self.col + deviation + 0, self.col + deviation + 1, self.col + deviation + 2]

        O_piece = Block()
        O_piece.name = 'O'
        O_piece.piece = [0 + deviation, 1 + deviation, self.col + deviation + 0, self.col + deviation + 1]

        S_piece = Block()
        S_piece.name = 'S'
        S_piece.piece = [1 + deviation, 2 + deviation, self.col + deviation + 0, self.col + deviation + 1]

        Z_piece = Block()
        Z_piece.name = 'Z'
        Z_piece.piece = [0 + deviation, 1 + deviation, self.col + deviation + 1, self.col + deviation + 2]

        T_piece = Block()
        T_piece.name = 'T'
        T_piece.piece = [1 + deviation, self.col + deviation + 0, self.col  + deviation+ 1, self.col + deviation + 2]

        self.block_list.append(I_piece)
        self.block_list.append(J_piece)
        self.block_list.append(L_piece)
        self.block_list.append(O_piece)
        self.block_list.append(Z_piece)
        self.block_list.append(T_piece)




class Block(object):
    """
        方块对象
    """
    name = ""
    piece = []
    color = '█'

    def __init__(self):
        super(Block, self).__init__()




import sys
import tty
import termios


class Control(object):

    '''
        方向键控制器
    '''
    UP, DOWN, RIGHT, LEFT = 65, 66, 67, 68

    # Vim keys
    K, J, L, H = 107, 106, 108, 104

    __key_aliases = {
        K: UP,
        J: DOWN,
        L: RIGHT,
        H: LEFT,
    }

    __key_map = {65: 'UP',
                 66: 'DOWN',
                 67: 'RIGHT',
                 68: 'LEFT'
                 }

    def __init__(self):
        self.__fd = sys.stdin.fileno()
        self.__old = termios.tcgetattr(self.__fd)

    def __getKey(self):
        """Return a key pressed by the user"""
        try:
            tty.setcbreak(sys.stdin.fileno())
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            ch = sys.stdin.read(1)
            return ord(ch) if ch else None
        finally:
            termios.tcsetattr(self.__fd, termios.TCSADRAIN, self.__old)

    def getKey(self):
        """
        same as __getKey, but handle arrow keys
        """
        k = self.__getKey()
        if k == 27:
            k = self.__getKey()
            if k == 91:
                k = self.__getKey()

        return self.__key_map.get(self.__key_aliases.get(k, k))



import os
import time
import threading
import copy
import sys
from random import choice

class GameArry(object):

    tetris = None
    now_piece = None
    islive = True
    __key = Control()  # 　获得终端按键
    __key

    def __init__(self):
        self.tetris = Tetris()
        self.running = True
    def start_drop(self):
        """ 开始下落 """
        while self.running:
            time.sleep(0.1)

            color = self.now_piece.color

            is_bottom = True
            for index, px in enumerate(self.now_piece.piece):
                now_piece = px + self.tetris.col # 下一行
                if now_piece > len(self.tetris.board):
                    is_bottom = False
                    break
                elif now_piece < len(self.tetris.board):
                    if self.tetris.board[now_piece] == color and now_piece not in self.now_piece.piece:
                        is_bottom = False
                        break

            # 可以移动
            if is_bottom:
                # 清空之前的打印
                for px in self.now_piece.piece:
                    self.tetris.board[px] = '0'
                for index, px in enumerate(self.now_piece.piece):
                    now_piece = px + self.tetris.col
                    self.tetris.board[now_piece] = color
                    self.now_piece.piece[index] = now_piece
                self.print_ui()
            else:
                self.check_score() #检查是否得分
                self.load_piece() #加载新的方块

  

    def load_game(self):
        p = ''
        self.islive = True

        for i in xrange(1,30):
            os.system("clear")
            print '游戏载入中....\n'
            print p + '>'
            p = p + '='
            time.sleep(0.02)

        self.tetris.score = 0 #清零分数
        self.load_piece()
        
        # 积木下落的线程
        t = threading.Thread(target=self.start_drop)
        t.setDaemon(True)
        t.start()

        while self.running:
            key = self.__key.getKey()
            if self.islive:
                if key == 'LEFT':
                    self.left()
                elif key == 'RIGHT':
                    self.right()
                elif key == 'UP':
                    pass
                elif key == 'DOWN':
                    pass



    def load_piece(self):

        """
            加载新的方块
        """

        self.tetris.create_block()
        piece = copy.copy(choice(self.tetris.block_list))
        color = piece.color

        is_next = True

        for px in piece.piece:
            if self.tetris.board[px] != '0':
                is_next = False
                break

        if is_next:
            self.now_piece = piece
            for index, px in enumerate(piece.piece):
                self.tetris.board[px] = color
            self.print_ui()
        else:
            self.now_piece = piece
            for index, px in enumerate(piece.piece):
                self.tetris.board[px] = color
            self.print_ui()
            print "\n-------Game Over!-------\n"
            self.islive = False
            self.running = False
            sys.exit(0)
            


    def check_score(self):

        """
            检查是否得分
        """
        this_score = 0 # 本次得分
        remove_row_list = [] #要消除的行集合
        index = 0
        for row in xrange(1, self.tetris.row + 1):
            i = 0
            for col in xrange(1, self.tetris.col + 1):
                if self.tetris.board[index] == '0':
                    i = i - 1
                index = index + 1

            # 如果这一行全是满的
            if i == 0:
                remove_row_list.append(row) #记录要消除的行
                this_score = this_score + 1

        # 加分
        self.tetris.score = self.tetris.score + this_score

        # 消除
        remove_px_list = [] #要消除的像素
        index = 0
        for row in xrange(1, self.tetris.row + 1):
            for col in xrange(1, self.tetris.col + 1):
                if row in remove_row_list:
                    remove_px_list.append(index)
                index = index + 1

        #反向遍历删除要消除的像素
        for px in remove_px_list[::-1]:
            del self.tetris.board[px]

        #补齐删除掉的行
        new_board = ['0' for _ in range(len(remove_row_list) * self.tetris.col)]
        self.tetris.board = new_board + self.tetris.board

        self.print_ui()


    def move(self, direction):
        """ 
            左右移动
        """

        i = 0

        if direction == 'left':
            i = -1
        else:
            i = 1

        is_bottom = True

        for index, px in enumerate(self.now_piece.piece):
            now_piece = px + i
            if now_piece/self.tetris.col > px/self.tetris.col or now_piece/self.tetris.col < px/self.tetris.col:
                is_bottom = False
                break
            elif self.tetris.board[now_piece] != "0" and now_piece not in self.now_piece.piece:
                is_bottom = False
                break

        # 可以移动
        if is_bottom:
            color = self.now_piece.color
            for px in self.now_piece.piece:
                self.tetris.board[px] = '0'

            for index, px in enumerate(self.now_piece.piece):
                now_piece = px + i
                self.tetris.board[now_piece] = color
                self.now_piece.piece[index] = now_piece

            self.print_ui()

    def left(self):
        self.move('left')

    def right(self):
        self.move('right')

    def print_ui(self):
        os.system("clear")
        print '┌' + (self.tetris.row * '─') + '─┐'

        index = 0
        for row in xrange(1, self.tetris.row + 1):
            print '│',
            for col in xrange(1, self.tetris.col + 1):
                if self.tetris.board[index] == '0':
                    print ' ',
                else :
                    print self.tetris.board[index],
                index = index + 1

            print '│\n',

        print '└' + (self.tetris.row * '─') + '─┘'
        print '得分: ' + str(self.tetris.score)


if __name__ == '__main__':
    game = GameArry()
    game.load_game()

    













        


