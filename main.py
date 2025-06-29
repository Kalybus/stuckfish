import copy
from operator import truediv

from chessboard import Chessboard
from display import Display
from engine import StuckFishV1, Engine
from position import ChessPos

WHITE = True
BLACK = False

if __name__ == '__main__':
  board = Chessboard(WHITE)
  board.init()

  pawn1_pos = ChessPos("D", 2)
  pawn1_newpos = ChessPos("D", 8)
  board.move(pawn1_pos, pawn1_newpos)
  #
  pawn2_pos = ChessPos("C", 8)
  pawn2_newpos = ChessPos("C", 3)
  board.move(pawn2_pos, pawn2_newpos)

  pawn3_pos = ChessPos("C", 7)
  pawn3_newpos = ChessPos("B", 3)
  board.move(pawn3_pos, pawn3_newpos)

  pawn4_pos = ChessPos("A", 2)
  pawn4_newpos = ChessPos("B", 5)
  board.move(pawn4_pos, pawn4_newpos)

  pawn5_pos = ChessPos("G", 7)
  pawn5_newpos = ChessPos("G", 5)
  board.move(pawn5_pos, pawn5_newpos)

  pawn6_pos = ChessPos("F", 2)
  pawn6_newpos = ChessPos("F", 5)
  board.move(pawn6_pos, pawn6_newpos)

  pawn6_pos = ChessPos("F", 8)
  pawn6_newpos = ChessPos("F", 4)
  board.move(pawn6_pos, pawn6_newpos)

  pawn7_pos = ChessPos("F", 1)
  pawn7_newpos = ChessPos("C", 4)
  board.move(pawn7_pos, pawn7_newpos)

  # pawn8_pos = ChessPos("C", 1)
  # pawn8_newpos = ChessPos("D", 2)
  # board.move(pawn8_pos, pawn8_newpos)

  # engine = StuckFishV1(True)
  # moves = engine.get_available_moves(board, engine.is_white)
  # moves_enemy = engine.get_available_moves(board, not engine.is_white)

  board.print_moves()

  display = Display()
  # display.draw(board)

  # display = Display()
  display.draw(board)
  display.draw_moves(board.moves, "blue")
  display.draw_moves(board.enemy_moves, "red")

  display.display()
  #
  # display.reset()
  # new_board = copy.deepcopy(board)
  # pawn8_pos = ChessPos("B", 2)
  # pawn8_newpos = ChessPos("B", 3)
  # new_board.move(pawn8_pos, pawn8_newpos)
  #
  # display.draw(new_board)
  # display.display()


