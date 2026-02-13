class GameState:
    def __init__(self, pacman, ghosts, points, score, MOVES, OBSTACLES, BOARD_WIDTH, BOARD_HEIGHT, PACMAN_MOVES):
        self.pacman = pacman
        self.ghosts = ghosts
        self.points = points
        self.score = score
        self.MOVES = MOVES
        self.OBSTACLES = OBSTACLES
        self.BOARD_WIDTH = BOARD_WIDTH
        self.BOARD_HEIGHT = BOARD_HEIGHT
        self.PACMAN_MOVES = PACMAN_MOVES
        

    def is_terminal(self):
        return not self.points or any(ghost == self.pacman for ghost in self.ghosts)

    def utility(self):

        if self.is_terminal():
            if self.pacman in self.ghosts:
                return float("-inf")
            else:
                return float("inf")
        else:
            distance1 = abs(self.pacman[0]-self.ghosts[0][0]) +abs(self.pacman[1]-self.ghosts[0][1])
            distance2 = abs(self.pacman[0]-self.ghosts[1][0]) +abs(self.pacman[1]-self.ghosts[1][1])

            k=0
            if min(distance1, distance2) > 3:
                k=100
            elif min(distance1, distance2)< 2:
                k=-1000
            else:
                k =-100

            l=0
            if len(self.PACMAN_MOVES) > 0:
                from src import bfs_for_food
                shortest_path_to_food = bfs_for_food(self, self.PACMAN_MOVES[-1], self.MOVES, self.OBSTACLES, self.BOARD_WIDTH, self.BOARD_HEIGHT)
                if self.pacman in shortest_path_to_food:
                    i=0
                    for pos in shortest_path_to_food:
                        if self.pacman == pos:
                            break
                        i += 1
                    l = i * 150
                else:
                    l=-100

            return self.score + k  + l

    def utility_ghost(self, ghost_i):
        if self.is_terminal():
            if self.pacman in self.ghosts:
                return float("inf")
            else:
                return float("-inf")
        else:

            l=0
            from src import bfs_to_pacman
            shortest_path_to_pacman = bfs_to_pacman(self, self.ghosts[ghost_i], self.MOVES, self.OBSTACLES, self.BOARD_WIDTH, self.BOARD_HEIGHT)
            if shortest_path_to_pacman and self.ghosts[ghost_i] in shortest_path_to_pacman:
                i=0
                for pos in shortest_path_to_pacman:
                    if self.ghosts[ghost_i] == pos:
                        break
                    i += 1
                l = i * -150
            else:
                l=100

            return l