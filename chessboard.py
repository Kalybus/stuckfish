
from piece import Slot, Rook, Knight, Bishop, Queen, King, Pawn, Piece, Empty


class Chessboard:
  def __init__(self):
    self.data = []
    for _ in range(8):
      row = [Empty() for _ in range(8)]
      self.data.append(row)

  def reset(self):
    self.data = [
      [Rook("black"), Knight("black"), Bishop("black"), Queen("black"), King("black"), Bishop("black"), Knight("black"), Rook("black")],
      [Pawn("black") for _ in range(8)],
      [Empty() for _ in range(8)],
      [Empty() for _ in range(8)],
      [Empty() for _ in range(8)],
      [Empty() for _ in range(8)],
      [Pawn("white") for _ in range(8)],
      [Rook("white"), Knight("white"), Bishop("white"), Queen("white"), King("white"), Bishop("white"), Knight("white"), Rook("white")],
    ]

  def get_slot(self, pos):
    x, y = pos.get_coords()
    if x < 0 or x >= 8 or y < 0 or y >= 8:
      return None
    return self.data[y][x]

  def set_slot(self, pos, slot):
    x, y = pos.get_coords()
    self.data[y][x] = slot

  def get_piece(self, pos):
    slot = self.get_slot(pos)
    if isinstance(slot, Piece):
      return slot
    return None

  def move(self, cur_pos, new_pos):
    piece = self.get_slot(cur_pos)
    if not isinstance(piece, Slot):
      return

    self.set_slot(cur_pos, Empty())
    self.set_slot(new_pos, piece)
