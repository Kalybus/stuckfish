import tkinter as tk

from piece import Piece


class Display:
  def __init__(self):
    self.root = None
    self.canvas = None
    self.canvas_size = 480
    self.reset()

  def reset(self):
    self.root = tk.Tk()
    self.root.title("Stuckfish chessboard")
    self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size)
    self.canvas.pack()

  def draw(self, board):
    square_size = self.canvas_size // 8
    colors = ["#F0D9B5", "#B58863"]  # Light and dark squares
    for row in range(8):
      for col in range(8):
        x1 = col * square_size
        y1 = row * square_size
        x2 = x1 + square_size
        y2 = y1 + square_size

        color = colors[(row + col) % 2]
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        piece = board.data[row][col]
        if isinstance(piece, Piece):
          self.canvas.create_text(
            x1 + square_size // 2,
            y1 + square_size // 2,
            text=piece.get_icon(),
            font=("Arial", square_size // 2),
            fill="white" if piece.color else "black"
          )

  def draw_moves(self, moves, color):
    # self.canvas.create_rectangle(10, 10, 300, 300, fill="yellow")
    for pos, new_poses in moves.items():
      x, y = pos.get_coords()
      x1 = x * 60 + (28 if color == "blue" else 32)
      y1 = y * 60 + 30
      for new_pos in new_poses:
        x_new, y_new = new_pos.get_coords()
        x2 = x_new * 60 + (28 if color == "blue" else 32)
        y2 = y_new * 60 + 30
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

  def display(self):
    self.root.mainloop()