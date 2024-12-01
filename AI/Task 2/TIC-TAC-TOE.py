import customtkinter as ctk
import math

class TicTacToeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe")
        self.geometry("380x580")
        self.resizable(False, False)
        self.configure(bg="#1f1f2e")

        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.turn = "X"  # Human
        self.widgets()

    def widgets(self):
        # Title Label
        self.title_label = ctk.CTkLabel(
            self,
            text="Tic-Tac-Toe",
            font=("Arial", 30, "bold"),
            text_color="#ffffff",
            bg_color="#1f1f2e",
        )
        self.title_label.pack(pady=20)

        # Frame for buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="#2e2e38")
        self.button_frame.pack(pady=10)

        # grid of buttons for the game board
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = ctk.CTkButton(
                    self.button_frame,
                    text="",
                    font=("Arial", 20, "bold"),
                    width=100,
                    height=100,
                    fg_color="#3b3b4f",
                    hover_color="#4f4f6b",
                    text_color="#f8f9fa",
                    corner_radius=10,
                    command=lambda row=i, col=j: self.click(row, col),
                )
                self.buttons[i][j].grid(row=i, column=j, padx=10, pady=10)

        # Information Label
        self.info_label = ctk.CTkLabel(
            self,
            text="Your Turn",
            font=("Arial", 18),
            text_color="#e5e5e5",
        )
        self.info_label.pack(pady=20)

        # Play Again Button (initially non-responsive)
        self.play_again_button = ctk.CTkButton(
            self,
            text="Play Again",
            font=("Arial", 16, "bold"),
            width=200,
            fg_color="#00aaff",
            hover_color="#007acc",
            text_color="#ffffff",
            command=self.reset,
            state="disabled",
        )
        self.play_again_button.pack(pady=10)

    def click(self, row, col):
        if self.board[row][col] == " " and self.turn == "X":
            # Human move
            self.board[row][col] = "X"
            self.buttons[row][col].configure(text="X", state="disabled")
            winner = self.check_winner()
            if winner or self.is_draw():
                self.end(winner)
                return

            # AI move
            self.info_label.configure(text="AI's Turn")
            self.after(500, self.ai)

    def ai(self):
        row, col = self.best_moves()
        self.board[row][col] = "O"
        self.buttons[row][col].configure(text="O", state="disabled")
        winner = self.check_winner()
        if winner or self.is_draw():
            self.end(winner)
        else:
            self.info_label.configure(text="Your Turn")

    def check_winner(self):
        # Check rows, columns, and diagonals
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != " ":
                return row[0]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != " ":
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != " ":
            return self.board[0][2]
        return None

    def is_draw(self):
        return all(cell != " " for row in self.board for cell in row)

    def best_moves(self):
        best_score = -math.inf
        move = (-1, -1)
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = "O"
                    score = self.minimax(0, False)
                    self.board[i][j] = " "
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        return move

    def minimax(self, depth, is_maximizing):
        winner = self.check_winner()
        if winner == "X":
            return -1
        elif winner == "O":
            return 1
        elif self.is_draw():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == " ":
                        self.board[i][j] = "O"
                        score = self.minimax(depth + 1, False)
                        self.board[i][j] = " "
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == " ":
                        self.board[i][j] = "X"
                        score = self.minimax(depth + 1, True)
                        self.board[i][j] = " "
                        best_score = min(score, best_score)
            return best_score

    def end(self, winner):
        if winner:
            self.info_label.configure(text=f"{winner} Wins!")
        else:
            self.info_label.configure(text="It's a Draw!")
        # Disable all buttons
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(state="disabled")

        # Enable Play Again button
        self.play_again_button.configure(state="normal")

    def reset(self):
        # Reset the game state
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.turn = "X"
        self.info_label.configure(text="Your Turn")
        self.play_again_button.configure(state="disabled")

        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(text="", state="normal")


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    app = TicTacToeApp()
    app.mainloop()
