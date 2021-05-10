import tkinter as tk
from random import randint

# from datetime import datetime
# from PIL import Image, ImageTk

NUM_COLORS = {
    1: '#3d4eeb',
    2: '#1ed115',
    3: '#d62822',
    4: '#8d07e0',
    5: '#7d0b1a',
    6: '#24ede6',
    7: '#cf6c0a',
    8: '#0a0a0a'
}

IMAGES = {
    'BOMB': './images/bomb.png',
    'FLAG': './images/flag.png'
}


class NewButton(tk.Button):

    def __init__(self, master, row, column, *args, **kwargs):
        super(NewButton, self).__init__(master, *args, **kwargs)
        self.row = row
        self.column = column
        self.is_bomb = False

    def __repr__(self):
        return f'Button{self.row}{self.column} {self.is_bomb}'


class MineSweeper:
    buttons = None
    bombs = None
    window = tk.Tk()
    window.title('Minesweeper')
    frm = tk.Frame(master=window, bg='#0a0a0a')
    frm.pack()
    ROW = 10
    COLUMN = 10
    BOMBS = 20

    for row in range(ROW):
        frm.grid_rowconfigure(index=row, minsize=55)
    for column in range(COLUMN):
        frm.grid_columnconfigure(index=column, minsize=55)

    def __init__(self):
        # Заменить Minesweeper.bombs на self.bombs
        MineSweeper.bombs = [[0 for _ in range(MineSweeper.COLUMN)] for _ in range(MineSweeper.ROW)]
        counter = 0
        while counter != MineSweeper.BOMBS:
            row, column = randint(0, MineSweeper.ROW - 1), randint(0, MineSweeper.COLUMN - 1)
            if MineSweeper.bombs[row][column] == 0:
                MineSweeper.bombs[row][column] = 'B'
                counter += 1
        for i in range(len(MineSweeper.bombs)):
            for j in range(len(MineSweeper.bombs[i])):
                if MineSweeper.bombs[i][j] == 'B':
                    continue
                if i > 0:
                    if j != len(MineSweeper.bombs[i]) - 1:
                        if MineSweeper.bombs[i - 1][j + 1] == 'B':
                            MineSweeper.bombs[i][j] += 1
                    if MineSweeper.bombs[i - 1][j] == 'B':
                        MineSweeper.bombs[i][j] += 1
                    if MineSweeper.bombs[i - 1][j - 1] == 'B' and j > 0:
                        MineSweeper.bombs[i][j] += 1
                if MineSweeper.bombs[i][j - 1] == 'B' and j > 0:
                    MineSweeper.bombs[i][j] += 1
                if j != len(MineSweeper.bombs[i]) - 1:
                    if MineSweeper.bombs[i][j + 1] == 'B':
                        MineSweeper.bombs[i][j] += 1
                if i != len(MineSweeper.bombs) - 1:
                    if MineSweeper.bombs[i + 1][j - 1] == 'B' and j > 0:
                        MineSweeper.bombs[i][j] += 1
                    if MineSweeper.bombs[i + 1][j] == 'B':
                        MineSweeper.bombs[i][j] += 1
                    if j != len(MineSweeper.bombs[i]) - 1:
                        if MineSweeper.bombs[i + 1][j + 1] == 'B':
                            MineSweeper.bombs[i][j] += 1

        for i in MineSweeper.bombs:
            print(*i)
        MineSweeper.buttons = []
        for i in range(MineSweeper.ROW):
            row_btn = []
            for j in range(MineSweeper.COLUMN):
                btn = NewButton(master=MineSweeper.frm, width=6, height=3, bg='#99ccff', row=i, column=j)
                row_btn.append(btn)
            MineSweeper.buttons.append(row_btn)

    # Обработка нажатия левой кнопкой мыши
    @staticmethod
    def lmb_click(event, check, i, j):
        MineSweeper.buttons[i][j].unbind('<Button-3>')
        if check:
            MineSweeper.detonate()
        else:
            if MineSweeper.bombs[i][j] != 0:
                MineSweeper.buttons[i][j].grid_forget()
                lbl = tk.Label(master=MineSweeper.frm, text=f'{MineSweeper.bombs[i][j]}',
                               fg=NUM_COLORS[MineSweeper.bombs[i][j]], font='Times 20')
                lbl.grid(row=i, column=j, padx=0.5, pady=0.5, sticky='nsew')
            else:
                MineSweeper.null_button(i, j)

    @staticmethod
    def rmb_click(event, i, j):
        btn = MineSweeper.buttons[i][j]
        if btn['text'] == '?':
            btn.configure(text='')
            btn.bind('<Button-1>',
                     lambda event, is_bomb=btn.is_bomb, i=btn.row, j=btn.column:
                     MineSweeper.lmb_click(event, is_bomb, i, j))
        else:
            btn.configure(text='?')
            btn.unbind('<Button-1>')

    # Обработка нажатия на кнопку с бомбой
    @staticmethod
    def detonate():
        MineSweeper.frm.destroy()
        MineSweeper.window.title('Вы проиграли', )
        label = tk.Label(master=MineSweeper.window, text='Вы проиграли', font='Times 30',
                         width=20, height=10, bg='#99ccff')
        label.pack()

    # Обработка нажатия на кнопку с пустым полем
    @staticmethod
    def null_button(i, j):
        MineSweeper.buttons[i][j].grid_forget()
        lbl = tk.Label(master=MineSweeper.frm,
                       fg='#ffffff', font='Times 20')
        lbl.grid(row=i, column=j, padx=0.5, pady=0.5, sticky='nsew')
        if j < len(MineSweeper.bombs[0]) - 1:
            for column in range(j + 1, len(MineSweeper.bombs[0])):
                if MineSweeper.bombs[i][column] != 0:
                    MineSweeper.lmb_click('NullButton', False, i, column)
                    break
                MineSweeper.buttons[i][column].grid_forget()
                lbl = tk.Label(master=MineSweeper.frm,
                               fg='#ffffff', font='Times 20')
                lbl.grid(row=i, column=column, padx=0.5, pady=0.5, sticky='nsew')
        if j > 0:
            for column in range(j - 1, -1, -1):
                if MineSweeper.bombs[i][column] != 0:
                    MineSweeper.lmb_click('NullButton', False, i, column)
                    break
                MineSweeper.buttons[i][column].grid_forget()
                lbl = tk.Label(master=MineSweeper.frm,
                               fg='#ffffff', font='Times 20')
                lbl.grid(row=i, column=column, padx=0.5, pady=0.5, sticky='nsew')
        if i < len(MineSweeper.bombs) - 1:
            for row in range(i + 1, len(MineSweeper.bombs)):
                if MineSweeper.bombs[row][j] != 0:
                    MineSweeper.lmb_click('NullButton', False, row, j)
                    break
                MineSweeper.buttons[row][j].grid_forget()
                lbl = tk.Label(master=MineSweeper.frm,
                               fg='#ffffff', font='Times 20')
                lbl.grid(row=row, column=j, padx=0.5, pady=0.5, sticky='nsew')
        if i > 0:
            for row in range(i - 1, -1, -1):
                if MineSweeper.bombs[row][j] != 0:
                    MineSweeper.lmb_click('NullButton', False, row, j)
                    break
                MineSweeper.buttons[row][j].grid_forget()
                lbl = tk.Label(master=MineSweeper.frm,
                               fg='#ffffff', font='Times 20')
                lbl.grid(row=row, column=j, padx=0.5, pady=0.5, sticky='nsew')
        if i > 0 and j > 0:
            MineSweeper.lmb_click('NullButton', False, i - 1, j - 1)
        if i > 0 and j < len(MineSweeper.bombs[0]) - 1:
            MineSweeper.lmb_click('NullButton', False, i - 1, j + 1)

    # Привязка кнопок к функциям и создание игрового поля
    @staticmethod
    def create_buttons():
        for row in range(MineSweeper.ROW):
            for column in range(MineSweeper.COLUMN):
                btn = MineSweeper.buttons[row][column]
                btn.bind('<Button-3>', lambda event, i=btn.row, j=btn.column: MineSweeper.rmb_click(event, i, j))
                if MineSweeper.bombs[row][column] == 'B':
                    MineSweeper.buttons[row][column].is_bomb = True
                btn.grid(row=row, column=column, padx=0.5, pady=0.5)
                btn.bind('<Button-1>',
                         lambda event, is_bomb=btn.is_bomb, i=btn.row, j=btn.column:
                         MineSweeper.lmb_click(event, is_bomb, i, j))

    def start_game(self):
        self.create_buttons()
        MineSweeper.window.mainloop()


game = MineSweeper()
game.start_game()
