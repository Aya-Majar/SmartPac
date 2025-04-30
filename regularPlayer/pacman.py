import pygame
import random
import sys

pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
TILE_SIZE = 35
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)


class Maze:
    def __init__(self, screen_width, screen_height, tile_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = tile_size  # Fixed: was named cellSize in draw method
        # integer division => returns whole number
        self.rows = screen_height // tile_size
        self.cols = screen_width // tile_size

        # layout(0 = empty, 1 = wall, 2 = dot) => 2d list
        # can be done with numpy arange? no, will generate unorderd nums
        self.layout = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
            [1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1],
            [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
            [1, 0, 1, 1, 2, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 2, 1, 1, 0, 1],
            [1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1],
            [1, 0, 1, 1, 2, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 2, 1, 1, 0, 1],
            [1, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 1],
            [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
            [1, 2, 0, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 0, 1],
            [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
            [1, 2, 2, 1, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 1, 2, 2, 1],
            [1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1],
            [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

    def wall(self, row, col):
        # maze boundaries - if position is out of the boundaries
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return True

        # within boundaries and
        # len(self.layout) = num of rows
        # len(self.layout[0]) = length of 1 row = num of cols
        if 0 <= row < len(self.layout) and col < len(self.layout[0]):
            # check if it is a wall
            return self.layout[row][col] == 1
        return False  # not wall

    def dot(self, row, col):
        if 0 <= row < len(self.layout) and col < len(self.layout[0]):
            return self.layout[row][col] == 2
        return False  # not dot

    def eat_dot(self, row, col):
        if 0 <= row < len(self.layout) and col < len(self.layout[0]):
            if self.layout[row][col] == 2:
                self.layout[row][col] = 0  # eated = empty = 0
                return 10  # dot score
        return 0  # no dot was eaten

    def all_dots_eaten(self):
        # Check if all dots have been eaten
        # search row by row
        for row in self.layout:
            for cell in row:
                if cell == 2:
                    return False
        return True

    def draw(self, screen):
        # for each row
        for row in range(len(self.layout)):
            # for each col
            for col in range(len(self.layout[row])):
                # coordinates
                x = col * self.cell_size
                y = row * self.cell_size

                if self.layout[row][col] == 1:  # wall
                    pygame.draw.rect(screen, BLUE, [x, y, self.cell_size, self.cell_size])
                elif self.layout[row][col] == 2:  # dot
                    pygame.draw.circle(screen, YELLOW,
                                       (x + self.cell_size // 2, y + self.cell_size // 2),
                                       self.cell_size / 10)


class Player:
    stop = True

    def __init__(self, tile_size, maze):
        # Initialize player in the middle of the maze
        self.row = 1
        self.col = 1
        self.tile_size = tile_size
        self.maze = maze
        self.direction = ""
        self.score = 0
        self.radius = tile_size // 2 - 2
        self.speed = 1

    def draw(self, screen):
        # Draw Pac-Man
        x = self.col * self.tile_size + self.tile_size // 2  # in the middle of tile
        y = self.row * self.tile_size + self.tile_size // 2
        pygame.draw.circle(screen, YELLOW, (x, y), self.radius)

    def change_direction(self, direction):
        self.direction = direction

    def update(self):
        new_row, new_col = self.row, self.col

        if self.direction == "up":
            new_row -= self.speed
        elif self.direction == "down":
            new_row += self.speed
        elif self.direction == "left":
            new_col -= self.speed
        elif self.direction == "right":
            new_col += self.speed

        # Check if the new position is valid (not a wall)
        if not self.maze.wall(new_row, new_col):
            self.row = new_row
            self.col = new_col
            # Check if there's a dot to eat
            self.score += self.maze.eat_dot(self.row, self.col)

    def check_ghost_collision(self, ghosts):
        if self.row == ghosts.row and self.col == ghosts.col:
            return True
        return False


class Ghost:
    def __init__(self, tile_size, maze, ghost_id):
        # Initialize ghost positions based on ghost_id
        self.row = 9  # Initial row position
        self.col = 9 + ghost_id % 2  # Stagger ghost positions

        self.tile_size = tile_size
        self.maze = maze
        self.positionMaze = [self.row, self.col]  # Position in maze coordinates
        self.positionX = self.col * tile_size  # Position in pixel coordinates
        self.positionY = self.row * tile_size  # Position in pixel coordinates

        # Set ghost colors based on ghost_id
        self.ghost_color = ["pinkGho1.png", "purpleGho.png"]
        self.ghost_image = self.ghost_color[ghost_id]

        # Initialize ghost movement parameters
        self.id = ghost_id
        self.move_delay = 250  # milliseconds between moves
        self.last_move_time = pygame.time.get_ticks()  # time of the last move
        self.actions = ["up", "down", "right", "left"]
        self.possible_action = []
        self.chooseExecuted = True
        self.choice = ""

        # For compatibility with player collision detection
        self.direction = ""

    def is_not_path(self, maze_layout, newPositionY, newPositionX):
        if 0 <= newPositionY < len(maze_layout) and 0 <= newPositionX < len(maze_layout[0]):
            return maze_layout[newPositionY][newPositionX] == 1
        return True  # Consider out of bounds as a wall

    def possibleActions(self):
        self.possible_action = []  # Clear previous actions

        # Check all four directions
        if not self.is_not_path(self.maze.layout, self.positionMaze[0] + 1, self.positionMaze[1]):
            self.possible_action.append("down")
        if not self.is_not_path(self.maze.layout, self.positionMaze[0] - 1, self.positionMaze[1]):
            self.possible_action.append("up")
        if not self.is_not_path(self.maze.layout, self.positionMaze[0], self.positionMaze[1] + 1):
            self.possible_action.append("right")
        if not self.is_not_path(self.maze.layout, self.positionMaze[0], self.positionMaze[1] - 1):
            self.possible_action.append("left")

        self.chooseExecuted = False

    def Choose(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.move_delay:
            # If we have more than one option, avoid going back the way we came
            if len(self.possible_action) > 1:
                if self.choice == "up" and "down" in self.possible_action:
                    self.possible_action.remove("down")
                elif self.choice == "down" and "up" in self.possible_action:
                    self.possible_action.remove("up")
                elif self.choice == "right" and "left" in self.possible_action:
                    self.possible_action.remove("left")
                elif self.choice == "left" and "right" in self.possible_action:
                    self.possible_action.remove("right")

            # Choose a random direction from available options
            if self.possible_action:  # Make sure there's at least one option
                self.choice = random.choice(self.possible_action)

                # Move ghost based on chosen direction
                if self.choice == "down":
                    self.positionY += TILE_SIZE
                    self.positionMaze[0] += 1
                    self.row += 1
                elif self.choice == "up":
                    self.positionY -= TILE_SIZE
                    self.positionMaze[0] -= 1
                    self.row -= 1
                elif self.choice == "right":
                    self.positionX += TILE_SIZE
                    self.positionMaze[1] += 1
                    self.col += 1
                elif self.choice == "left":
                    self.positionX -= TILE_SIZE
                    self.positionMaze[1] -= 1
                    self.col -= 1

                self.last_move_time = current_time

            self.possible_action = []
            self.chooseExecuted = True

    def update(self, player):
        # Get possible actions if needed
        if self.chooseExecuted:
            self.possibleActions()

        # Choose a direction and move
        if not self.chooseExecuted:
            self.Choose()

    def GhostDrawer(self):
        screen.blit(Ghost1Agent, (ghosts.positionX, ghosts.positionY))


# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

# Create game objects - maze | player | ghost
maze = Maze(SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE)
player = Player(TILE_SIZE, maze)

# create 1 ghost
ghosts = Ghost(TILE_SIZE, maze, 0)
Ghost1Agent = pygame.image.load(ghosts.ghost_image)
# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            player.stop = False
            if event.key == pygame.K_LEFT:
                player.change_direction("left")
            elif event.key == pygame.K_RIGHT:
                player.change_direction("right")
            elif event.key == pygame.K_UP:
                player.change_direction("up")
            elif event.key == pygame.K_DOWN:
                player.change_direction("down")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player.stop = True

                # Update game state
    if player.stop == False:
        player.update()
    ghosts.update(player)

    # Check for collisions
    if player.check_ghost_collision(ghosts):
        # Handle game over logic
        print("Game Over!")
        running = False

    # Check if all dots are eaten
    if maze.all_dots_eaten():
        print("You Win!")
        running = False

    # Draw everything
    screen.fill(BLACK)
    maze.draw(screen)
    player.draw(screen)
    ghosts.GhostDrawer()

    # Update the display
    pygame.display.flip()
    clock.tick(10)  # 10 FPS

pygame.quit()
sys.exit()
