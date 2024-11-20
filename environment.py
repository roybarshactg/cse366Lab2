import random

class Environment:
    def __init__(self, grid_size, num_tasks, num_barriers):
        self.grid_size = grid_size
        self.grid = [[0] * grid_size for _ in range(grid_size)]  # 0 for empty, 1 for barrier, 2 for task
        self.task_locations = {}
        self.barriers = set()

        # Place tasks
        while len(self.task_locations) < num_tasks:
            x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
            if self.grid[x][y] == 0:
                self.grid[x][y] = 2
                self.task_locations[(x, y)] = len(self.task_locations) + 1

        # Place barriers
        while len(self.barriers) < num_barriers:
            x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
            if self.grid[x][y] == 0:
                self.grid[x][y] = 1
                self.barriers.add((x, y))

    def is_within_bounds(self, pos):
        x, y = pos
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size

    def is_passable(self, pos):
        return pos not in self.barriers

    def neighbors(self, pos):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        result = []
        for direction in directions:
            neighbor = (pos[0] + direction[0], pos[1] + direction[1])
            if self.is_within_bounds(neighbor) and self.is_passable(neighbor):
                result.append(neighbor)
        return result

    def step_cost(self, from_node, to_node):
        return 1  # Constant cost for all movements