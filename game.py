from display import Display
from chessboard import Chessboard
from position import ChessPos

WHITE = True
BLACK = False

class Game:
  def __init__(self):
    self.color = WHITE # White starts
    self.current_board = Chessboard(WHITE)
    self.current_board.init()

  def play(self):
    user_input = []
    pos = None
    next_pos = None
    while not (len(user_input) == 2 and ChessPos.is_pos(user_input[0]) and ChessPos.is_pos(user_input[1])):
      user_input = input(f"{self.print_color()} enters move (eg: E2,E3): ").strip().lower().split(",")
      pos = ChessPos(user_input[0])
      next_pos = ChessPos(user_input[1])
    self.current_board.move(pos, next_pos)
    self.color = not self.color
    next_board = Chessboard(self.color, self.current_board.data)
    self.current_board = next_board

  def display(self):
    display = Display()
    display.draw(self.current_board)
    display.draw_moves(self.current_board.moves, "blue")
    display.draw_moves(self.current_board.enemy_moves, "red")
    display.display()

    # display = Display()
    # display.draw(board)
    # # display.draw_moves(board.moves, "blue")
    # # display.draw_moves(board.enemy_moves, "red")
    # display.display()

  def print_color(self):
    return 'White' if self.color else 'Black'

  # def is_pos(self, user_input):
  #   return len(user_input) == 2 and user_input[0] in "abcdefgh" and user_input[1] in "12345678"