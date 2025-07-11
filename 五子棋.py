import tkinter as tk
from tkinter import messagebox

BOARD_SIZE = 15
GRID_SIZE = 40
PADDING = 20
PIECE_RADIUS = 15

class Gobang:
    def __init__(self, root):
        self.root = root
        self.root.title("五子棋游戏")

        # 初始界面
        self.start_frame = tk.Frame(root)
        self.start_frame.pack()
        tk.Label(self.start_frame, text="欢迎进入五子棋游戏", font=('Helvetica', 16)).pack(pady=20)
        tk.Button(self.start_frame, text="Start", width=10, command=self.start_game).pack(pady=10)
        tk.Button(self.start_frame, text="Quit", width=10, command=root.quit).pack(pady=10)

        # 游戏画布
        self.canvas = tk.Canvas(root, width=BOARD_SIZE * GRID_SIZE + 2 * PADDING,
                                height=BOARD_SIZE * GRID_SIZE + 2 * PADDING, bg="burlywood")

        # 状态记录
        self.record_black = []
        self.record_white = []
        self.record_all = []
        self.turn = 'black'  # 初始回合是黑方（左键）

    def start_game(self):
        self.start_frame.destroy()
        self.canvas.pack()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.callback_black)  # 左键：黑方
        self.canvas.bind("<Button-3>", self.callback_white)  # 右键：白方

    def draw_board(self):
        for i in range(BOARD_SIZE):
            self.canvas.create_line(PADDING, PADDING + i * GRID_SIZE,
                                    PADDING + (BOARD_SIZE - 1) * GRID_SIZE, PADDING + i * GRID_SIZE)
            self.canvas.create_line(PADDING + i * GRID_SIZE, PADDING,
                                    PADDING + i * GRID_SIZE, PADDING + (BOARD_SIZE - 1) * GRID_SIZE)

    def get_index(self, x, y):
        col = round((x - PADDING) / GRID_SIZE)
        row = round((y - PADDING) / GRID_SIZE)
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return row, col
        return None, None

    def draw_piece(self, row, col, color):
        x = PADDING + col * GRID_SIZE
        y = PADDING + row * GRID_SIZE
        self.canvas.create_oval(x - PIECE_RADIUS, y - PIECE_RADIUS,
                                x + PIECE_RADIUS, y + PIECE_RADIUS,
                                fill=color)

    def callback_black(self, event):
        if self.turn != 'black':
            return  # 非黑方回合，不允许黑下
        row, col = self.get_index(event.x, event.y)
        if row is None or col is None:
            return
        pos = row * BOARD_SIZE + col
        if pos in self.record_all:
            return
        self.draw_piece(row, col, "black")
        self.record_black.append((row, col))
        self.record_all.append(pos)
        if self.check_win(self.record_black):
            messagebox.showinfo("游戏结束", "黑方获胜！")
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<Button-3>")
        else:
            self.turn = 'white'  # 切换回合

    def callback_white(self, event):
        if self.turn != 'white':
            return  # 非白方回合，不允许白下
        row, col = self.get_index(event.x, event.y)
        if row is None or col is None:
            return
        pos = row * BOARD_SIZE + col
        if pos in self.record_all:
            return
        self.draw_piece(row, col, "white")
        self.record_white.append((row, col))
        self.record_all.append(pos)
        if self.check_win(self.record_white):
            messagebox.showinfo("游戏结束", "白方获胜！")
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<Button-3>")
        else:
            self.turn = 'black'  # 切换回合

    def check_win(self, records):
        for row, col in records:
            if (self.count_line(row, col, 0, 1, records) + self.count_line(row, col, 0, -1, records) >= 4 or
                self.count_line(row, col, 1, 0, records) + self.count_line(row, col, -1, 0, records) >= 4 or
                self.count_line(row, col, 1, 1, records) + self.count_line(row, col, -1, -1, records) >= 4 or
                self.count_line(row, col, 1, -1, records) + self.count_line(row, col, -1, 1, records) >= 4):
                return True
        return False

    def count_line(self, row, col, dr, dc, records):
        count = 0
        for i in range(1, 5):
            r = row + dr * i
            c = col + dc * i
            if (r, c) in records:
                count += 1
            else:
                break
        return count

if __name__ == "__main__":
    root = tk.Tk()
    game = Gobang(root)
    root.mainloop()
