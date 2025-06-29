from chessboard import Chessboard
from display import Display
from engine import StuckFishV1
from position import ChessPos

if __name__ == '__main__':
  board = Chessboard()
  board.reset()

  pawn1_pos = ChessPos("D", 2)
  pawn1_newpos = ChessPos("D", 8)
  board.move(pawn1_pos, pawn1_newpos)
  #
  pawn2_pos = ChessPos("E", 7)
  pawn2_newpos = ChessPos("D", 3)
  board.move(pawn2_pos, pawn2_newpos)

  pawn3_pos = ChessPos("C", 7)
  pawn3_newpos = ChessPos("C", 3)
  board.move(pawn3_pos, pawn3_newpos)

  pawn4_pos = ChessPos("A", 2)
  pawn4_newpos = ChessPos("A", 6)
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

  engine = StuckFishV1(board, True)
  moves = engine.get_available_moves(engine.is_white)
  moves_enemy = engine.get_available_moves(not engine.is_white)

  display = Display()
  display.draw(board)
  display.draw_moves(moves, "blue")
  display.draw_moves(moves_enemy, "red")


  display.display()
