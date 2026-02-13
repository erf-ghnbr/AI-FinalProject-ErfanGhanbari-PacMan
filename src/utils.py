from src import GameState

def bfs_for_food(game_state, start, MOVES, OBSTACLES, BOARD_WIDTH, BOARD_HEIGHT):
    explored = []
    queue = [[start]]

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node not in explored:
            for move in MOVES.values():
                new_pos = (node[0]+move[0],node[1]+move[1])
                if (move !=(0,0)) and (new_pos not in explored) and (new_pos not in OBSTACLES) and (0 <= new_pos[0] < BOARD_WIDTH and 0 <= new_pos[1] < BOARD_HEIGHT):
                    new_path = list(path)
                    new_path.append(new_pos)
                    queue.append(new_path)

                if new_pos in game_state.points:
                    return new_path
            explored.append(node)


def bfs_to_pacman(game_state, start, MOVES, OBSTACLES, BOARD_WIDTH, BOARD_HEIGHT):
    explored = []
    queue = [[start]]

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node not in explored:
            for move in MOVES.values():
                new_pos = (node[0]+move[0],node[1]+move[1])
                if (move !=(0,0)) and (new_pos not in explored) and (new_pos not in OBSTACLES) and (0 <= new_pos[0] < BOARD_WIDTH and 0 <= new_pos[1] < BOARD_HEIGHT):
                    new_path = list(path)
                    new_path.append(new_pos)
                    queue.append(new_path)

                if new_pos == game_state.pacman:
                    return new_path
            explored.append(node)


def get_child_state(state, move, is_pacman, ghost_index=None):
    if is_pacman:
        new_position = (state.pacman[0] + move[0], state.pacman[1] + move[1])
        if new_position in state.OBSTACLES or not is_valid_position(new_position, state.BOARD_WIDTH, state.BOARD_HEIGHT, state.OBSTACLES):
            new_position = state.pacman
        points = state.points - {new_position} if new_position in state.points else state.points
        return GameState(new_position,state.ghosts,
                            points, state.score + (200 if new_position in state.points else -10),
                            state.MOVES, state.OBSTACLES, state.BOARD_WIDTH, state.BOARD_HEIGHT, state.PACMAN_MOVES
                        )
    else:
        new_ghosts = list(state.ghosts)
        new_position = (state.ghosts[ghost_index][0] + move[0], state.ghosts[ghost_index][1] + move[1])
        if new_position in state.OBSTACLES or not is_valid_position(new_position, state.BOARD_WIDTH, state.BOARD_HEIGHT, state.OBSTACLES):
            new_position = state.ghosts[ghost_index]
        new_ghosts[ghost_index] = new_position
        return GameState(state.pacman, tuple(new_ghosts), state.points, state.score,
                         state.MOVES, state.OBSTACLES, state.BOARD_WIDTH, state.BOARD_HEIGHT, state.PACMAN_MOVES
                        )


def get_best_child_state(state, move):
    new_position = (state.pacman[0] + move[0], state.pacman[1] + move[1])
    if new_position in state.OBSTACLES or not is_valid_position(new_position, state.BOARD_WIDTH, state.BOARD_HEIGHT, state.OBSTACLES):
        new_position = state.pacman
    points = state.points - {new_position} if new_position in state.points else state.points
    return GameState(new_position, state.ghosts, points, state.score + (10 if new_position in state.points else -1),
                     state.MOVES, state.OBSTACLES, state.BOARD_WIDTH, state.BOARD_HEIGHT, state.PACMAN_MOVES
                    )


def is_valid_position(position, BOARD_WIDTH, BOARD_HEIGHT, OBSTACLES):
    row, col = position
    return 0 <= row < BOARD_WIDTH and 0 <= col < BOARD_HEIGHT and position not in OBSTACLES


def get_best_ghost_move(state, ghost_index, MAX_DEPTH):
    """Find the best move for a ghost using minimax algorithm."""
    best_move = None
    best_eval = float("inf")  # Ghosts minimize
    
    for move in state.MOVES.values():
        ghost_pos = state.ghosts[ghost_index]
        new_pos = (ghost_pos[0] + move[0], ghost_pos[1] + move[1])
        if is_valid_position(new_pos, state.BOARD_WIDTH, state.BOARD_HEIGHT, state.OBSTACLES):
            child = get_child_state(state, move, False, ghost_index)
            from src import minimax
            # Determine the next agent based on which ghost we're moving
            next_agent = 2 if ghost_index == 0 else 0  # After ghost 0 comes ghost 1, after ghost 1 comes pacman
            eval = minimax(child, MAX_DEPTH - 1, next_agent)
            if eval <= best_eval:
                best_eval = eval
                best_move = move
    
    return best_move if best_move is not None else (0, 0)