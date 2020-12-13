from msvcrt import getch
import os
import random


class Game:
    def __init__(self):
        self.board = [['   ', '   ', '   '], ['   ', '   ', '   '], ['   ', '   ', '   ']]
        self.combs = [[0, 0, 1, 0, 2, 0], [0, 1, 1, 1, 2, 1], [0, 2, 1, 2, 2, 2],
                      [0, 0, 0, 1, 0, 2], [1, 0, 1, 1, 1, 2], [2, 0, 2, 1, 2, 2],
                      [0, 0, 1, 1, 2, 2], [2, 0, 1, 1, 0, 2]]
        self.os_type = os.name
        self.x, self.y = 0, 0
        self.old_x, self.old_y = 0, 0
        self.mark = None
        self.cpu_mark = None
        self.rnd = 1

    def check_if_draw(self):
        for col in self.board:
            for val in col:
                if val == '   ' or val == '| |':
                    return False
        return True

    def check_board(self):
        # Looks at the board to find winner or draw
        for triple in self.combs:
            lst = []
            x1, y1, x2, y2, x3, y3 = triple
            first = self.board[x1][y1].replace('|', ' ')
            second = self.board[x2][y2].replace('|', ' ')
            third = self.board[x3][y3].replace('|', ' ')
            lst.extend([first, second, third])
            if ''.join(lst) == ' X  X  X ':
                return 'X'
            if ''.join(lst) == ' O  O  O ':
                return 'O'
        draw = self.check_if_draw()
        if draw:
            return 'Draw'
        return

    def ai_move(self):
        # Finish or block opponent if he's about to finish
        for i in range(3):
            for triple in self.combs:
                lst = []
                x1, y1, x2, y2, x3, y3 = triple
                first = self.board[x1][y1].replace('|', ' ')
                second = self.board[x2][y2].replace('|', ' ')
                third = self.board[x3][y3].replace('|', ' ')
                lst.extend([first, second, third])
                pos_string = ''.join(lst)
                if i == 0:
                    if pos_string == f' {self.cpu_mark}     {self.cpu_mark} ':
                        self.ai_mark_pos(x2, y2)
                        return
                    if pos_string == f' {self.cpu_mark}  {self.cpu_mark}    ':
                        self.ai_mark_pos(x3, y3)
                        return
                    if pos_string == f'    {self.cpu_mark}  {self.cpu_mark} ':
                        self.ai_mark_pos(x1, y1)
                        return
                if i == 1:
                    if pos_string == f' {self.mark}     {self.mark} ':
                        self.ai_mark_pos(x2, y2)
                        return
                    if pos_string == f' {self.mark}  {self.mark}    ':
                        self.ai_mark_pos(x3, y3)
                        return
                    if pos_string == f'    {self.mark}  {self.mark} ':
                        self.ai_mark_pos(x1, y1)
                        return
                if i == 2:

                    # if one mark present in line and rest of line empty, add another mark
                    if pos_string == f' {self.cpu_mark}       ' or pos_string == f'    {self.cpu_mark}    ':
                        self.ai_mark_pos(x3, y3)
                        return
                    if pos_string == f'       {self.cpu_mark} ':
                        self.ai_mark_pos(x1, y1)
                        return

        # If none from above match, take strategic position: mid first then corners, otherwise take any empty
        if self.board[1][1] == '   ':
            self.ai_mark_pos(1, 1)
            return
        if self.board[0][0] == '   ':
            self.ai_mark_pos(0, 0)
            return
        if self.board[2][0] == '   ':
            self.ai_mark_pos(2, 0)
            return
        if self.board[0][2] == '   ':
            self.ai_mark_pos(0, 2)
            return
        if self.board[2][2] == '   ':
            self.ai_mark_pos(2, 2)
            return
        if self.board[1][0] == '   ':
            self.ai_mark_pos(1, 0)
            return
        if self.board[0][1] == '   ':
            self.ai_mark_pos(0, 1)
            return
        if self.board[1][2] == '   ':
            self.ai_mark_pos(1, 2)
            return
        if self.board[2][1] == '   ':
            self.ai_mark_pos(2, 1)
            return

    def ai_mark_pos(self, aix, aiy):
        pos = list(self.board[aix][aiy])
        pos[0] = ' '
        pos[1] = self.cpu_mark
        pos[2] = ' '
        self.board[aix][aiy] = ''.join(pos)

    def player_mark_pos(self, mode):
        if mode == 0:
            old_pos = list(self.board[self.old_x][self.old_y])
            old_pos[0] = ' '
            old_pos[2] = ' '
            self.board[self.old_x][self.old_y] = ''.join(old_pos)

            new_pos = list(self.board[self.x][self.y])
            new_pos[0] = '|'
            new_pos[2] = '|'
            self.board[self.x][self.y] = ''.join(new_pos)
        elif mode == 1:
            pos = list(self.board[self.x][self.y])
            if pos[1] != ' ':
                return False
            else:
                pos[0] = '|'
                pos[1] = self.mark
                pos[2] = '|'
                self.board[self.x][self.y] = ''.join(pos)
                return True

    def move_cursor(self, direction):

        if direction == 'u':
            if (self.y - 1) < 0:
                return
            else:
                self.old_y = self.y
                self.old_x = self.x
                self.y -= 1
                self.player_mark_pos(0)
        if direction == 'l':
            if (self.x - 1) < 0:
                return
            else:
                self.old_x = self.x
                self.old_y = self.y
                self.x -= 1
                self.player_mark_pos(0)
        if direction == 'r':
            if (self.x + 1) > 2:
                return
            else:
                self.old_x = self.x
                self.old_y = self.y
                self.x += 1
                self.player_mark_pos(0)
        if direction == 'd':
            if (self.y + 1) > 2:
                return
            else:
                self.old_y = self.y
                self.old_x = self.x
                self.y += 1
                self.player_mark_pos(0)

    def display_board(self):
        self.clear_scr()
        print('\n\n')
        print('\t\t\t ##############')
        print('\t\t\t # Round: ', self.rnd, ' #')
        print('\t\t\t ##############')
        print('')
        print('\t\t\tYou are: ', self.mark)
        print('')
        print('\t\t\t     |   |')
        print('\t\t\t  ' + self.board[0][0] + '|' + self.board[1][0] + '|' + self.board[2][0])
        print('\t\t\t     |   |')
        print('\t\t\t -------------')
        print('\t\t\t     |   |')
        print('\t\t\t  ' + self.board[0][1] + '|' + self.board[1][1] + '|' + self.board[2][1])
        print('\t\t\t     |   |')
        print('\t\t\t -------------')
        print('\t\t\t     |   |')
        print('\t\t\t  ' + self.board[0][2] + '|' + self.board[1][2] + '|' + self.board[2][2])
        print('\t\t\t     |   |')
        print('\n')

    def clear_scr(self):
        if self.os_type == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def retry(self):
        play_again = ''
        while play_again != 'Y' and play_again != 'N':
            play_again = input('\t\t\tPlay again? (Y/N): ').upper()
            if play_again == 'Y':
                self.clear_scr()
                self.board = [['   ', '   ', '   '], ['   ', '   ', '   '], ['   ', '   ', '   ']]
                self.rnd = 1
                self.mark = None
                self.run()
            if play_again == 'N':
                print('\t\t\tBye!')
                return

    def run(self):
        while self.mark != 'X' and self.mark != 'O':
            self.mark = input('\n\t\t\tWhat do you want to play as? X or O: ').upper()

        if self.mark == 'X':
            self.cpu_mark = 'O'
        else:
            self.cpu_mark = 'X'
        self.player_mark_pos(0)

        player_1 = random.randint(0, 1)

        while True:

            if player_1 == 1:
                self.ai_move()
                player_1 -= 1
            self.display_board()

            key = ord(getch())
            if key == 72:
                self.move_cursor('u')
            if key == 75:
                self.move_cursor('l')
            if key == 77:
                self.move_cursor('r')
            if key == 80:
                self.move_cursor('d')
            if key == 13:
                empty = self.player_mark_pos(1)
                if empty:
                    self.display_board()
                    result = self.check_board()
                    if result == 'X':
                        if self.mark == 'X':
                            print('\t\t\t[!] Congrats, you won')
                        else:
                            print('\t\t\t[!] You lost')
                        break
                    if result == 'O':
                        if self.mark == 'O':
                            print('\t\t\t[!] Congrats, you won')
                        else:
                            print('\t\t\t[!] You lost')
                        break
                    if result == 'Draw':
                        print('\t\t\tGame ended in a draw !!!')
                        break

                    self.ai_move()
                    self.rnd += 1
                    self.display_board()
                    result = self.check_board()
                    if result == 'X':
                        if self.mark == 'X':
                            print('\t\t\t[!] Congrats, you won')
                        else:
                            print('\t\t\t[!] You lost')
                        break
                    if result == 'O':
                        if self.mark == 'O':
                            print('\t\t\t[!] Congrats, you won')
                        else:
                            print('\t\t\t[!] You lost')
                        break
                    if result == 'Draw':
                        print('\t\t\tGame ended in a draw !!!')
                        break

        self.retry()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
