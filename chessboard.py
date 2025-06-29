import copy
import uuid

from piece import Slot, Rook, Knight, Bishop, Queen, King, Pawn, Piece, Empty
from position import Pos


class Chessboard:
  def __init__(self, color, data=[], ignore_checks=False):
    self.data = data
    self.color = color
    self.ignore_checks = ignore_checks
    self.uuid = uuid.uuid4()

    # Analysed data
    self.__king_pos = None
    self.__moves = None
    self.__enemy_moves = None
    self.__checkers = []

  def reset(self):
    self.__king_pos = None
    self.__moves = None
    self.__enemy_moves = None
    self.__checkers = []

  def analyse_board(self):
    print(f"Analysing chessboard {self.uuid}")
    self.__moves = {}
    self.__enemy_moves = {}
    # Get available moves
    for row in range(8):
      for col in range(8):
        pos = Pos(col, row)
        piece = self.get_slot(pos)
        if isinstance(piece, Piece) and piece.is_white == self.color:
          self.__moves[pos] = self.get_piece_moves(self.color, piece, pos)
        if isinstance(piece, Piece) and piece.opposite_color == self.color:
          self.__enemy_moves[pos] = self.get_piece_moves(not self.color, piece, pos)
        if isinstance(piece, King) and piece.color == self.color:
          self.__king_pos = pos

    # Must crash if no king is found
    assert(self.king_pos is not None)

    if not self.ignore_checks:
      # Remove check moves
      for enemy_pos, enemy_piece_moves in self.__enemy_moves.items():
        for enemy_piece_move in enemy_piece_moves:
          # Remove moves where the king is will checked
          if enemy_piece_move in self.__moves[self.king_pos]:
            print(f"{enemy_pos} to {enemy_piece_move} will be checking your king")
            self.__moves[self.king_pos].remove(enemy_piece_move)
          # Get pieces that check the king
          if enemy_piece_move == self.king_pos:
            print(f"{enemy_pos} to {enemy_piece_move} is checking your king")
            self.__checkers.append(enemy_pos)

      # Find moves to prevent a check
      if self.__checkers:
        safes_moves = {}
        for checker_pos in self.__checkers:
          checker_piece = self.get_piece(checker_pos)
          for piece_pos, piece_moves in self.__moves.items():
            # Your king's move are always safe. Unsafe moves already removed by previous step
            if piece_pos == self.king_pos:
              safes_moves[self.king_pos] = piece_moves
              continue
            # Verify your other pieces
            piece_next_poses = []
            for piece_next_pos in piece_moves:
              next_board = Chessboard(self.color, copy.deepcopy(self.data))
              next_board.move(piece_pos, piece_next_pos)
              next_board.ignore_checks = True # Disable check verification to avoid recursion
              if not next_board.__is_checker(checker_piece, checker_pos):
                print(f"{piece_pos} to {piece_next_pos} protects from {checker_pos} to {self.king_pos} ")
                piece_next_poses.append(piece_next_pos)
            safes_moves[piece_pos] = piece_next_poses
        self.__moves = safes_moves
    print(f'End of analysis of {self.uuid}\n')

  @property
  def moves(self):
    if not self.__moves:
      self.analyse_board()
    return self.__moves

  @property
  def enemy_moves(self):
    if not self.__enemy_moves:
      self.analyse_board()
    return self.__enemy_moves

  @property
  def king_pos(self):
    if not self.__king_pos:
      self.analyse_board()
    return self.__king_pos

  def init(self):
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

  # Chess Engine rules
  def get_piece_moves(self, color, piece, pos):
    valid_moves = []
    if isinstance(piece, Pawn) or isinstance(piece, Queen):
      valid_moves += self.get_pawn_moves(color, piece, pos)

    if isinstance(piece, Rook) or isinstance(piece, Queen):
      valid_moves += self.get_rook_moves(color, piece, pos)

    if isinstance(piece, Bishop) or isinstance(piece, Queen):
      valid_moves += self.get_bishop_moves(color, piece, pos)

    if isinstance(piece, Knight):
      valid_moves += self.get_knight_moves(color, piece, pos)

    if isinstance(piece, King) or isinstance(piece, Queen):
      valid_moves += self.get_king_moves(color, piece, pos)

    return set(valid_moves)

  def get_pawn_moves(self, color, piece, pos):
    valid_moves = []
    # General case
    move_one = piece.move(pos, 0, 1)
    move_one_slot = self.get_slot(move_one)
    if isinstance(move_one_slot, Empty):
      valid_moves.append(move_one)

    # Start case
    move_two = piece.move(pos, 0, 2)
    move_two_slot = self.get_slot(move_two)
    if self.__is_pawn_at_start(piece, pos, color) and isinstance(move_one_slot, Empty) and isinstance(
      move_two_slot, Empty):
      valid_moves.append(move_two)

    # Attack case
    for enemy_pos in [piece.move(pos, 1, 1), piece.move(pos, -1, 1)]:
      enemy = self.get_piece(enemy_pos)
      if isinstance(enemy, Piece) and enemy.opposite_color == color:
        valid_moves.append(enemy_pos)
    # TODO Implement en-passant
    return valid_moves

  def get_rook_moves(self, color, piece, pos):
    valid_moves = []
    # Up
    for i in range(1, 8):
      move_one = piece.move(pos, 0, i)
      move_one_slot = self.get_slot(move_one)
      if isinstance(move_one_slot, Empty):
        valid_moves.append(move_one)
        continue
      if isinstance(move_one_slot, Piece) and move_one_slot.opposite_color == color:
        valid_moves.append(move_one)
      break
    # Down
    for i in range(1, 8):
      move_one = piece.move(pos, 0, -i)
      move_one_slot = self.get_slot(move_one)
      if isinstance(move_one_slot, Empty):
        valid_moves.append(move_one)
        continue
      if isinstance(move_one_slot, Piece) and move_one_slot.opposite_color == color:
        valid_moves.append(move_one)
      break
    # Right
    for i in range(1, 8):
      move_one = piece.move(pos, i, 0)
      move_one_slot = self.get_slot(move_one)
      if isinstance(move_one_slot, Empty):
        valid_moves.append(move_one)
        continue
      if isinstance(move_one_slot, Piece) and move_one_slot.opposite_color == color:
        valid_moves.append(move_one)
      break
    # Left
    for i in range(1, 8):
      move_one = piece.move(pos, -i, 0)
      move_one_slot = self.get_slot(move_one)
      if isinstance(move_one_slot, Empty):
        valid_moves.append(move_one)
        continue
      if isinstance(move_one_slot, Piece) and move_one_slot.opposite_color == color:
        valid_moves.append(move_one)
      break

    return valid_moves

  def get_bishop_moves(self, color, piece, pos):
    valid_moves = []
    # Right diagonal
    for i in range(1, 8):
      move_diag = piece.move(pos, i, i)
      move_diag_slot = self.get_slot(move_diag)
      if isinstance(move_diag_slot, Empty):
        valid_moves.append(move_diag)
        continue
      if isinstance(move_diag_slot, Piece) and move_diag_slot.opposite_color == color:
        valid_moves.append(move_diag)
      break

    # Left diagonal
    for i in range(1, 8):
      move_diag = piece.move(pos, -i, i)
      move_diag_slot = self.get_slot(move_diag)
      if isinstance(move_diag_slot, Empty):
        valid_moves.append(move_diag)
        continue
      if isinstance(move_diag_slot, Piece) and move_diag_slot.opposite_color == color:
        valid_moves.append(move_diag)
      break

    # Right reverse diagonal
    for i in range(1, 8):
      move_diag = piece.move(pos, i, -i)
      move_diag_slot = self.get_slot(move_diag)
      if isinstance(move_diag_slot, Empty):
        valid_moves.append(move_diag)
        continue
      if isinstance(move_diag_slot, Piece) and move_diag_slot.opposite_color == color:
        valid_moves.append(move_diag)
      break

    # Left reverse diagonal
    for i in range(1, 8):
      move_diag = piece.move(pos, -i, -i)
      move_diag_slot = self.get_slot(move_diag)
      if isinstance(move_diag_slot, Empty):
        valid_moves.append(move_diag)
        continue
      if isinstance(move_diag_slot, Piece) and move_diag_slot.opposite_color == color:
        valid_moves.append(move_diag)
      break
    return valid_moves

  def get_knight_moves(self, color, piece, pos):
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
      move_slot = self.get_slot(move)
      if isinstance(move_slot, Empty):
        valid_moves.append(move)
        continue
      if isinstance(move_slot, Piece) and move_slot.opposite_color == color:
        valid_moves.append(move)
        continue
    return valid_moves

  def get_king_moves(self, color, piece, pos):
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
      move_slot = self.get_slot(move)
      if isinstance(move_slot, Empty):
        valid_moves.append(move)
        continue
      if isinstance(move_slot, Piece) and move_slot.opposite_color == color:
        valid_moves.append(move)
        continue
    return valid_moves

  def __is_checker(self, checker_piece, checker_pos):
    checker_next_moves = self.get_piece_moves(checker_piece.color, checker_piece, checker_pos)
    for checker_next_pos in checker_next_moves:
      if checker_next_pos == self.king_pos:
        return True
    return False

  def __is_pawn_at_start(self, piece, pos, color):
    if isinstance(piece, Pawn) and piece.is_white == color:
      if piece.is_white and pos.y == 6:
        return True
      if piece.is_black and pos.y == 1:
        return True
    return False

  def print_moves(self):
    for pos, pos_moves in self.moves.items():
      piece = self.get_piece(pos)
      print(f"{piece} at {pos} can be moved to {pos_moves}")