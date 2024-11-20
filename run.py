import pygame
import sys
from agent import Agent
from environment import Environment

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 20
NUM_TASKS = 10
NUM_BARRIERS = 30
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
GRID_PIXEL_SIZE = 30

# Setup the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Pathfinding Simulation: UCS and A* Agents')

# Create environment
environment = Environment(GRID_SIZE, NUM_TASKS, NUM_BARRIERS)

# Create two agents
agent_ucs = Agent(environment, GRID_PIXEL_SIZE)
agent_a_star = Agent(environment, GRID_PIXEL_SIZE)

# Distinguish agents by their colors
agent_ucs.image.fill((255, 0, 0))  # Red for UCS agent
agent_a_star.image.fill((0, 0, 255))  # Blue for A* agent

# Set different starting positions for the agents
agent_ucs.position = [0, 0]
agent_ucs.rect.topleft = (0, 0)

agent_a_star.position = [GRID_SIZE - 1, GRID_SIZE - 1]
agent_a_star.rect.topleft = ((GRID_SIZE - 1) * GRID_PIXEL_SIZE, (GRID_SIZE - 1) * GRID_PIXEL_SIZE)

def draw_task_info():
    """Draw combined task information for both agents."""
    font = pygame.font.Font(None, 36)
    
    # UCS agent stats
    ucs_status = f"Algorithm: Uniform Cost Search"
    ucs_tasks_completed = f"Tasks Completed: {agent_ucs.task_completed}"
    ucs_position = f"Position: {agent_ucs.position}"
    ucs_completed_tasks = "Completed Tasks: " + ", ".join(
        [str(task) for task in agent_ucs.completed_tasks]
    )
    ucs_total_cost = f"Total Path Cost: {sum(agent_ucs.completed_tasks)}"

    # A* agent stats
    astar_status = f"Algorithm: A* Search"
    astar_tasks_completed = f"Tasks Completed: {agent_a_star.task_completed}"
    astar_position = f"Position: {agent_a_star.position}"
    astar_completed_tasks = "Completed Tasks: " + ", ".join(
        [str(task) for task in agent_a_star.completed_tasks]
    )
    astar_total_cost = f"Total Path Cost: {sum(agent_a_star.completed_tasks)}"

    # Combine the stats into a single section
    combined_stats = [
        ucs_status, ucs_tasks_completed, ucs_position, ucs_completed_tasks, ucs_total_cost, "",
        astar_status, astar_tasks_completed, astar_position, astar_completed_tasks, astar_total_cost
    ]

    # Display the stats
    for i, line in enumerate(combined_stats):
        color = (255, 0, 0) if "UCS" in line else (0, 0, 255) if "A*" in line else (0, 0, 0)
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (GRID_SIZE * GRID_PIXEL_SIZE + 20, 20 + i * 30))

def draw_grid_with_numbers():
    """Draw the grid and tasks with numbers."""
    font = pygame.font.Font(None, 36)
    
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * GRID_PIXEL_SIZE, y * GRID_PIXEL_SIZE, GRID_PIXEL_SIZE, GRID_PIXEL_SIZE)
            if environment.grid[x][y] == 1:
                pygame.draw.rect(screen, (200, 0, 0), rect)  # Barriers are red
            elif environment.grid[x][y] == 2:
                pygame.draw.rect(screen, (0, 200, 0), rect)  # Tasks are green
                task_number = environment.task_locations.get((x, y), None)
                if task_number:
                    task_surface = font.render(str(task_number), True, (0, 0, 0))
                    screen.blit(task_surface, (x * GRID_PIXEL_SIZE + GRID_PIXEL_SIZE // 3, y * GRID_PIXEL_SIZE + GRID_PIXEL_SIZE // 3))
            elif environment.grid[x][y] == 0:
                pygame.draw.rect(screen, (255, 255, 255), rect)  # Completed tasks turn white
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Grid lines

def main():
    clock = pygame.time.Clock()
    simulation_started = False
    last_move_time = 0
    MOVEMENT_DELAY = 1000  # 1 second between moves

    # Start button
    start_button = pygame.Rect(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 50, 140, 40)

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    simulation_started = True

        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw grid and tasks
        draw_grid_with_numbers()

        # Draw agents
        agent_ucs.draw(screen)
        agent_a_star.draw(screen)

        # Draw task information
        draw_task_info()

        # Draw start button
        font = pygame.font.Font(None, 36)
        if start_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (0, 255, 0), start_button)
        else:
            pygame.draw.rect(screen, (0, 200, 0), start_button)
        start_text = font.render("Start", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, start_text_rect)

        # Start simulation
        if simulation_started:
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time > MOVEMENT_DELAY:
                # UCS agent movement
                if not agent_ucs.moving and environment.task_locations:
                    nearest_task_ucs = agent_ucs.find_nearest_task()
                    if nearest_task_ucs:  # Ensure a valid task exists
                        agent_ucs.path = agent_ucs.find_path_to(nearest_task_ucs, algorithm='UCS')
                        agent_ucs.moving = True
                elif agent_ucs.moving:
                    agent_ucs.move()

                # A* agent movement
                if not agent_a_star.moving and environment.task_locations:
                    nearest_task_a_star = agent_a_star.find_nearest_task()
                    if nearest_task_a_star:  # Ensure a valid task exists
                        agent_a_star.path = agent_a_star.find_path_to(nearest_task_a_star, algorithm='A*')
                        agent_a_star.moving = True
                elif agent_a_star.moving:
                    agent_a_star.move()

                last_move_time = current_time

        # Update the display at a fixed frame rate
        pygame.display.flip()
        clock.tick(30)  # Limit to 30 frames per second

if __name__ == "__main__":
    main()