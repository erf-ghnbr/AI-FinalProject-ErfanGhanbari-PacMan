from src import get_child_state, is_valid_position

def minimax(state, depth, agent):
    # Terminal state evaluation
    if state.is_terminal():
        if agent == 0:
            return state.utility()
        else:
            return state.utility_ghost(agent - 1)
    
    # Depth limit reached
    if depth == 0:
        if agent == 0:
            return state.utility()
        else:
            return state.utility_ghost(agent - 1)
    
    if agent == 0:  # Pacman - Maximizer
        max_eval = float("-inf")
        has_valid_move = False
        for move in state.MOVES.values():
            if is_valid_position((state.pacman[0] + move[0], state.pacman[1] + move[1]), state.BOARD_WIDTH, state.BOARD_HEIGHT, state.OBSTACLES):
                has_valid_move = True
                child = get_child_state(state, move, True)
                eval = minimax(child, depth-1, 1)
                max_eval = max(max_eval, eval)
        
        # If no valid moves found, evaluate current state
        if not has_valid_move:
            return state.utility()
        return max_eval
    
    elif agent == 1:  # Ghost 0 - Minimizer
        min_eval = float("inf")
        has_valid_move = False
        for move in state.MOVES.values():
            if is_valid_position((state.ghosts[0][0] + move[0], state.ghosts[0][1] + move[1]), state.BOARD_WIDTH, state.BOARD_HEIGHT, state.OBSTACLES):
                has_valid_move = True
                child = get_child_state(state, move, False, 0)
                eval = minimax(child, depth-1, 2)
                min_eval = min(min_eval, eval)
        
        # If no valid moves found, evaluate current state
        if not has_valid_move:
            return state.utility_ghost(0)
        return min_eval
    
    elif agent == 2:  # Ghost 1 - Minimizer
        min_eval = float("inf")
        has_valid_move = False
        for move in state.MOVES.values():
            if is_valid_position((state.ghosts[1][0] + move[0], state.ghosts[1][1] + move[1]), state.BOARD_WIDTH, state.BOARD_HEIGHT, state.OBSTACLES):
                has_valid_move = True
                child = get_child_state(state, move, False, 1)
                eval = minimax(child, depth-1, 0)
                min_eval = min(min_eval, eval)
        
        # If no valid moves found, evaluate current state
        if not has_valid_move:
            return state.utility_ghost(1)
        return min_eval
