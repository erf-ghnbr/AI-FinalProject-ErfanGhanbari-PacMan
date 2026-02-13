from src import GameState

def manhattan_distance(pos1, pos2):
    """Calculate Manhattan distance between two positions."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def find_nearest_food(game_state):
    """Find the nearest food to Pacman using Manhattan distance."""
    if not game_state.points:
        return None
    nearest_food = min(game_state.points, key=lambda food: manhattan_distance(game_state.pacman, food))
    return nearest_food


def find_nearest_ghost_distance(game_state):
    """Find the minimum distance to any ghost."""
    if not game_state.ghosts:
        return float('inf')
    min_distance = min(manhattan_distance(game_state.pacman, ghost) for ghost in game_state.ghosts)
    return min_distance


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
        # Better scoring: 200 for food, -5 for normal movement
        food_bonus = 200 if new_position in state.points else -5
        return GameState(new_position,state.ghosts,
                            points, state.score + food_bonus,
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
    
    # Better scoring: 200 for food (good), -5 for moving without food (minimal penalty to encourage movement)
    food_bonus = 200 if new_position in state.points else -5
    points = state.points - {new_position} if new_position in state.points else state.points
    
    return GameState(new_position, state.ghosts, points, state.score + food_bonus,
                     state.MOVES, state.OBSTACLES, state.BOARD_WIDTH, state.BOARD_HEIGHT, state.PACMAN_MOVES
                    )


def is_valid_position(position, BOARD_WIDTH, BOARD_HEIGHT, OBSTACLES):
    row, col = position
    return 0 <= row < BOARD_WIDTH and 0 <= col < BOARD_HEIGHT and position not in OBSTACLES


def get_reachable_positions(state, ghost_index, depth):
    """Get all positions reachable by a ghost within 'depth' moves."""
    reachable = set()
    queue = [(state.ghosts[ghost_index], 0)]
    visited = {state.ghosts[ghost_index]}
    
    while queue:
        pos, d = queue.pop(0)
        if d < depth:
            for move in state.MOVES.values():
                new_pos = (pos[0] + move[0], pos[1] + move[1])
                if is_valid_position(new_pos, state.BOARD_WIDTH, state.BOARD_HEIGHT, state.OBSTACLES) and new_pos not in visited:
                    visited.add(new_pos)
                    reachable.add(new_pos)
                    queue.append((new_pos, d + 1))
    
    return reachable


def get_best_ghost_move(state, ghost_index, MAX_DEPTH):
    """Find the best move for a ghost using minimax algorithm with cooperation."""
    best_move = None
    best_eval = float("inf")  # Ghosts minimize (want lower utility)
    valid_moves = []
    
    # Get all valid moves first
    for move in state.MOVES.values():
        ghost_pos = state.ghosts[ghost_index]
        new_pos = (ghost_pos[0] + move[0], ghost_pos[1] + move[1])
        if is_valid_position(new_pos, state.BOARD_WIDTH, state.BOARD_HEIGHT, state.OBSTACLES):
            valid_moves.append(move)
    
    # If no valid moves found, try to stay in place
    if not valid_moves:
        return (0, 0)
    
    # Evaluate each valid move using minimax
    move_evaluations = []
    for move in valid_moves:
        child = get_child_state(state, move, False, ghost_index)
        from src import minimax
        # Determine the next agent in the turn sequence
        next_agent = 2 if ghost_index == 0 else 0  # After ghost 0 comes ghost 1, after ghost 1 comes pacman
        eval_score = minimax(child, MAX_DEPTH - 1, next_agent)
        move_evaluations.append((move, eval_score))
        
        if eval_score < best_eval:  # Changed to < instead of <= to avoid ties
            best_eval = eval_score
            best_move = move
    
    # If no move was selected (shouldn't happen), pick closest to Pacman
    if best_move is None:
        best_move = min(valid_moves, 
                       key=lambda m: manhattan_distance(
                           (state.ghosts[ghost_index][0] + m[0], state.ghosts[ghost_index][1] + m[1]),
                           state.pacman
                       ))
    
    return best_move if best_move is not None else (0, 0)