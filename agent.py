import pygame
from collections import deque
import heapq
from math import inf

class Agent(pygame.sprite.Sprite):
    def __init__(self, environment, grid_size):
        super().__init__()
        self.image = pygame.Surface((grid_size, grid_size))
        self.image.fill((0, 0, 255))  # Agent color is blue
        self.rect = self.image.get_rect()
        self.grid_size = grid_size
        self.environment = environment
        self.position = [0, 0]  # Starting at the top-left corner of the grid
        self.rect.topleft = (0, 0)
        self.task_completed = 0
        self.completed_tasks = []
        self.path = []  # List of positions to follow
        self.moving = False  # Flag to indicate if the agent is moving

    def draw(self, screen):
        """Draw the agent on the screen.""" 
        # draws the agent at its current position on the screen using Pygame.
        screen.blit(self.image, self.rect)

    def move(self):
        """Move the agent along the path."""
        if self.path:
            next_position = self.path.pop(0)
            self.position = list(next_position)
            self.rect.topleft = (self.position[0] * self.grid_size, self.position[1] * self.grid_size)
            self.check_task_completion()
        else:
            self.moving = False  # Stop moving when path is exhausted

    def check_task_completion(self):
        """Check if the agent has reached a task location."""
        position_tuple = tuple(self.position)
        if position_tuple in self.environment.task_locations:
            task_number = self.environment.task_locations.pop(position_tuple)
            self.task_completed += 1
            self.completed_tasks.append(task_number)

    def find_path_to(self, target, algorithm='UCS'):
        """Calculate path to the target using the specified algorithm (UCS or A*)."""
        start = tuple(self.position)
        frontier = []
        heapq.heappush(frontier, (0 + (self.heuristic(start, target) if algorithm == 'A*' else 0), start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current_cost, current = heapq.heappop(frontier)

            if current == target:
                break

            for next_pos in self.environment.neighbors(current):
                new_cost = cost_so_far[current] + self.environment.step_cost(current, next_pos)
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + (self.heuristic(next_pos, target) if algorithm == 'A*' else 0)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current

        # Reconstruct path
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def find_nearest_task(self):
        """Find the nearest task using Manhattan distance and return its position."""
        if not self.environment.task_locations:
            return None  # No tasks to complete

        # Find the nearest task using Manhattan distance
        nearest_task = min(
            self.environment.task_locations.keys(),
            key=lambda task: self.heuristic(tuple(self.position), task)
        )
        return nearest_task

    def heuristic(self, a, b):
        """Manhattan distance on a grid."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])