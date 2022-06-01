import pygame
from pygame.locals import * #mport certain global variables
import time
import random

SIZE = 26
BACKGROUND_COLOUR = (12, 79, 30)
class Apple:
    def __init__(self,parent_screen):
        self.apple = pygame.image.load("resources/apple.png")
        self.apple = pygame.transform.scale(self.apple,(25,25))
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,37) * SIZE
        self.y = random.randint(1,22) * SIZE

class Snake:
    def __init__(self,parent_screen,length):
        self.lenght = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.block = pygame.transform.scale(self.block, (25, 25))
        self.head = pygame.image.load("resources/snake_head.png")
        self.head = pygame.transform.scale(self.head, (25, 30))
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'right'

    def increase_length(self):
        self.lenght += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOUR)
        for i in range(1,self.lenght):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
            self.parent_screen.blit(self.head, (self.x[0], self.y[0]))
        pygame.display.flip()


    def move_up(self):
        self.direction = 'up'
    def move_down(self):
        self.direction = 'down'
    def move_left(self):
        self.direction = 'left'
    def move_right(self):
        self.direction = 'right'

    def walk(self):
        for i in range(self.lenght-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if self.direction == 'up':
            self.y[0] -= SIZE
            self.draw()
        if self.direction == 'down':
            self.y[0] += SIZE
            self.draw()
        if self.direction == 'left':
            self.x[0] -= SIZE
            self.draw()
        if self.direction == 'right':
            self.x[0] += SIZE
            self.draw()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000,600))  # setmode initializes the game window do it in all py game program, first parameter size of the window
        self.surface.fill(BACKGROUND_COLOUR)
        self.snake = Snake(self.surface,2)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    # def is_collision(self,x1,y1,x2,y2):
    #     if x1 >= x2 and x1 < x2 + SIZE:
    #         if y1 >= y2 and y1 < y2 + SIZE:
    #             return True
    #     return False


    def is_collision(self,x1,y1,x2,y2):
        if x1 == x2 and y1==y2:
            return True
        return False



    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0],self.apple.x,self.apple.y):
            self.snake.increase_length()
            self.apple.move()

        #snake colliding with itself
        for i in range(3,self.snake.lenght):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                raise Exception("Game Over")
                # print("Game Over")
                # exit(0)

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOUR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Score: {self.snake.lenght - 2}", True, (0, 255, 255))
        self.surface.blit(line1,(200,200))
        line2 = font.render("To play the game again press Enter. To exit press Escape", True,(0, 255, 255))
        self.surface.blit(line2, (200, 250))
        pygame.display.flip()



    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.lenght-2}",True,(200,200,200))
        self.surface.blit(score,(800,10))

    def reset(self):
        self.snake = Snake(self.surface, 2)
        self.apple = Apple(self.surface)


    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():  # gives keyboard, mouse events
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        pause = False
                    if event.key == K_ESCAPE:
                        running = False
                    if not pause:
                        if event.key == K_UP:
                            if self.snake.direction != 'down':
                                self.snake.move_up()
                        if event.key == K_DOWN:
                            if self.snake.direction != 'up':
                                self.snake.move_down()
                        if event.key == K_LEFT:
                            if self.snake.direction != 'right':
                                self.snake.move_left()
                        if event.key == K_RIGHT:
                            if self.snake.direction != 'left':
                                self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause =True
                self.reset()

            time.sleep(0.1)




if __name__ == "__main__":
    game = Game()
    game.run()
    #pygame.display.flip()  #updates the surface after we change the property that is the fill colour and displays it

    #we need an event loop in any ui application which waits for the user input like mouse or keyboard input (its a while loop)

