from src import GameState
from src import get_child_state, get_best_child_state, is_valid_position
from src import minimax 
import random

BOARD_WIDTH = 18
BOARD_HEIGHT = 9   
OBSTACLES = [(1,1),(1,2),(1,3),(1,5),(1,6),(1,7),(2,1),(2,7),(3,3),(3,5),(4,0),(4,1),(4,3),(4,5),(4,7),(4,8),
                (6,1),(6,3),(6,4),(6,5),(6,7),(7,1),(7,3),(7,5),(7,7),(8,1),(8,3),(8,7),(9,1),(9,3),(9,7),(10,1),
                (10,3),(10,5),(10,7),(11,1),(11,3),(11,4),(11,5),(11,7),(13,0),(13,1),(13,3),(13,5),(13,7),(13,8),
                (14,3),(14,5),(15,1),(15,7),(16,1),(16,2),(16,3),(16,5),(16,6),(16,7)] # These can be adjusted
PACMAN_START = (0, 0)
GHOSTS_START = [(8,8), (4,4)]
MOVES = { 'S':(0,0),'U': (0, 1), 'R': (1, 0), 'L': (-1, 0),'D': (0, -1)}
MAX_DEPTH = 9
PACMAN_MOVES = []


def play_game():
    points = {(row, col) for row in range(BOARD_WIDTH) for col in range(BOARD_HEIGHT) if (row, col) not in OBSTACLES}
    state = GameState(PACMAN_START, GHOSTS_START, points, 0, MOVES, OBSTACLES, BOARD_WIDTH, BOARD_HEIGHT, PACMAN_MOVES)
    while not state.is_terminal():
        best_move = None
        best_eval = float("-inf")
        moves = [(0,0),(1,0),(-1,0),(0,1),(0,-1)]
        for move in moves:
            if is_valid_position((state.pacman[0] + move[0], state.pacman[1] + move[1]), BOARD_WIDTH, BOARD_HEIGHT, OBSTACLES):
                if len(PACMAN_MOVES)>3 :
                    if not( (state.pacman[0] + move[0], state.pacman[1] + move[1]) == PACMAN_MOVES[len(PACMAN_MOVES)-2] and PACMAN_MOVES[len(PACMAN_MOVES)-1] == PACMAN_MOVES[len(PACMAN_MOVES)-3]) and not ((state.pacman[0] + move[0], state.pacman[1] + move[1]) == PACMAN_MOVES[len(PACMAN_MOVES)-1] and PACMAN_MOVES[len(PACMAN_MOVES)-1] == PACMAN_MOVES[len(PACMAN_MOVES)-2]):
                        child = get_child_state(state, move, True)
                        eval = minimax(child, MAX_DEPTH-1, 1)
                        if eval >= best_eval:
                            best_eval = eval
                            best_move = move
                else:
                    child = get_child_state(state, move, True)
                    eval = minimax(child, MAX_DEPTH-1, 1)
                    if eval >= best_eval:
                        best_eval = eval
                        best_move = move

        state = get_best_child_state(state, best_move)

        PACMAN_MOVES.append(state.pacman)

        print(f"Pacman is at {state.pacman}, Score: {state.score}")
        for i, _ in enumerate(state.ghosts):
            random_move = random.choice(list(MOVES.values()))
            state = get_child_state(state, random_move, False, i)
            print(f"Ghost {i+1} is at {state.ghosts[i]}")
        map=""
        for i in reversed(range(0,9)):
            for j in range(0,18):
                if (j,i) in OBSTACLES:
                    map = map + "#"

                elif (j,i) == state.pacman:
                    map = map + "p"

                elif (j,i) == state.ghosts[0]:
                    map = map + "g"

                elif (j,i) == state.ghosts[1]:
                    map = map + "s"

                elif (j,i) in state.points:
                    map = map + "."

                else:
                    map = map + " "
                map=map+" "
            map = map +"\n"

        print(map)
        # print(state.score)
        if not state.points:
            print("Pacman wins!")
            break
        elif state.pacman in state.ghosts:
            print("Pacman is caught by a ghost!")
            break

play_game()