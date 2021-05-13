import tkinter as tk
# shuffle позволяет перемещивать коллекцию
from random import shuffle


# Переобределяем стандартный вывод кнопки
class MyButton(tk.Button):
    def __init__(self, master, x, y, number, *args, **kwargs):
        # вызываем метод init у самой кнопки
        super(MyButton, self).__init__(master, width=3, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False

    def __repr__(self):
        return f'My Button ({self.x}:{self.y}) #{self.number} {self.is_mine}'


class MineSweeper:
    root = tk.Tk()
    ROW = 10
    COLUMNS = 7
    MINES = 15

    # Инициализация игры. В этот момент создаются все данные, которые
    # в дальнейшем будут обрабатываться.
    def __init__(self):
        self.buttons = []
        count = 1  # порядковый номер кнопки на доске
        for i in range(MineSweeper.ROW):
            temp = []
            for j in range(MineSweeper.COLUMNS):
                btn = MyButton(MineSweeper.root, x=i, y=j, number=count)
                # после создания кнопки опредяляем действие
                btn.config(command=lambda button=btn: self.click(button))
                # btn.grid(row=i, column=j)  # => create_widgets
                temp.append(btn)
                count += 1
            self.buttons.append(temp)

    @staticmethod
    def click(clicked_button: MyButton):
        if clicked_button.is_mine:
            clicked_button.config(text='*', background='red', disabledforeground='black')
        else:
            clicked_button.config(text=clicked_button.number, disabledforeground='black')
        clicked_button.config(state='disabled')

    def create_widgets(self):
        for i in range(MineSweeper.ROW):
            for j in range(MineSweeper.COLUMNS):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)

    def start(self):
        self.create_widgets()
        self.insert_mines()
        self.print_buttons()
        MineSweeper.root.mainloop()

    def print_buttons(self):
        for row_btn in self.buttons:
            print(row_btn)

    def insert_mines(self):
        index_mines = self.get_mines_places()
        print(index_mines)
        for row_btn in self.buttons:
            for btn in row_btn:  # для каждого ряда проходим кнопки
                if btn.number in index_mines:
                    btn.is_mine = True

    @staticmethod
    def get_mines_places():
        indexes = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROW + 1))
        shuffle(indexes)  # Перемещиваем список кнопок
        return indexes[:MineSweeper.MINES]


game = MineSweeper()
game.start()
