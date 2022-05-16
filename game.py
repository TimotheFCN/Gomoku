import time
import piece
import numpy as np
from board import BoardState
from ai import get_best_move


class GameRunner:
    def __init__(self, size=15, depth=2):
        self.size = size
        self.depth = depth
        self.finished = False
        self.total_time = 0
        self.restart()

    def restart(self, player_index=1):
        self.is_max_state = True if player_index == -1 else False
        self.state = BoardState(self.size)
        self.ai_color = -player_index

    def play(self, j, i):
        position = (i-1, j-1)
        if self.state.color != self.ai_color:
            return False
        if not self.state.is_valid_position(position):
            return False
        self.state = self.state.next(position)
        self.finished = self.state.is_terminal()
        return True

    def aiplay(self):
        t = time.time()
        if self.state.color == self.ai_color:
            return False, (0, 0)
        move, value = get_best_move(self.state, self.depth, self.is_max_state)
        self.state = self.state.next(move)
        self.finished = self.state.is_terminal()
        self.total_time += time.time() - t
        print("Temps de reflexion: " + str(time.time() - t))
        return True, move