import tkinter as tk

from piece import Piece


class Display:
  def draw(self, board):
    root = tk.Tk()
    root.title("Stuckfish chessboard")

    canvas_size = 480
    square_size = canvas_size // 8

    canvas = tk.Canvas(root, width=canvas_size, height=canvas_size)
    canvas.pack()
    colors = ["#F0D9B5", "#B58863"]  # Light and dark squares
    for row in range(8):
      for col in range(8):
        x1 = col * square_size
        y1 = row * square_size
        x2 = x1 + square_size
        y2 = y1 + square_size

        color = colors[(row + col) % 2]
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        piece = board.data[row][col]
        if isinstance(piece, Piece):
          canvas.create_text(
            x1 + square_size // 2,
            y1 + square_size // 2,
            text=piece.get_icon(),
            font=("Arial", square_size // 2),
            fill="white" if piece.white else "black"
          )

    root.mainloop()