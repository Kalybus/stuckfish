class Pos:
  def __init__(self, x = 0, y = 0):
    self.x = x # A to H (cols)
    self.y = y # 8 to 1 (reversed rows)

  # Convert chess position to board coordinates
  @staticmethod
  def coord_to_pos(x, y):
    col_mapper = {
      0: 'A',
      1: 'B',
      2: 'C',
      3: 'D',
      4: 'E',
      5: 'F',
      6: 'G',
      7: 'H',
    }
    return col_mapper[x], 8 - y

  # Convert chess position to board coordinates
  @staticmethod
  def pos_to_coord(a, b):
    col_mapper = {
      'A': 0,
      'B': 1,
      'C': 2,
      'D': 3,
      'E': 4,
      'F': 5,
      'G': 6,
      'H': 7,
    }
    return col_mapper[a], 8 - b

  def get_coords(self):
    return self.x, self.y

  def get_pos(self):
    return Pos.coord_to_pos(self.x, self.y)

  def is_inbound(self):
    if self.x < 0 or self.y < 0 or self.x > 7 or self.y > 7:
      return False
    return True

  def __str__(self):
    return '%s%d' % Pos.coord_to_pos(self.x, self.y)

  def __repr__(self):
    return 'Pos(%s%d)' % Pos.coord_to_pos(self.x, self.y)

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  def __hash__(self):
    return self.x * 10 + self.y

class ChessPos(Pos):
  def __init__(self, a=0, b=0):
    super().__init__(*Pos.pos_to_coord(a, b))
