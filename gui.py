import tkinter as tk
from tkinter import messagebox
import threading

from board import createBoard, is_valid_move, make_move, check_winner, switch_turn
from agent import minimax

class TaflGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Viking Chess")
        self.root.configure(bg="#2C3E50")

        self.board = []
        self.size = 11
        self.cell_size = 50
        self.current_player = 'A'
        self.selected_cell = None
        
        self.play_ai = False
        self.ai_player = None
        self.ai_depth = 2
        self.ai_is_thinking = False
        self.ai_best_move = None

        self.setup_ui()

    def setup_ui(self):
        self.menu_frame = tk.Frame(self.root, bg="#2C3E50", pady=20)
        self.menu_frame.pack()

        tk.Label(self.menu_frame, text="Viking Chess", font=("Helvetica", 24, "bold"), fg="white", bg="#2C3E50").pack(pady=10)

        tk.Button(self.menu_frame, text="Player vs Player", font=("Helvetica", 14), width=20, 
                  command=lambda: self.start_game(ai=False)).pack(pady=5)
        
        tk.Label(self.menu_frame, text="Play against AI:", font=("Helvetica", 12), fg="white", bg="#2C3E50").pack(pady=(15, 0))
        
        ai_frame = tk.Frame(self.menu_frame, bg="#2C3E50")
        ai_frame.pack()
        
        tk.Button(ai_frame, text="Play as Defenders (Easy)", 
                  command=lambda: self.start_game(ai=True, human_side='D', depth=1)).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(ai_frame, text="Play as Defenders (Medium)", 
                  command=lambda: self.start_game(ai=True, human_side='D', depth=2)).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(ai_frame, text="Play as Defenders (Hard)", 
                  command=lambda: self.start_game(ai=True, human_side='D', depth=3)).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(ai_frame, text="Play as Attackers (Easy)", 
                  command=lambda: self.start_game(ai=True, human_side='A', depth=1)).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(ai_frame, text="Play as Attackers (Medium)", 
                  command=lambda: self.start_game(ai=True, human_side='A', depth=2)).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(ai_frame, text="Play as Attackers (Hard)", 
                  command=lambda: self.start_game(ai=True, human_side='A', depth=3)).grid(row=1, column=2, padx=5, pady=5)

    def start_game(self, ai, human_side='D', depth=2):
        self.play_ai = ai
        if ai:
            self.ai_player = 'A' if human_side == 'D' else 'D'
            self.ai_depth = depth

        self.board = createBoard(self.size)
        self.current_player = 'A'
        
        self.menu_frame.destroy()
        self.build_game_screen()
        self.draw_board()
        
        if self.play_ai and self.current_player == self.ai_player:
            self.trigger_ai_turn()

    def build_game_screen(self):
        self.status_label = tk.Label(self.root, text="Turn: Attackers", font=("Helvetica", 16, "bold"), fg="white", bg="#2C3E50")
        self.status_label.pack(pady=10)

        canvas_size = self.size * self.cell_size
        self.canvas = tk.Canvas(self.root, width=canvas_size, height=canvas_size, bg="#DEB887", highlightthickness=0)
        self.canvas.pack(padx=20, pady=10)
        
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def get_moves_for_piece(self, r, c, piece):
        moves = []
        size = self.size
        for rt in range(size):
            if is_valid_move(self.board, r, c, rt, c, piece):
               moves.append((rt, c))
        for ct in range(size):
            if is_valid_move(self.board, r, c, r, ct, piece):
               moves.append((r, ct))
        return moves
    
    def draw_board(self):
        self.canvas.delete("all")
        corners = [(0, 0), (0, self.size-1), (self.size-1, 0), (self.size-1, self.size-1)]
        throne = (self.size // 2, self.size // 2)
        valid_moves = []
        if self.selected_cell:
           sr, sc = self.selected_cell
           piece = self.board[sr][sc]
           valid_moves = self.get_moves_for_piece(sr, sc, piece)
        
        for r in range(self.size):
            for c in range(self.size):
                x0, y0 = c * self.cell_size, r * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                
                fill_color = "#F5DEB3" 
                
                if (r, c) in corners or (r, c) == throne:
                    fill_color = "#CD853F"
                
                if self.selected_cell == (r, c):
                    fill_color = "#98FB98"
                
                elif (r, c) in valid_moves:
                    fill_color = "#90EE90"

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill_color, outline="#8B4513")

                piece = self.board[r][c]
                if piece != '.':
                    pad = 5
                    if piece == 'A':
                        self.canvas.create_oval(x0+pad, y0+pad, x1-pad, y1-pad, fill="#2C3E50", outline="red", width=2)
                    elif piece == 'D':
                        self.canvas.create_oval(x0+pad, y0+pad, x1-pad, y1-pad, fill="#ECF0F1", outline="#3498DB", width=2)
                    elif piece == 'K':
                        self.canvas.create_oval(x0+pad, y0+pad, x1-pad, y1-pad, fill="#F1C40F", outline="#E67E22", width=3)
                        self.canvas.create_text(x0 + self.cell_size/2, y0 + self.cell_size/2, text="K", font=("Helvetica", 14, "bold"))

    def on_canvas_click(self, event):
        if self.ai_is_thinking:
            return

        c = event.x // self.cell_size
        r = event.y // self.cell_size

        if not (0 <= r < self.size and 0 <= c < self.size):
            return

        if self.selected_cell is None:
            piece = self.board[r][c]
            target_pieces = ['A'] if self.current_player == 'A' else ['D', 'K']
            
            if piece in target_pieces:
                self.selected_cell = (r, c)
                self.draw_board()
        
        else:
            r1, c1 = self.selected_cell
            
            if r1 == r and c1 == c:
                self.selected_cell = None
                self.draw_board()
                return

            piece_char = self.board[r1][c1]
            
            if make_move(self.board, r1, c1, r, c, piece_char):
                self.selected_cell = None
                self.end_turn()
            else:
                self.selected_cell = None
                self.draw_board()

    def end_turn(self):
        self.draw_board()
        
        status = check_winner(self.board)
        if status != "Ongoing":
            self.status_label.config(text=f"GAME OVER: {status}")
            messagebox.showinfo("Game Over", status)
            return

        self.current_player = switch_turn(self.current_player)
        
        turn_text = "Attackers" if self.current_player == 'A' else "Defenders"
        self.status_label.config(text=f"Turn: {turn_text}")

        if self.play_ai and self.current_player == self.ai_player:
            self.trigger_ai_turn()

    def trigger_ai_turn(self):
        self.ai_is_thinking = True
        self.status_label.config(text="AI is thinking...", fg="#F1C40F")
        self.root.update()

        threading.Thread(target=self.ai_worker, daemon=True).start()
        
        self.root.after(100, self.check_ai_result)

    def ai_worker(self):
        _, self.ai_best_move = minimax(self.board, self.ai_depth, float('-inf'), float('inf'), True, self.current_player, self.ai_player)

    def check_ai_result(self):
        if self.ai_best_move is not None:
            ro, co, rt, ct, piece = self.ai_best_move
            make_move(self.board, ro, co, rt, ct, piece)
            
            self.ai_best_move = None
            self.ai_is_thinking = False
            self.status_label.config(fg="white")
            self.end_turn()
        else:
            self.root.after(100, self.check_ai_result)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaflGUI(root)
    root.mainloop()