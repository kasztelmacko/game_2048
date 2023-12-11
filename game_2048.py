import tkinter as tk
import customtkinter as ctk
import random
from tile_colors import tile_colors

ROW = 4
COL = 4

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game")

        self.canvas = tk.Canvas(root, width=400, height=400, bg="lightgray")
        self.canvas.pack(pady=10)

        self.score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 16))
        self.score_label.pack()

        self.create_board()


        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        up_button = tk.Button(button_frame, text="↑", command=self.move_up, height=3, width=10)
        up_button.grid(row=0, column=1, padx=10, pady=(0, 10))

        left_button = tk.Button(button_frame, text="←", command=self.move_left, height=3, width=10)
        left_button.grid(row=1, column=0, padx=10, pady=(0, 10))

        right_button = tk.Button(button_frame, text="→", command=self.move_right, height=3, width=10)
        right_button.grid(row=1, column=3, padx=10, pady=(0, 10))

        down_button = tk.Button(button_frame, text="↓", command=self.move_down, height=3, width=10)
        down_button.grid(row=1, column=1, padx=10, pady=(0, 10))

        restart_button = tk.Button(button_frame, text="Restart", command=self.restart_game , justify="left", width=10)
        restart_button.grid(row=3, column=0, padx=10, pady=(10, 0))

        quit_button = tk.Button(button_frame, text="Quit", command=root.destroy, justify="right", width=10)
        quit_button.grid(row=3, column=3, padx=10, pady=(10, 0))

        self.arr = self.new_board()
        self.total_score = 0

        self.update_board()

    def create_board(self):
        cell_size = 100
        self.rectangles = []
        self.texts = []
        for row in range(ROW):
            for col in range(COL):
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                self.rectangles.append(rect)
                text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="", font=("Helvetica", 16))
                self.texts.append(text)

    def update_board(self):
        for i in range(ROW):
            for j in range(COL):
                value = self.arr[i][j]
                index = i * COL + j
                color = tile_colors.get(str(value), 'white')
                self.canvas.itemconfig(self.rectangles[index], fill=color)
                self.canvas.itemconfig(self.texts[index], text=str(value) if value != 0 else "")
        self.score_label.config(text="Score: {}".format(self.total_score))

    def restart_game(self):
        self.arr = self.new_board()
        self.total_score = 0
        self.update_board()

    def new_board(self):
        arr = self.start_game()
        self.losuj(arr)
        self.losuj(arr)
        self.losuj(arr)
        return arr

    def losuj(self, plansza):
        puste_pole = [[row, col] for row in range(ROW) for col in range(COL) if plansza[row][col] == 0]
        if puste_pole:
            row, col = random.choice(puste_pole)
            plansza[row][col] = 2 if random.random() < 0.9 else 4

    def start_game(self):
        plansza = [[0 for _ in range(COL)] for _ in range(ROW)]
        return plansza

    def reverse(self, mat):
        new_mat = []
        for i in range(ROW):
            new_mat.append([])
            for j in range(COL):
                new_mat[i].append(mat[i][3 - j])
        return new_mat

    def transp(self, mat):
        new_mat = [[0 for i in range(ROW)] for i in range(COL)]
        for i in range(ROW):
            for j in range(COL):
                new_mat[i][j] = mat[j][i]
        return new_mat

    def merge(self, mat):
        score_increment = 0
        for i in range(ROW):
            for j in range(COL - 1):
                if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                    mat[i][j] += mat[i][j]
                    score_increment += mat[i][j]
                    mat[i][j + 1] = 0
        return mat, score_increment

    def compress(self, mat):
        new_mat = [[0 for i in range(ROW)] for i in range(COL)]
        for i in range(ROW):
            pos = 0
            for j in range(COL):
                if mat[i][j] != 0:
                    new_mat[i][pos] = mat[i][j]
                    pos += 1
        return new_mat

    def move_left(self):
        st1, score_increment = self.merge(self.compress(self.arr))
        st2 = self.compress(st1)
        self.arr = st2
        self.total_score += score_increment
        self.losuj(self.arr)
        self.update_board()

    def move_right(self):
        st0 = self.reverse(self.arr)
        st1, score_increment = self.merge(self.compress(st0))
        st2 = self.compress(st1)
        st3 = self.reverse(st2)
        self.arr = st3
        self.total_score += score_increment
        self.losuj(self.arr)
        self.update_board()

    def move_up(self):
        st0 = self.transp(self.arr)
        st1, score_increment = self.merge(self.compress(st0))
        st2 = self.compress(st1)
        st3 = self.transp(st2)
        self.arr = st3
        self.total_score += score_increment
        self.losuj(self.arr)
        self.update_board()

    def move_down(self):
        st0 = self.transp(self.arr)
        st = self.reverse(st0)
        st1, score_increment = self.merge(self.compress(st))
        st2 = self.compress(st1)
        st3 = self.reverse(st2)
        st4 = self.transp(st3)
        self.arr = st4
        self.total_score += score_increment
        self.losuj(self.arr)
        self.update_board()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
