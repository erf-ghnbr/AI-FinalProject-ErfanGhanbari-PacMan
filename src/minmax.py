from src import get_child_state, is_valid_position

def minimax(state, depth, agent):
    if depth == 0 or state.is_terminal():
        return state.utility()
    if agent==0:
        max_eval = float("-inf")
        for move in state.MOVES.values():
            if is_valid_position((state.pacman[0] + move[0], state.pacman[1] + move[1]), state.BOARD_WIDTH, state.BOARD_HEIGHT, state.OBSTACLES):
                child = get_child_state(state, move, True)
                eval = minimax(child, depth-1, 1)
                max_eval = max(max_eval, eval)
        return max_eval
    elif agent ==1:
        min_eval = float("inf")
        for move in state.MOVES.values():
            if is_valid_position((state.ghosts[0][0] + move[0], state.ghosts[0][1] + move[1]), state.BOARD_WIDTH, state.BOARD_HEIGHT, state.OBSTACLES):
                child = get_child_state(state, move, False, 0)
                eval = minimax(child, depth-1, 2)
                min_eval = min(min_eval, eval)
        return min_eval
    elif agent ==2:
        min_eval = float("inf")
        for move in state.MOVES.values():
            if is_valid_position((state.ghosts[1][0] + move[0], state.ghosts[1][1] + move[1]), state.BOARD_WIDTH, state.BOARD_HEIGHT, state.OBSTACLES):
                child = get_child_state(state, move, False, 1)
                eval = minimax(child, depth-1, 0)
                min_eval = min(min_eval, eval)
        return min_eval
