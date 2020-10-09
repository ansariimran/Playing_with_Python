#Snake game
#I haven't commented out this progaram much because i think it's self explanatory; use kite for python
import sys
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

pygame.init()
    

class Cube(object):
    rows = 20
    w = 500
    def __init__(self, start, direction_x=1, direction_y=0, color=(255, 0, 0)):
        self.position = start
        self.direction_x = 1
        self.direction_y = 0
        self.color = color

    def move(self, direction_x, direction_y):
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.position = (self.position[0] + self.direction_x, self.position[1] + self.direction_y)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.position[0]
        j = self.position[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis // 2
            radius = 3
            #eye correction implementation - starts here
            if self.direction_x == 1 and self.direction_y == 0:
                circle_middle1 = (i*dis+dis-8, j*dis+7)
                circle_middle2 = (i*dis+dis-8, j*dis+dis-7)
                # circle_middle1 = (i*dis+dis-8, j*dis+radius*2)
                # circle_middle2 = (i*dis+dis-8, j*dis+dis-radius*2)
                pygame.draw.circle(surface, (0, 0, 0), circle_middle1, radius)
                pygame.draw.circle(surface, (0, 0, 0), circle_middle2, radius)

            elif self.direction_x == -1 and self.direction_y == 0:
                circle_middle3 = (i*dis+8, j*dis+7)
                circle_middle4 = (i*dis+8, j*dis+dis-7)
                pygame.draw.circle(surface, (0, 0, 0), circle_middle3, radius)
                pygame.draw.circle(surface, (0, 0, 0), circle_middle4, radius)

            elif self.direction_x == 0 and self.direction_y == 1:
                circle_middle7 = (i*dis+7, j*dis+dis-8)
                circle_middle8 = (i*dis+dis-7, j*dis+dis-8)
                pygame.draw.circle(surface, (0, 0, 0), circle_middle7, radius)
                pygame.draw.circle(surface, (0, 0, 0), circle_middle8, radius)
                
            elif self.direction_x == 0 and self.direction_y == -1:
                circle_middle5 = (i*dis+7, j*dis+8)
                circle_middle6 = (i*dis+dis-7, j*dis+8)
                pygame.draw.circle(surface, (0, 0, 0), circle_middle5, radius)
                pygame.draw.circle(surface, (0, 0, 0), circle_middle6, radius)
                
            #eye correction implementation - ends here


class Snake(object):
    body = []
    turns = {}
    def __init__(self, color, position):
        self.color = color
        self.head = Cube(position)
        self.body.append(self.head)
        self.direction_x = 0
        self.direction_y = 0

    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            pygame.init()
            keys = pygame.key.get_pressed()


            #implementation2 starts here            
            flag1 = keys[pygame.K_LEFT]
            flag2 = keys[pygame.K_RIGHT]
            flag3 = keys[pygame.K_UP]
            flag4 = keys[pygame.K_DOWN]

            for key in keys:
                if self.direction_x == 1 and self.direction_y == 0:
                    flag1 = False
                elif self.direction_x == -1 and self.direction_y == 0:
                    flag2 = False
                elif self.direction_x == 0 and self.direction_y == 1:
                    flag3 = False
                elif self.direction_x == 0 and self.direction_y == -1:
                    flag4 = False
            #implementation2 ends here

            #changes made inline with implementation2-Starts here
            for key in keys:
                if flag1:
                    self.direction_x = -1
                    self.direction_y = 0
                    self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]

                elif flag2:
                    self.direction_x = 1
                    self.direction_y = 0
                    self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]
                    
                elif flag3:
                    self.direction_x = 0
                    self.direction_y = -1
                    self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]
                    
                elif flag4:
                    self.direction_x = 0
                    self.direction_y = 1
                    self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]

            #changes made inline with implementation2-Ends here


        # i is for index & c is for cube object reference
        for i, c in enumerate(self.body):
            p = c.position[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            
            else:
                if c.direction_x == -1 and c.position[0] <= 0:
                    c.position = (c.rows-1, c.position[1])
                elif c.direction_x == 1 and c.position[0] >= c.rows-1:
                    c.position = (0, c.position[1])
                elif c.direction_y == -1 and c.position[1] <= 0:
                    c.position = (c.position[0], c.rows-1)
                elif c.direction_y == 1 and c.position[1] >= c.rows-1:
                    c.position = (c.position[0], 0)
                else: c.move(c.direction_x, c.direction_y)


    def reset(self, position):
        self.head = Cube(position)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.direction_x = 0
        self.direction_y = 1


    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.direction_x, tail.direction_y

        if dx == 1 and dy == 0:
                    self.body.append(Cube((tail.position[0]-1, tail.position[1])))
        elif dx == -1 and dy == 0:
                    self.body.append(Cube((tail.position[0]+1, tail.position[1])))
        elif dx == 0 and dy == 1:
                    self.body.append(Cube((tail.position[0], tail.position[1]-1)))
        elif dx == 0 and dy == -1:
                    self.body.append(Cube((tail.position[0], tail.position[1]+1)))
            
        self.body[-1].direction_x = dx
        self.body[-1].direction_y = dy


    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)
    
def draw_grid(w, rows, surface):
    sizebtwn = w // rows
    
    x = 0
    y = 0
    for i in range(rows):
        x = x + sizebtwn
        y = y + sizebtwn
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

def redraw_window(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows, surface)
    pygame.display.update()

def random_snack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.position == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x, y)
    #checked-OK

#Message box function for after loosig message
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
    
def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = Snake((255, 0, 0), (10, 10))
    snack = Cube(random_snack(rows, s), (0, 255, 0))

    clock = pygame.time.Clock()

    while 1:
        pygame.init()
        pygame.time.delay(50)
        clock.tick(10)
        s.move()

        #if head position is same as snack position, snack is added to the snake body by calling add_cube function
        if s.body[0].position == snack.position:
            s.add_cube()
            snack = Cube(random_snack(rows, s), (0, 255, 0)) #generating snacks at random location
                
        
        #below code calls message box function when position of any cube of snake-body is same as position of any other cube of the snake-body
        for x in range(len(s.body)):
            if s.body[x].position in list(map(lambda z:z.position, s.body[x+1:])):
                print('score: ', len(s.body))
                message_box("you lost!!!", "Play again")
                s.reset((10, 10))
                break
        redraw_window(win)
    
      
main()    