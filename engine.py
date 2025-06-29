import copy

from piece import Piece, Pawn, Empty, Rook, Bishop, Knight, Queen, King
from position import Pos


class Engine:
  def __init__(self, is_white):
    self.is_white = is_white

  def get_available_moves(self, board, color):
    raise NotImplementedError()

  def next_move(self):
    raise NotImplementedError()

class StuckFishV1(Engine):
  pass


