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
        if not self.ghosts:
            return float('inf')
        return min(self.manhattan_distance(self.pacman, ghost) for ghost in self.ghosts)

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
            total_eval -= 800  # Very dangerous!
        elif ghost_distance == 2:
            total_eval -= 400  # Still very dangerous
        elif ghost_distance <= 3:
            total_eval -= 150  # Caution zone
        elif ghost_distance <= 5:
            total_eval -= 50   # Still be careful
        else:
            total_eval += 30   # Safe distance, small reward
        
        # FOOD ATTRACTION: Strong incentive to eat food
        if self.points:
            food_distance = self.get_nearest_food_distance()
            food_reward = 300 - (food_distance * 15)  # Closer food = bigger reward
            total_eval += food_reward
            
            # Bonus for clearing the board
            remaining_points_penalty = (len(self.points) * 25)
            total_eval -= remaining_points_penalty
        
        return total_eval

    def utility_ghost(self, ghost_i):
        """Evaluate state for Ghost (minimizer). Ghosts want to catch Pacman."""
        if self.is_terminal():
            if self.pacman in self.ghosts:
                return float("inf")  # Ghost wins if Pacman is caught
            else:
                return float("-inf")  # Ghost loses if Pacman escapes
        
        # PACMAN HUNTING: Calculate base hunting score
        ghost_to_pacman_dist = self.manhattan_distance(self.ghosts[ghost_i], self.pacman)
        
        # Terminal conditions first
        if ghost_to_pacman_dist == 0:
            return float("inf")  # Caught Pacman!
        
        # Base evaluation based on distance to Pacman
        if ghost_to_pacman_dist == 1:
            base_eval = 500  # About to catch
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
        other_ghost_dist_to_pacman = self.manhattan_distance(self.ghosts[other_ghost_i], self.pacman)
        ghost_to_ghost_dist = self.manhattan_distance(self.ghosts[ghost_i], self.ghosts[other_ghost_i])
        
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
                cooperation_bonus += 80  # Excellent spread for trapping
            elif ghost_to_ghost_dist > 3:
                cooperation_bonus += 40  # Good spread
            elif ghost_to_ghost_dist < 2:
                cooperation_bonus -= 50  # Penalty for being too close together
        
        final_eval = base_eval + cooperation_bonus
        return -final_eval