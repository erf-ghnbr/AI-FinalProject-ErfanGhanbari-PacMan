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

    def manhattan_distance(self, pos1, pos2):
        """Calculate Manhattan distance between two positions."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def get_nearest_food_distance(self):
        """Get distance to nearest food."""
        if not self.points:
            return float('inf')
        return min(self.manhattan_distance(self.pacman, food) for food in self.points)

    def get_nearest_ghost_distance(self):
        """Get distance to nearest ghost."""
        explored = []
        queue = [[self.pacman]]

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node not in explored:
                for move in self.MOVES.values():
                    new_pos = (node[0]+move[0],node[1]+move[1])
                    if (move !=(0,0)) and (new_pos not in explored) and (new_pos not in self.OBSTACLES) and (0 <= new_pos[0] < self.BOARD_WIDTH and 0 <= new_pos[1] < self.BOARD_HEIGHT):
                        new_path = list(path)
                        new_path.append(new_pos)
                        queue.append(new_path)

                    if new_pos in self.ghosts:
                        return len(new_path)
                explored.append(node)

    def get_pacman_shortest_distance(self, ghost_i):
        """Get distance to nearest ghost."""
        explored = []
        queue = [[self.ghosts[ghost_i]]]

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node not in explored:
                for move in self.MOVES.values():
                    new_pos = (node[0]+move[0],node[1]+move[1])
                    if (move !=(0,0)) and (new_pos not in explored) and (new_pos not in self.OBSTACLES) and (0 <= new_pos[0] < self.BOARD_WIDTH and 0 <= new_pos[1] < self.BOARD_HEIGHT):
                        new_path = list(path)
                        new_path.append(new_pos)
                        queue.append(new_path)

                    if new_pos == self.pacman:
                        return len(new_path)
                explored.append(node)

    
    def ghost_to_ghost_distance(self, ghost_i, other_ghost_i):
        """Get distance between two ghosts."""
        explored = []
        queue = [[self.ghosts[ghost_i]]]

        while queue:
            path = queue.pop(0)
            node = path[-1]
            new_path = None

            if node not in explored:
                for move in self.MOVES.values():
                    new_pos = (node[0]+move[0],node[1]+move[1])
                    if (move !=(0,0)) and (new_pos not in explored) and (new_pos not in self.OBSTACLES) and (0 <= new_pos[0] < self.BOARD_WIDTH and 0 <= new_pos[1] < self.BOARD_HEIGHT):
                        new_path = list(path)
                        new_path.append(new_pos)
                        queue.append(new_path)

                    if new_pos == self.ghosts[other_ghost_i]:
                        return len(new_path) if new_path is not None else len(path)
                explored.append(node)

    def utility(self):
        """Evaluate state for Pacman (maximizer). Pacman wants to eat food and avoid ghosts."""

        if self.is_terminal():
            if self.pacman in self.ghosts:
                return float("-inf")
            else:
                return float("inf")
        
        total_eval = self.score
        
        # GHOST AVOIDANCE: Strongly penalize being close to ghosts
        ghost_distance = self.get_nearest_ghost_distance()
        if ghost_distance == 0:
            return float("-inf")
        elif ghost_distance == 1:
            total_eval -= 400  # Very dangerous!
        elif ghost_distance == 2:
            total_eval -= 200  # Still very dangerous
        elif ghost_distance <= 3:
            total_eval -= 100  # Caution zone
        elif ghost_distance <= 5:
            total_eval -= 50   # Still be careful
        else:
            total_eval += 30   # Safe distance, small reward
        
        # FOOD ATTRACTION: Strong incentive to eat food
        # if self.points:
        #     food_distance = self.get_nearest_food_distance()
        #     food_reward = 300 - (food_distance * 15)  # Closer food = bigger reward
        #     total_eval += food_reward
            
        #     # Bonus for clearing the board
        #     remaining_points_penalty = (len(self.points) * 25)
        #     total_eval -= remaining_points_penalty

        l=0
        if len(self.PACMAN_MOVES) > 0:
            from src.utils import bfs_for_food
            shortest_path_to_food = bfs_for_food(self, self.PACMAN_MOVES[-1], self.MOVES, self.OBSTACLES, self.BOARD_WIDTH, self.BOARD_HEIGHT)
            if self.pacman in shortest_path_to_food:
                i=0
                for pos in shortest_path_to_food:
                    if self.pacman == pos:
                        break
                    i += 1
                l = i * 250
            else:
                l=-100
        
        return total_eval + l

    def utility_ghost(self, ghost_i):
        """Evaluate state for Ghost (minimizer). Ghosts want to catch Pacman."""
        if self.is_terminal():
            if self.pacman in self.ghosts:
                return float("-inf")  # Ghost wins if Pacman is caught
            else:
                return float("inf")  # Ghost loses if Pacman escapes
        
        # PACMAN HUNTING: Calculate base hunting score
        ghost_to_pacman_dist = self.get_pacman_shortest_distance(ghost_i)
        
        # Terminal conditions first
        if ghost_to_pacman_dist == 0:
            return float("-inf")  # Caught Pacman!
        
        # Base evaluation based on distance to Pacman
        if ghost_to_pacman_dist == 1:
            base_eval = 1000  # About to catch
        elif ghost_to_pacman_dist <= 3:
            base_eval = 200  # Close to Pacman
        elif ghost_to_pacman_dist <= 5:
            base_eval = 100  # Moderately close
        elif ghost_to_pacman_dist <= 8:
            base_eval = 30   # Getting closer
        else:
            # Ghost far from Pacman - use BFS info if available
            try:
                from src import bfs_to_pacman
                shortest_path_to_pacman = bfs_to_pacman(self, self.ghosts[ghost_i], self.MOVES, self.OBSTACLES, self.BOARD_WIDTH, self.BOARD_HEIGHT)
                if shortest_path_to_pacman:
                    path_length = len(shortest_path_to_pacman)
                    # Incentivize moving closer along the shortest path
                    base_eval = 50 - (path_length * 2)
                else:
                    base_eval = -100  # Can't reach Pacman, penalize
            except:
                # Fallback if BFS fails
                base_eval = max(0, 20 - ghost_to_pacman_dist)
        
        # COOPERATION BONUS: Award ghosts for working together
        other_ghost_i = 1 if ghost_i == 0 else 0
        other_ghost_dist_to_pacman = self.get_pacman_shortest_distance(other_ghost_i)
        ghost_to_ghost_dist = self.ghost_to_ghost_distance(ghost_i, other_ghost_i)
        
        cooperation_bonus = 0
        
        # Both ghosts very close to pacman = highest cooperation bonus
        if ghost_to_pacman_dist <= 3 and other_ghost_dist_to_pacman <= 3:
            cooperation_bonus = 300  # Extremely strong bonus for boxing pacman
        # Both ghosts moderately close
        elif ghost_to_pacman_dist <= 5 and other_ghost_dist_to_pacman <= 5:
            cooperation_bonus = 200  # Strong bonus for boxing pacman in
        elif ghost_to_pacman_dist <= 6 and other_ghost_dist_to_pacman <= 6:
            cooperation_bonus = 100  # Good coordination bonus
        
        # Distance between ghosts - reward spreading out to trap pacman (only when close to pacman)
        if ghost_to_pacman_dist <= 6 and other_ghost_dist_to_pacman <= 8:
            if ghost_to_ghost_dist > 5:
                cooperation_bonus += 5  # Excellent spread for trapping
            elif ghost_to_ghost_dist > 3:
                cooperation_bonus += 10  # Good spread
            elif ghost_to_ghost_dist < 2:
                cooperation_bonus -= 10  # Penalty for being too close together
        
        final_eval = base_eval + cooperation_bonus
        return -final_eval