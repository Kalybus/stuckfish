from piece import Piece, Pawn, Slot, Empty, Rook, Bishop, Knight, Queen
from position import Pos


class Engine:
  def __init__(self, board, is_white):
    self.board = board
    self.is_white = is_white

  def get_available_moves(self):
    raise NotImplementedError()

  def next_move(self):
    raise NotImplementedError()


class StuckFishV1(Engine):
  def get_available_moves(self):
    for row in range(8):
      for col in range(8):
        pos = Pos(col, row)
        piece = self.board.get_slot(pos)
        if isinstance(piece, Piece) and piece.is_white == self.is_white:
          moves = self.get_pos_moves(piece, pos)
          # moves = piece.get_moves(piece_pos)
          print(f"{piece} at {pos} can be moved to {moves}")

  def get_pos_moves(self, piece, pos):
    valid_moves = []
    if isinstance(piece, Pawn) or isinstance(piece, Queen):
      # General case
      move_one = piece.move(pos, 0, 1)
      move_one_slot = self.board.get_slot(move_one)
      if isinstance(move_one_slot, Empty):
        valid_moves.append(move_one)

      # Start case
      move_two = piece.move(pos, 0, 2)
      move_two_slot = self.board.get_slot(move_two)
      if self.is_at_start_y(piece, pos) and isinstance(move_one_slot, Empty) and isinstance(move_two_slot, Empty):
        valid_moves.append(move_two)

      # Attack case
      for enemy_pos in [piece.move(pos, 1, 1), piece.move(pos, -1, 1)]:
        enemy = self.board.get_piece(enemy_pos)
        if isinstance(enemy, Piece) and enemy.opposite_color == self.is_white:
          valid_moves.append(enemy_pos)
      # TODO Implement en-passant

    if isinstance(piece, Rook) or isinstance(piece, Queen):
      for i in range(1,8):
        move_one = piece.move(pos, 0, i)
        move_one_slot = self.board.get_slot(move_one)
        if isinstance(move_one_slot, Empty):
          valid_moves.append(move_one)
          continue
        if isinstance(move_one_slot, Piece) and move_one_slot.opposite_color == self.is_white:
          valid_moves.append(move_one)
        break

    if isinstance(piece, Bishop) or isinstance(piece, Queen):
      # Left diagonal
      for i in range(1,8):
        move_diag = piece.move(pos, i, i)
        move_diag_slot = self.board.get_slot(move_diag)
        if isinstance(move_diag_slot, Empty):
          valid_moves.append(move_diag)
          continue
        if isinstance(move_diag_slot, Piece) and move_diag_slot.opposite_color == self.is_white:
          valid_moves.append(move_diag)
        break

      # Right diagonal
      for i in range(1,8):
        move_diag = piece.move(pos, -i, i)
        move_diag_slot = self.board.get_slot(move_diag)
        if isinstance(move_diag_slot, Empty):
          valid_moves.append(move_diag)
          continue
        if isinstance(move_diag_slot, Piece) and move_diag_slot.opposite_color == self.is_white:
          valid_moves.append(move_diag)
        break

    if isinstance(piece, Knight):
      moves = [
        piece.move(pos, 2, 1),
        piece.move(pos, 1, 2),
        piece.move(pos, 2, -1),
        piece.move(pos, 1, -2),
        piece.move(pos, -2, 1),
        piece.move(pos, -1, 2),
        piece.move(pos, -2, -1),
        piece.move(pos, -1, -2),
      ]
      for move in moves:
        move_slot = self.board.get_slot(move)
        if isinstance(move_slot, Empty):
          valid_moves.append(move)
          continue
        if isinstance(move_slot, Piece) and move_slot.opposite_color == self.is_white:
          valid_moves.append(move)
          continue

    return valid_moves

  def is_at_start_y(self, piece, pos):
    if isinstance(piece, Pawn) and piece.is_white == self.is_white:
      if piece.is_white and pos.y == 6:
        return True
      if piece.is_black and pos.y == 1:
        return True
    return False