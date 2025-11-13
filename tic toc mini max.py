import tkinter as tk
from tkinter import messagebox, simpledialog
import math
import time

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        master.title("Tic Tac Toe")

        self.n = 0
        self.board = []
        self.buttons = []
        self.player_X = False
        self.player_O = False
        self.current_player = "X"
        self.move_count = 0
        self.start_time = 0
        self.xscore = 0
        self.oscore = 0

        self.board_frame = tk.Frame(master)
        self.board_frame.pack()

        self.size_label = tk.Label(master, text="Enter the board size (3-10):")
        self.size_label.pack()
        self.size_entry = tk.Entry(master)
        self.size_entry.pack()
        self.start_button = tk.Button(master, text="Start Game", command=self.start_game)
        self.start_button.pack()

    def start_game(self):
        try:
            self.n = int(self.size_entry.get())
            if 3 <= self.n <= 10:
                self.board = [[" " for _ in range(self.n)] for _ in range(self.n)]
                self.buttons = []
                self.player_X = self.get_player_type("X") == "computer"
                self.player_O = self.get_player_type("O") == "computer"
                self.current_player = "X"
                self.move_count = 0
                self.start_time = time.time()

                self.create_board_gui()

                if self.player_X and self.current_player == "X":
                    self.computer_move()
            else:
                messagebox.showerror("Error", "Invalid input! Please enter a number between 3 and 10.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please enter a number.")

    def create_board_gui(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.buttons = []
        for i in range(self.n):
            row_buttons = []
            for j in range(self.n):
                button = tk.Button(self.board_frame, text=" ", width=4, height=2,
                                   command=lambda row=i, col=j: self.button_click(row, col))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        self.status_label = tk.Label(self.board_frame, text=f"Player {self.current_player}'s turn")
        self.status_label.grid(row=self.n, columnspan=self.n)

    def button_click(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            self.move_count += 1

            if self.is_board_full():
                self.end_game("It's a draw!")
                return

            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label.config(text=f"Player {self.current_player}'s turn")

            if (self.current_player == "X" and self.player_X) or (self.current_player == "O" and self.player_O):
                self.master.after(100, self.computer_move)

    def computer_move(self):
        row, col = self.best_move(self.board, self.current_player, self.move_count)
        self.button_click(row, col)

    def get_player_type(self, player_mark):
        player_type = simpledialog.askstring("Player Type",
                                             f"Is player {player_mark} a computer or human? (computer/human)",
                                             parent=self.master)
        if player_type and player_type.lower() in ["computer", "human"]:
            return player_type.lower()
        else:
            messagebox.showerror("Error", "Invalid input! Please enter 'computer' or 'human'.")
            return self.get_player_type(player_mark)
    def check_winner(self, player):
        n = len(self.board)
        for i in range(n):
            if all([self.board[i][j] == player for j in range(n)]) or all([self.board[j][i] == player for j in range(n)]):
                return True
        if all([self.board[i][i] == player for i in range(n)]) or all([self.board[i][n - 1 - i] == player for i in range(n)]):
            return True
        return False

    def is_board_full(self):
        return all([cell != " " for row in self.board for cell in row])

    def extract_board_elements(self):
        n = len(self.board)
        elements = []

        for row in self.board:
            elements.append(row)

        for j in range(n):
            column = [self.board[i][j] for i in range(n)]
            elements.append(column)


        elements.append([self.board[i][i] for i in range(n)])
        elements.append([self.board[i][n - 1 - i] for i in range(n)])

        for d in range(1, n):
            lower_main = [self.board[i + d][i] for i in range(n - d)]
            lower_anti = [self.board[i + d][n - 1 - i] for i in range(n - d)]
            upper_main = [self.board[i][i + d] for i in range(n - d)]
            upper_anti = [self.board[i][n - 1 - (i + d)] for i in range(n - d)]

            if lower_main: elements.append(lower_main)
            if lower_anti: elements.append(lower_anti)
            if upper_main: elements.append(upper_main)
            if upper_anti: elements.append(upper_anti)

        return elements

    def calculate_player_score(self):
        x_score, o_score = 0, 0

        for element in self.extract_board_elements():
            count = 0
            for sign in element:
                if sign == 'X':
                    count += 1
                else:
                    if count > 2:
                        x_score += (count - 2) + (count - 3)
                    count = 0
            if count > 2:
                x_score += (count - 2) + (count - 3)

        for element in self.extract_board_elements():
            count = 0
            for sign in element:
                if sign == 'O':
                    count += 1
                else:
                    if count > 2:
                        o_score += (count - 2) + (count - 3)
                    count = 0
            if count > 2:
                o_score += (count - 2) + (count - 3)

        return x_score, o_score

    def minimax(self, board, depth, is_maximizing, alpha, beta, max_depth):
        if self.check_winner("O"):
            return 10 - depth
        if self.check_winner("X"):
            return depth - 10
        if self.is_board_full() or depth == max_depth:
            x_score, o_score = self.calculate_player_score()
            return o_score - x_score

        if is_maximizing:
            max_eval = -math.inf
            for i in range(len(board)):
                for j in range(len(board)):
                    if board[i][j] == " ":
                        board[i][j] = "O"
                        eval = self.minimax(board, depth + 1, False, alpha, beta, max_depth)
                        board[i][j] = " "
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = math.inf
            for i in range(len(board)):
                for j in range(len(board)):
                    if board[i][j] == " ":
                        board[i][j] = "X"
                        eval = self.minimax(board, depth + 1, True, alpha, beta, max_depth)
                        board[i][j] = " "
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    def best_move(self, board, player, move_count):
        max_depth = 5 if move_count <= 10 else 5
        best_val = -math.inf if player == "O" else math.inf
        best_move = (-1, -1)

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == " ":
                    board[i][j] = player
                    move_val = self.minimax(board, 0, player == "X", -math.inf, math.inf, max_depth)
                    board[i][j] = " "

                    if (player == "O" and move_val > best_val) or (player == "X" and move_val < best_val):
                        best_move = (i, j)
                        best_val = move_val

        return best_move

    def end_game(self, message):
        self.xscore, self.oscore = self.calculate_player_score()
        end_time = time.time()
        elapsed_time = end_time - self.start_time

        result_message = f"{message}\n"
        result_message += f"Player X score: {self.xscore}, Player O score: {self.oscore}\n"
        if self.xscore > self.oscore:
            result_message += 'Player X wins!\n'
        elif self.oscore == self.xscore:
            result_message += 'It\'s a draw!\n'
        else:
            result_message += 'Player O wins!\n'
        result_message += f"Time taken: {elapsed_time:.2f} seconds"

        messagebox.showinfo("Game Over", result_message)
        for i in range(self.n):
            for j in range(self.n):
                self.buttons[i][j].config(state=tk.DISABLED)

root = tk.Tk()
gui = TicTacToeGUI(root)
root.mainloop()