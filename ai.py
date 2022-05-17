import piece
import numpy as np


def get_best_move(state, depth, is_max_state):
    values = state.values
    best_value = is_max_state and -9999 or 9999
    best_move = (-1, -1)
    pieces = len(values[values != piece.EMPTY])

    if pieces == 0:
        return ([7,7], 1)
    if pieces == 2:
        return second_move(state)

    top_moves = get_top_moves(state, 10, is_max_state)

    for move_n_value in top_moves:
        move = move_n_value[0]
        value = minimax(state.next(move),
                        -10e5,
                        10e5,
                        depth - 1,
                        not is_max_state)

        if ((is_max_state and value > best_value)
                or (not is_max_state and value < best_value)):
            best_value = value
            best_move = move
            # print(best_move, best_value)

    if best_move[0] == -1 and best_move[1] == -1:
        return top_moves[0]

    return best_move


def get_top_moves(state, n, is_max_state):
    color = state.color
    top_moves = []

    for move in state.legal_moves():
        evaluation = evaluation_state(state.next(move), color)
        top_moves.append((move, evaluation))
    return sorted(top_moves, key=lambda x: x[1], reverse=is_max_state)[:n]


def minimax(state, alpha, beta, depth, is_max_state):
    if depth == 0 or state.is_terminal():
        return evaluation_state(state, -state.color)

    if is_max_state:
        value = -9999
        for move in state.legal_moves():
            value = max(
                value,
                minimax(state.next(move), alpha, beta, depth - 1, False)
            )
            alpha = max(value, alpha)
            if alpha >= beta:
                break
        return value
    else:
        value = 9999
        for move in state.legal_moves():
            value = min(
                value,
                minimax(state.next(move), alpha, beta, depth - 1, True)
            )
            beta = min(value, beta)
            if alpha >= beta:
                break
        return value


def first_move(state):
    x = state.size // 2
    return np.random.choice((x - 1, x, x + 1), 2), 1


def second_move(state):
    #The corners of the 7x7 square around H8
    secondpos = ((4,4), (4,11), (11,4), (11,11))
    return secondpos[np.random.randint(0,4)], 2

#Evaluation function
def evaluation_state(state, current_color):
    return evaluate_color(state, piece.BLACK, current_color) + \
        evaluate_color(state, piece.WHITE, current_color)


def evaluate_color(state, color, current_color):
    values = state.values
    size = state.size
    current = color == current_color
    evaluation = 0

    # evaluate rows and cols
    for i in range(size):
        evaluation += evaluate_line(values[i, :], color, current)
        evaluation += evaluate_line(values[:, i], color, current)

    # evaluate diags (by turning it into a line)
    for i in range(-size + 5, size - 4):
        evaluation += evaluate_line(np.diag(values, k=i),
                                    color,
                                    current)
        evaluation += evaluate_line(np.diag(np.fliplr(values), k=i),
                                    color,
                                    current)

    return evaluation * color


def evaluate_line(line, color, current):
    evaluation = 0
    size = len(line)
    # consecutive
    consec = 0
    #a block is a group of pieces
    block_count = 2
    empty = False

    for i in range(len(line)):
        value = line[i]
        if value == color:
            consec += 1
        elif value == piece.EMPTY and consec > 0:
            if not empty and i < size - 1 and line[i + 1] == color:
                empty = True
            else:
                evaluation += calc(consec, block_count - 1, current, empty)
                consec = 0
                block_count = 1
                empty = False
        elif value == piece.EMPTY:
            block_count = 1
        elif consec > 0:
            evaluation += calc(consec, block_count, current)
            consec = 0
            block_count = 2
        else:
            block_count = 2

    if consec > 0:
        evaluation += calc(consec, block_count, current)

    return evaluation


def calc(consec, block_count, is_current, has_empty_space=False):
    if block_count == 2 and consec < 5:
        return 0

    if consec >= 5:
        if has_empty_space:
            return 8000
        return 100000

    consec_score = (2, 5, 1000, 10000)
    block_count_score = (0.5, 0.6, 0.01, 0.25)
    not_current_score = (1, 1, 0.2, 0.15)
    empty_space_score = (1, 1.2, 0.9, 0.4)

    consec_idx = consec - 1
    value = consec_score[consec_idx]
    if block_count == 1:
        value *= block_count_score[consec_idx]
    if not is_current:
        value *= not_current_score[consec_idx]
    if has_empty_space:
        value *= empty_space_score[consec_idx]
    return int(value)
