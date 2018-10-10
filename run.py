from gui import Chessboard
import threading

def make_chessboard(coords=()):
    chessboard = Chessboard((8, 8), 4)
    chessboard.draw_queens(coords, 0)
    chessboard.draw_queens(coords, 1)
    chessboard.draw_queens(coords, 2)
    chessboard.draw_queens(coords, 3)
    chessboard.start()

arg = []
for i in range(8):
    for j in range(8):
        arg.append((i,j))

gui = threading.Thread(target=make_chessboard, args=[arg])
gui.start()


