import pygame
import random

pygame.init()

screen_width=600
screen_height=400

window=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Snake Game")

white=(255,255,255)
black=(0,0,0)
red=(213,50,80)
green=(0,255,0)

snake_block=20
snake_speed=15

clock=pygame.time.Clock()

game_over=False
game_close=False

x1=screen_width/2
y1=screen_height/2

x1_change=0
y1_change=0

foodx=round(random.randrange(0, screen_width-snake_block)/20.0)*20.0
foody=round(random.randrange(0,screen_height-snake_block)/20.0)*20.0

snake_List = []
Length_of_snake=1

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x1_change = -snake_block
                y1_change = 0
            elif event.key == pygame.K_RIGHT:
                x1_change = snake_block
                y1_change = 0
            elif event.key == pygame.K_UP:
                y1_change = -snake_block
                x1_change = 0
            elif event.key == pygame.K_DOWN:
                y1_change = snake_block
                x1_change = 0

x1 +=x1_change
y1 +=y1_change
snake_Head = []
snake_Head.append(x1)
snake_Head.append(y1)
snake_List.append(snake_Head)

if len(snake_List) > Length_of_snake:
        del snake_List[0] 
for x in snake_List[:-1]:
        if x == snake_Head:
            game_over = True               
if x1>=screen_width or x1<0 or y1>=screen_height or y1<0:
    game_over=True
window.fill(black)
pygame.draw.rect(window,red,[foodx,foody,snake_block,snake_block])


if x1 == foodx and y1 == foody:
        Length_of_snake +=1
        foodx = round(random.randrange(0, screen_width - snake_block) / 20.0) * 20.0
        foody = round(random.randrange(0, screen_height - snake_block) / 20.0) * 20.0
for x in snake_List:
     pygame.draw.rect(window,green,[x[0],x[1],snake_block,snake_block])
     

pygame.display.update()
clock.tick(snake_speed)

pygame.quit()
quit()



           