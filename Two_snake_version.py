import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)
WHITE_COLOR = (255, 255, 255)


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/The_apple_everyone_want.jpg").convert()
        self.parent_screen = parent_screen
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'
        self.length = 1
        self.x = [SIZE]  # SIZE == 40 [SIZE]
        self.y = [SIZE]
        self.dead = False

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update body
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        #   update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE
        elif self.direction == 'up':
            self.y[0] -= SIZE
        elif self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
            print(self.x[i], self.y[i])

        pygame.display.update()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Codebasics Snake And Apple Game")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800))
        self.snake1 = Snake(self.surface) # for the yellow one.
        self.snake2 = Snake(self.surface) # for the blue one.
        # for initialize the two snakes's pictures.
        self.snake1.image = pygame.image.load("resources/deku.jpg").convert()
        self.snake2.image = pygame.image.load("resources/bakugou.jpg").convert()
        # for initialize the two snakes' positions
        self.snake1.x = [920]
        self.snake1.y = [40]
        self.snake2.x = [40]
        self.snake2.y = [40]
        self.snake1.draw()
        self.snake2.draw()
        self.snake1.dead = False
        self.snake2.dead = False
        # todo for the two apples

        self.apple1 = Apple(self.surface)
        self.apple1.image = pygame.image.load("resources/The_apple_everyone_want.jpg").convert()
        self.apple1.draw()

        self.apple2 = Apple(self.surface)
        self.apple2.image = pygame.image.load("resources/gold_apple.jpg").convert()
        self.apple2.draw()

    def play_background_music(self):  # todo spend times read docs
        pygame.mixer.music.load('resources/My_Hero_Academy_OP.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound(r"D:\Python\Master_Python\Python_Snake_games\resources\crash.mp3")
            pygame.mixer.Sound.play(sound)
        elif sound_name == "ding":
            sound = pygame.mixer.Sound(r"D:\Python\Master_Python\Python_Snake_games\resources\ding.mp3")
            pygame.mixer.Sound.play(sound)

        # pygame.mixer.Sound.play(pygame.mixer.Sound("resouces/ding.mp3"))
        print("todo recover")

    def reset(self):
        self.snake1 = Snake(self.surface)
        self.snake2 = Snake(self.surface)
        self.snake1.dead = False
        self.snake2.dead = False
        self.snake1.x = [920]
        self.snake1.y = [40]
        self.snake2.x = [40]
        self.snake2.y = [40]
        self.snake1.image = pygame.image.load("resources/deku.jpg").convert()
        self.snake2.image = pygame.image.load("resources/bakugou.jpg").convert()

        self.apple1 = Apple(self.surface)
        self.apple1.image = pygame.image.load("resources/The_apple_everyone_want.jpg").convert()
        self.apple2 = Apple(self.surface)
        self.apple2.image = pygame.image.load("resources/gold_apple.jpg").convert()


    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        return False

    def collide_boundaries(self, x, y):
        if x > 1000 or x < 0:
            print("is collide")
            return True
        if y > 800 or y < 0:
            print("is collide")
            return True

        print("not collide")
        return False

    def render_background(self):
        bg = pygame.image.load("resources/background_hero.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        # for the two snake
        # if self.snake2.dead == True:
        #     print("go expection")
        if self.snake1.dead == True and self.snake2.dead == True:
            print("default true ?? ")
            raise "Collision Occured"
        if self.snake1.dead == False:
            self.snake1.walk()
            print("DEKU ALIVE")
        if self.snake2.dead == False:
            self.snake2.walk()
            print("BAKUGOU ALIVE")
        # self.snake2.walk()
        # TODO: Make the apple become two
        self.apple1.draw()
        self.apple2.draw()

        self.display_score()

        pygame.display.flip() # for the screen update

        # snake colliding with apple

        if self.is_collision(self.snake1.x[0], self.snake1.y[0], self.apple1.x, self.apple1.y):
            self.play_sound("ding")
            self.snake1.increase_length()
            self.apple1.move()
            self.apple1.draw()

        if self.is_collision(self.snake2.x[0], self.snake2.y[0], self.apple1.x, self.apple1.y):
            self.play_sound("ding")
            self.snake2.increase_length()
            self.apple1.move()
            self.apple1.draw()

        if self.is_collision(self.snake1.x[0], self.snake1.y[0], self.apple2.x, self.apple2.y):
            self.play_sound("ding")
            self.snake1.increase_length()
            self.apple2.move()
            self.apple2.draw()

        if self.is_collision(self.snake2.x[0], self.snake2.y[0], self.apple2.x, self.apple2.y):
            self.play_sound("ding")
            self.snake2.increase_length()
            self.apple2.move()
            self.apple2.draw()
        # todo make these sankes over the window
        # snake colliding with itself
        if self.snake1.dead == False:
            for i in range(3, self.snake1.length):
                if self.is_collision(self.snake1.x[0], self.snake1.y[0], self.snake1.x[i], self.snake1.y[i]):
                    self.play_sound("crash")
                    self.snake1.dead = True

        if self.snake2.dead == False:
            for i in range(3, self.snake2.length):
                if self.is_collision(self.snake2.x[0], self.snake2.y[0], self.snake2.x[i], self.snake2.y[i]):
                    self.play_sound("crash")
                    self.snake2.dead = True

        # TODO if snake1's head eats snake2 it becomes bigger
        if self.snake1.dead == False and self.snake2.dead == False:
            for i in range(self.snake2.length):
                if self.is_collision(self.snake1.x[0], self.snake1.y[0], self.snake2.x[i], self.snake2.y[i]):
                    self.play_sound("crash")
                    self.snake2.dead = True

        # TODO if snake2's head eats snake1 it becomes bigger
        if self.snake1.dead == False and self.snake2.dead == False:
            for i in range(self.snake1.length):
                if self.is_collision(self.snake2.x[0], self.snake2.y[0], self.snake1.x[i], self.snake1.y[i]):
                    self.play_sound("crash")
                    self.snake1.dead = True
        # TODO if both's head eats it becomes bigger

        # snake colliding with the wall boundaries
        # collides with boundaries.
        if self.snake1.dead == False:
            if self.collide_boundaries(self.snake1.x[0], self.snake1.y[0]):
                self.play_sound("crash")
                self.snake1.dead = True
                for i in range(self.snake1.length):
                    self.snake1.x[i] = -10000000000 - 1000 * i
                    self.snake1.y[i] = -10000000000 - 1000 * i
        if self.snake2.dead == False:
            if self.collide_boundaries(self.snake2.x[0], self.snake2.y[0]):
                self.play_sound("crash")
                self.snake2.dead = True
                for i in range(self.snake2.length):
                    self.snake2.x[i] = -10000000000 - 1000 * i
                    self.snake2.y[i] = -10000000000 - 1000 * i

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake1.length + self.snake2.length}", True, (200, 200, 200))
        self.surface.blit(score, (850, 10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont("arial", 30)
        line1 = font.render(f"Game is over! Your score is {self.snake1.length + self.snake2.length}", True, WHITE_COLOR)
        self.surface.blit(line1, (200, 300))  # blit(source, postion)
        line2 = font.render("To play again press Enter. To exit press Escape!", True, WHITE_COLOR)
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        # for the first snake
                        if self.snake1.dead == False:
                            if event.key == K_LEFT:
                                self.snake1.move_left()

                            if event.key == K_RIGHT:
                                self.snake1.move_right()

                            if event.key == K_UP:
                                self.snake1.move_up()

                            if event.key == K_DOWN:
                                self.snake1.move_down()
                        # for the second snake
                        if self.snake2.dead == False:
                            if event.key == K_a:
                                self.snake2.move_left()

                            if event.key == K_d:
                                self.snake2.move_right()

                            if event.key == K_w:
                                self.snake2.move_up()

                            if event.key == K_s:
                                self.snake2.move_down()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                print(e)
                print("raise exception")
                self.show_game_over()
                pause = True
                self.reset()

            # self.snake.walk()
            time.sleep(.1)


if __name__ == "__main__":
    game = Game()
    game.run()
