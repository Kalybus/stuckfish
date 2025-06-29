from piece import Piece, Pawn, Slot, Empty, Rook, Bishop, Knight, Queen, King
from position import Pos


class Engine:
  def __init__(self, board, is_white):
    self.board = board
    self.is_white = is_white

  def get_available_moves(self, color):
    raise NotImplementedError()

  def next_move(self):
    raise NotImplementedError()


class StuckFishV1(Engine):
  def get_available_moves(self, color):
    moves = {}
    enemy_moves = {}

    for row in range(8):
      for col in range(8):
        pos = Pos(col, row)
        piece = self.board.get_slot(pos)
        if isinstance(piece, Piece) and piece.is_white == color:
          moves[pos] = self.get_piece_moves(piece, pos, color)

        if isinstance(piece, Piece) and piece.opposite_color == color:
          enemy_moves[pos] = self.get_piece_moves(piece, pos, not color)

    moves = self.remove_checks(moves, enemy_moves, color)
    for pos, pos_moves in moves.items():
      piece = self.board.get_slot(pos)
      print(f"{piece} at {pos} can be moved to {pos_moves}")
    print('End of analysis\n')

    return moves

  def remove_checks(self, moves, enemy_moves, color):
    king = None
    king_pos = None
    for pos in moves:
      piece = self.board.get_slot(pos)
      if isinstance(piece, King) and piece.is_white == color:
        king = piece
        king_pos = pos
        break
    if king is None:
      raise Exception("No king")

    for enemy_pos, enemy_piece_moves in enemy_moves.items():
      for enemy_piece_move in enemy_piece_moves:
        if enemy_piece_move == king_pos:
          print("King is checked")
          moves = {king_pos: moves[king_pos]}

        if enemy_piece_move in moves[king_pos]:
          print(f"King will be checked at {enemy_piece_move}")
          moves[king_pos].remove(enemy_piece_move)

    return moves

  def get_piece_moves(self, piece, pos, color):
    valid_moves = []
    if isinstance(piece, Pawn) or isinstance(piece, Queen):
      valid_moves += self.get_pawn_moves(piece, pos, color)

    if isinstance(piece, Rook) or isinstance(piece, Queen):
      valid_moves += self.get_rook_moves(piece, pos, color)

    if isinstance(piece, Bishop) or isinstance(piece, Queen):
      valid_moves += self.get_bishop_moves(piece, pos, color)

    if isinstance(piece, Knight):
      valid_moves += self.get_knight_moves(piece, pos, color)

    if isinstance(piece, King) or isinstance(piece, Queen):
      valid_moves += self.get_king_moves(piece, pos, color)

    return valid_moves

  def get_pawn_moves(self, piece, pos, color):
    valid_moves = []
    # General case
    move_one = piece.move(pos, 0, 1)
    move_one_slot = self.board.get_slot(move_one)
    if isinstance(move_one_slot, Empty):
      valid_moves.append(move_one)

    # Start case
    move_two = piece.move(pos, 0, 2)
    move_two_slot = self.board.get_slot(move_two)
    if self.is_at_start_y(piece, pos, color) and isinstance(move_one_slot, Empty) and isinstance(move_two_slot, Empty):
      valid_moves.append(move_two)

    # Attack case
    for enemy_pos in [piece.move(pos, 1, 1), piece.move(pos, -1, 1)]:
      enemy = self.board.get_piece(enemy_pos)
      if isinstance(enemy, Piece) and enemy.opposite_color == color:
        valid_moves.append(enemy_pos)
    # TODO Implement en-passant
    return valid_moves

  def get_rook_moves(self, piece, pos, color):
    valid_moves = []
    for i in range(1, 8):
      move_one = piece.move(pos, 0, i)
      move_one_slot = self.board.get_slot(move_one)
      if isinstance(move_one_slot, Empty):
        valid_moves.append(move_one)
        continue
      if isinstance(move_one_slot, Piece) and move_one_slot.opposite_color == color:
        valid_moves.append(move_one)
      break
    return valid_moves

  def get_bishop_moves(self, piece, pos, color):
    valid_moves = []
    # Left diagonal
    for i in range(1, 8):
      move_diag = piece.move(pos, i, i)
      move_diag_slot = self.board.get_slot(move_diag)
      if isinstance(move_diag_slot, Empty):
        valid_moves.append(move_diag)
        continue
      if isinstance(move_diag_slot, Piece) and move_diag_slot.opposite_color == color:
        valid_moves.append(move_diag)
      break

    # Right diagonal
    for i in range(1, 8):
      move_diag = piece.move(pos, -i, i)
      move_diag_slot = self.board.get_slot(move_diag)
      if isinstance(move_diag_slot, Empty):
        valid_moves.append(move_diag)
        continue
      if isinstance(move_diag_slot, Piece) and move_diag_slot.opposite_color == color:
        valid_moves.append(move_diag)
      break
    return valid_moves

  def get_knight_moves(self, piece, pos, color):
    valid_moves = []
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
      if isinstance(move_slot, Piece) and move_slot.opposite_color == color:
        valid_moves.append(move)
        continue
    return valid_moves

  def get_king_moves(self, piece, pos, color):
    valid_moves = []
    moves = [
      piece.move(pos, 1, 0),
      piece.move(pos, 0, 1),
      piece.move(pos, -1, 0),
      piece.move(pos, 0, -1),
      piece.move(pos, 1, 1),
      piece.move(pos, -1, 1),
      piece.move(pos, -1, -1),
      piece.move(pos, 1, -1),
    ]
    for move in moves:
      move_slot = self.board.get_slot(move)
      if isinstance(move_slot, Empty):
        valid_moves.append(move)
        continue
      if isinstance(move_slot, Piece) and move_slot.opposite_color == color:
        valid_moves.append(move)
        continue
    return valid_moves

  def is_at_start_y(self, piece, pos, color):
    if isinstance(piece, Pawn) and piece.is_white == color:
      if piece.is_white and pos.y == 6:
        return True
      if piece.is_black and pos.y == 1:
        return True
    return False