import tkinter as tk
# shuffle позволяет перемещивать коллекцию
from random import shuffle

colors = {
    1: 'blue',
    2: '#008200',
    3: '#FF0000',
    4: '#000084',
    5: '#840000',
    6: '#008284',
    7: '#840084',
    8: '#000000'
}


# Переобределяем стандартный вывод кнопки
class MyButton(tk.Button):
    def __init__(self, master, x, y, number=0, *args, **kwargs):
        # вызываем метод init у самой кнопки
        super(MyButton, self).__init__(master, width=3, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False

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

    def click(self, clicked_button: MyButton):
        if clicked_button.is_mine:
            clicked_button.config(text='*', background='red', disabledforeground='black')
            clicked_button.is_open = True
        else:
            color = colors.get(clicked_button.count_bomb, 'black')
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)

        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)  # эффект нажатия кнопки

    def breadth_first_search(self, btn: MyButton):
        """
        Функция обхода в ширину.
        Открывает при нажатии на кнопку все соседние кнопки, в которых
        не содержатся бомбы.
        """
        queue = [btn]

        while queue:
            cur_btn = queue.pop()  # достаем из очереди первую кнопку
            color = colors.get(cur_btn.count_bomb, 'black')

            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text='', disabledforeground=color)

            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)  # эффект нажатия кнопки

            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:  # соседи по оси x
                    for dy in [-1, 0, 1]:  # соседи по оси y
                        # оставляем только соседей сверху, справа, слева
                        # и снизу
                        if not abs(dx - dy) == 1:
                            continue

                        # координаты след. кнопки
                        next_btn = self.buttons[x + dx][y + dy]
                        # Проверка:
                        # 1. Кнопка не была открыта
                        # 2. Не является барьерной
                        # 3. Не находится в очереди
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.ROW and \
                                1 <= next_btn.y <= MineSweeper.COLUMNS and next_btn not in queue:
                            queue.append(next_btn)

    def create_widgets(self):
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)

    def open_all_buttons(self):
        for i in range(MineSweeper.ROW + 2):
            for j in range(MineSweeper.COLUMNS + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*', background='red', disabledforeground='black')
                # elif btn.count_bomb == 1:
                #     btn.config(text=btn.count_bomb, foreground='blue')
                # elif btn.count_bomb == 2:
                #     btn.config(text=btn.count_bomb, fg='green')
                #
                # по умолчанию проверяется среди ключей словаря
                elif btn.count_bomb in colors:
                    color = colors.get(btn.count_bomb, 'black')
                    btn.config(text=btn.count_bomb, fg=color)

    def start(self):
        self.create_widgets()
        self.insert_mines()
        self.count_mines_in_cells()
        self.print_buttons()
        # self.open_all_buttons()
        MineSweeper.root.mainloop()

    def print_buttons(self):
        # проходимся по всем кнопкам, которые не являются барьерными
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('B', end='')
                else:
                    print(btn.count_bomb, end='')
            print()  # перенос для нового ряда

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

    def count_mines_in_cells(self):
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    # находим соседей
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            # получаем всех возможных соседей тек. кнопки
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            # если сосед мина, увеличиваем счетчик
                            if neighbour.is_mine:
                                count_bomb += 1
                btn.count_bomb = count_bomb

    @staticmethod
    def get_mines_places():
        indexes = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROW + 1))
        shuffle(indexes)  # Перемещиваем список кнопок
        return indexes[:MineSweeper.MINES]


game = MineSweeper()
game.start()
