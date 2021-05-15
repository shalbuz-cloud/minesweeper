import tkinter as tk
# shuffle позволяет перемещивать коллекцию
from random import shuffle


# Переобределяем стандартный вывод кнопки
class MyButton(tk.Button):
    def __init__(self, master, x, y, number=0, *args, **kwargs):
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
        # добавляем 2 колонки и 2 ряда - барьерные элементы, чтобы не выйти
        # за пределы списка
        for i in range(MineSweeper.ROW + 2):
            temp = []
            for j in range(MineSweeper.COLUMNS + 2):
                btn = MyButton(MineSweeper.root, x=i, y=j)
                # после создания кнопки опредяляем действие
                btn.config(command=lambda button=btn: self.click(button))
                # btn.grid(row=i, column=j)  # => create_widgets
                temp.append(btn)
            self.buttons.append(temp)

    @staticmethod
    def click(clicked_button: MyButton):
        if clicked_button.is_mine:
            clicked_button.config(text='*', background='red', disabledforeground='black')
        else:
            clicked_button.config(text=clicked_button.number, disabledforeground='black')
        clicked_button.config(state='disabled')

    def create_widgets(self):
        for i in range(MineSweeper.ROW + 2):
            for j in range(MineSweeper.COLUMNS + 2):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)

    def open_all_buttons(self):
        for i in range(MineSweeper.ROW + 2):
            for j in range(MineSweeper.COLUMNS + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*', background='red', disabledforeground='black')
                else:
                    btn.config(text=btn.number, disabledforeground='black')

    def start(self):
        self.create_widgets()
        self.insert_mines()
        self.print_buttons()
        self.open_all_buttons()
        MineSweeper.root.mainloop()

    def print_buttons(self):
        for row_btn in self.buttons:
            print(row_btn)

    def insert_mines(self):
        index_mines = self.get_mines_places()
        print(index_mines)
        count = 1
        # не берем 1 и последниие колонки и 1 и последние ряды
        for i in range(1, MineSweeper.ROW + 1):
            # для каждого ряда проходим кнопки
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]  # находим кнопку по индексу
                btn.number = count
                if btn.number in index_mines:
                    btn.is_mine = True
                count += 1

    @staticmethod
    def get_mines_places():
        indexes = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROW + 1))
        shuffle(indexes)  # Перемещиваем список кнопок
        return indexes[:MineSweeper.MINES]


game = MineSweeper()
game.start()
