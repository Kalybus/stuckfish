from position import Pos

class Slot:
  def __init__(self, name = ""):
    self.name = name

  def get_icon(self):
    return ""

  def __str__(self):
    return self.name

class Empty(Slot):
  def __init__(self):
    Slot.__init__(self, "Empty")

class Piece(Slot):
  def __init__(self, name, icons, color):
    Slot.__init__(self, name)
    if color is None or color != "black":
      self.white = True
    else:
      self.white = False
    self.icons = icons

  def move(self, pos, dx, dy):
    return Pos(pos.x + dx, pos.y - dy) if self.is_white else Pos(pos.x - dx, pos.y + dy)

  def get_icon(self):
    return self.icons[1 if self.white else 0]

  @property
  def is_white(self):
    return self.white

  @property
  def is_black(self):
    return not self.white

  @property
  def opposite_color(self):
    return not self.white

# Chessboard pieces
class Pawn(Piece):
  def __init__(self, color):
    Piece.__init__(self, "pion", ["♙", "♟"], color)

class Rook(Piece):
  def __init__(self, color):
    Piece.__init__(self, "tour",["♖", "♜"], color)

class Knight(Piece):
  def __init__(self, color):
    Piece.__init__(self, "cavalier", ["♘", "♞"], color)

class Bishop(Piece):
  def __init__(self, color):
    Piece.__init__(self, "fou", ["♗", "♝"], color)

class Queen(Piece):
  def __init__(self, color):
    Piece.__init__(self, "reine", ["♕", "♛"], color)

class King(Piece):
  def __init__(self, color):
    Piece.__init__(self, "roi", ["♔", "♚"], color)
