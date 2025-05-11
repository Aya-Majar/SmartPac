pacman.py
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
    dots = []
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
            [1, 0, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
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
        self.dots=[]
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
                    self.dots.append((row,col))
                    pygame.draw.circle(screen, YELLOW,
                                       (x + self.cell_size // 2, y + self.cell_size // 2),
                                       self.cell_size / 10)


class Player:
    stop=True
    possible_action = []
    target=[]
    cost=[]
    direction_cost=[]
    target_reached=True
    done=False
    tookLongValue=3
    Loops=0
    using_astar=False


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
        x = self.col * self.tile_size + self.tile_size // 2 # in the middle of tile
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
   

    def is_not_path(self, maze_layout, newPositionY, newPositionX):
        if 0 <= newPositionY < len(maze_layout) and 0 <= newPositionX < len(maze_layout[0]):
            return maze_layout[newPositionY][newPositionX] == 1
        return True  # Consider out of bounds as a wall
    

    def calculate_ghost_penalty(self, position, ghosts):
        penalty = 0
        for ghost in [ghosts]:  # Correct: iterate over each ghost               
            ghost_pos = (ghost.row, ghost.col)
            distance = self.manhattan_distance(position, ghost_pos)
            if distance <= 1:
                penalty += 50
            elif distance == 2:
                penalty += 15
            elif distance == 3:
                penalty += 5
        return penalty
    

    def possibleActions(self):
        self.possible_action = []  # Clear previous actions

        # Check all four directions
        if not self.is_not_path(self.maze.layout, self.row + 1, self.col):
            self.possible_action.append("down")
            self.direction_cost.append(self.manhattan_distance(( self.row + 1, self.col),self.target)+
             self.calculate_ghost_penalty((self.row + 1, self.col),ghosts) ) 
            
        if not self.is_not_path(self.maze.layout, self.row - 1, self.col):
            self.possible_action.append("up")
            self.direction_cost.append(self.manhattan_distance(( self.row - 1, self.col),self.target)+
             self.calculate_ghost_penalty(( self.row - 1, self.col),ghosts) ) 
            
        if not self.is_not_path(self.maze.layout, self.row, self.col + 1):
            self.possible_action.append("right")
            self.direction_cost.append(self.manhattan_distance(( self.row, self.col + 1),self.target)+
             self.calculate_ghost_penalty((  self.row, self.col + 1),ghosts))
             
        if not self.is_not_path(self.maze.layout, self.row, self.col - 1):
            self.possible_action.append("left")
            self.direction_cost.append(self.manhattan_distance(( self.row, self.col - 1),self.target)+
             self.calculate_ghost_penalty((self.row, self.col - 1),ghosts)) 
            

    def manhattan_distance(self,start, goal):
     # start and goal are (row, col)
     return abs(start[0] - goal[0]) + abs(start[1] - goal[1])
    
    
    def AStarSearch(self):
      if maze.all_dots_eaten():
        print("You Win!")
        self.done=True
        return
      
      self.direction_cost=[]
      self.cost=[]
 
      for dots in maze.dots:
            self.cost.append(self.manhattan_distance((self.row,self.col),(dots)))

      indices = [i for i, x in enumerate(self.cost) if x == min(self.cost)]
      if not(self.target_reached) and self.tookLongValue<= self.Loops:
        self.target=maze.dots[random.choice(indices)]    
      else:self.target=maze.dots[self.cost.index(min(self.cost))]
      self.target_reached=False

      self.possibleActions()

      if not(self.target_reached) and self.tookLongValue<= self.Loops:
         if len(self.possible_action)!=1:
                if self.direction=="up" and "down" in self.possible_action:
                    self.direction_cost.pop(self.possible_action.index("down"))
                    self.possible_action.remove("down")
                    
                elif self.direction=="down" and "up" in self.possible_action:
                    self.direction_cost.pop(self.possible_action.index("up")) 
                    self.possible_action.remove("up") 
                elif self.direction=="right" and "left" in self.possible_action:
                 self.direction_cost.pop(self.possible_action.index("left"))
                 self.possible_action.remove("left") 
                 
                elif self.direction=="left" and "right" in self.possible_action:
                    self.direction_cost.pop(self.possible_action.index("right"))
                    self.possible_action.remove("right") 
                    
      min_value = min(self.direction_cost)
      indices = [i for i, x in enumerate(self.direction_cost) if x == min_value]            
      self.index= random.choice(indices)
      self.change_direction(self.possible_action[self.index])

      self.update()

      if not(maze.dot(self.target[0], self.target[1])):
          self.target_reached=True
          self.Loops=0
      else:  self.Loops+=1  


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
        else:
            self.Choose()
    def GhostDrawer(self):
        screen.blit(Ghost1Agent,(ghosts.positionX,ghosts.positionY))
   

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

# Create game objects - maze | player | ghost
maze = Maze(SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE)
player = Player(TILE_SIZE, maze)
ghosts = Ghost(TILE_SIZE, maze,0) 

Ghost1Agent = pygame.image.load(ghosts.ghost_image)
no_of_loops=0


# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            player.stop=False
            if event.key == pygame.K_LEFT:
                player.change_direction("left")
            elif event.key == pygame.K_RIGHT:
                player.change_direction("right")
            elif event.key == pygame.K_UP:
                player.change_direction("up")
            elif event.key == pygame.K_DOWN:
                player.change_direction("down")
            elif event.key == pygame.K_a:  # Toggle A* pathfinding
                player.using_astar = not player.using_astar    
        if event.type==pygame.KEYUP:
           if event.key==pygame.K_UP or event.key==pygame.K_DOWN or event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT:
               player.stop=True 
    
    ghosts.update(player)

    # Check for collisions
    if player.check_ghost_collision(ghosts):
        # Handle game over logic
        print("Game Over!")
        print("Your score is "+ str(player.score))
        running = False
        
    # Draw everything
    screen.fill(BLACK)
    maze.draw(screen)
    player.draw(screen)
    ghosts.GhostDrawer()

    # Update player state
    if player.stop==False and not(player.using_astar) :
        player.update()
    elif player.using_astar:
         player.AStarSearch()
         no_of_loops+=1

     # Check if player winned
    if player.done:
        print(no_of_loops)
        print("Your score is "+ str(player.score))
        running = False

    # Update the display
    pygame.display.flip()
    clock.tick(10)  # 10 FPS
    
pygame.quit()
sys.exit()
