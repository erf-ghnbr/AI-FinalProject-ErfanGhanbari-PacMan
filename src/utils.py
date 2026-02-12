from src import GameState

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


def is_pacman_stuck(state):
    pass