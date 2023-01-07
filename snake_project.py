import pygame
import random
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

pygame.init()
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_UP)

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 102)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 600
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake_block = 10
FPS = 20

font_style = pygame.font.SysFont('bahnschrift', 25)
score_font = pygame.font.SysFont('comicsansms', 35)

start_time = pygame.time.get_ticks()

def Your_score(score):
    Play_time = round((pygame.time.get_ticks() - start_time) / 1000, 1)
    value = score_font.render('Your Score (speed) : ' + str(score) + '       Time : ' + str(Play_time), True, yellow)
    dis.blit(value, [0, 0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def gameLoop():
    game_over = False
    game_close = False
    
    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1



    foodx = round(random.randrange(10, dis_width - snake_block - 10) / 10.0) * 10.0
    foody = round(random.randrange(30, dis_height - snake_block - 10) / 10.0) * 10.0

    while not game_over:
        while game_close == True:
            dis.fill(blue)
            message('You Lost! Press C-Play Again or Q-Quite', red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        if GPIO.input(11) == 0:
            x1_change = -snake_block
            y1_change = 0
        elif GPIO.input(12) == 0:
            x1_change = snake_block
            y1_change = 0
        elif GPIO.input(13) == 0:
            x1_change = 0
            y1_change = -snake_block
        elif GPIO.input(15) == 0:
            x1_change = 0
            y1_change = snake_block
        
        if x1 >= dis_width - 10 or x1 < 10 or y1 >= dis_height - 10 or y1 < 30:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.line(dis, black, (10, 30), (dis_width - 10, 30))
        pygame.draw.line(dis, black, (10, 30), (10, dis_height - 10))
        pygame.draw.line(dis, black, (dis_width - 10, dis_height - 10), (10, dis_height - 10))
        pygame.draw.line(dis, black, (dis_width - 10, dis_height - 10), (dis_width - 10, 30))
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
        
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
        
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(10, dis_width - snake_block - 10) / 10.0) * 10.0
            foody = round(random.randrange(30, dis_height - snake_block - 10) / 10.0) * 10.0
            Length_of_snake += 1
        
        snake_speed = (FPS + Length_of_snake) / 2
        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
