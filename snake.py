import os;
from time import sleep
import threading
from msvcrt import getch
import random


# #
# Config
#
mapClass = []
life = 1;
field_empty =" ";
snake_pattern = "x";
map_length = 6;
movement = 1
point = 0;

food_x_post = random.randint(0, map_length-1)
food_y_post = random.randint(0, map_length-1)
grow = 0;

# #
# Snake Class
#
class LinkedList:
    def __init__(self,val):
        self.val = val;
        self.prev = ''
        self.next = '';

    def setNext(self,val,prev):
        self.prev = prev;
        self.next = LinkedList(val);

    def getValue(self):
        return self.val;

    def getNext(self):
        return self.next;

    def getPrev(self):
        return self.prev;


class SnakeBlock(object):
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos;
        self.y_pos = y_pos;

    def move(self,movement):
        if(movement==2):
            self.x_pos = self.x_pos+1
            if self.x_pos == map_length:
                self.x_pos = 0;
        elif movement == 1:
            self.y_pos = self.y_pos+1
            if self.y_pos == map_length:
                self.y_pos = 0;
        elif movement ==-2:
            self.x_pos = self.x_pos-1
            if self.x_pos == -1:
                self.x_pos = map_length-1;
        elif movement == -1:
            self.y_pos = self.y_pos-1
            if self.y_pos == -1:
                self.y_pos = map_length-1;

    def follow(self,head):
        self.x_pos = head.getX();
        self.y_pos = head.getY();

    def setX(self,x):
        self.x_pos = x;

    def setY(self,y):
        self.y_pos = y;

    def getX(self):
        return self.x_pos;

    def getY(self):
        return self.y_pos;

class ocupiedPost():
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos;
        self.y_pos = y_pos;

    def getX(self):
        return self.x_pos;

    def getY(self):
        return self.y_pos;

# #
# Init Snake
#
snake = LinkedList(SnakeBlock(map_length/2,2));
snake.setNext(SnakeBlock(map_length/2,1),snake);
snake.next.setNext(SnakeBlock(map_length/2,0),snake.next);
snake.next.next.setNext(SnakeBlock(map_length/2,-1),snake.next.next);

# #
# Clear Screen to refresh
#
def clearScreen():
    osName = os.name;
    if (osName=='nt'):
        os.system('cls');
    elif(osName=='mac'):
        print('ClearScreen not Compatible Yet');
    else:
        os.system('clear');

# #
# Read input for movement direction
#
def readInput():
    global movement
    while 1:
        key =ord(getch())
        if(key):
            if(key==80):
                if movement != -1:
                    movement = 1
            elif key ==72:
                if movement != 1:
                    movement = -1
            elif key==75:
                if movement != 2:
                    movement = -2
            elif key==77:
                if movement != -2:
                    movement = 2

# # #
# For aranging movement
#
def movement_map():
    global x,y
    global snake;
    while (life>0):
        post = [];
        clearScreen()
        print("New Game")
        SnakeTemp = snake;
        while True:
            x_ = SnakeTemp.getValue().getX()
            y_ = SnakeTemp.getValue().getY()
            post.append(
                ocupiedPost(x_,y_)
            )
            SnakeTemp = SnakeTemp.next;
            if SnakeTemp == '':
                break;

        map = arrayMap(post)

        for i in range(0,map_length):
            print(map[i])

        print("Score :",point)
        moves = movement;
        SnakeTemp = snake;
        isEaten(snake, movement)
        Moving(snake,moves,0,0,0)

        sleep(1)

    print("GAME OVER");

def generateFoodPlace():
    global food_x_post,food_y_post
    food_x_post = random.randint(0, map_length-1)
    food_y_post = random.randint(0, map_length-1)

def Moving(snakes,moves,val,x__,y__):
    global grow,point
    if val == 0:
        x__ = snakes.getValue().getX();
        y__ = snakes.getValue().getY();
        if x__ == food_x_post :
            if y__ == food_y_post:
                generateFoodPlace()
                grow = 1;
                x_pos,y_pos = move_point(movement,x__,y__);
                Grow_snake(snake,x_pos,y_pos)
                point = point + 1;
                return 0;
        snakes.getValue().move(moves);
        val = 1;

    else:
        if(snakes==''):
            return 0;
        x__temp = snakes.getValue().getX();
        y__temp = snakes.getValue().getY();
        snakes.getValue().setX(x__);
        snakes.getValue().setY(y__);
        x__ = x__temp;
        y__ = y__temp;
    Moving(snakes.next,moves,val,x__,y__)

def Grow_snake(SnakeTemp,x_movement,y_movement):
    global grow
    if grow == 0 :
        return 0;
    if(SnakeTemp.getNext() == ''):
        SnakeTemp.setNext(SnakeBlock(x_movement,y_movement),SnakeTemp);
        grow = 0
        return 0;
    Grow_snake(SnakeTemp.next,x_movement,y_movement)

def move_point(move,x_pos,y_pos):
    if(move==2):
          x_pos = x_pos+1
          if x_pos == map_length:
              x_pos = 0;
    elif move == 1:
          y_pos = y_pos+1
          if y_pos == map_length:
              y_pos = 0;
    elif move ==-2:
          x_pos = x_pos-1
          if x_pos == -1:
              x_pos = map_length-1;
    elif move == -1:
          y_pos = y_pos-1
          if y_pos == -1:
              y_pos = map_length-1;
    return x_pos,y_pos;

def isEaten(snake_link, moves):
    x__ = snake_link.getValue().getX();
    y__ = snake_link.getValue().getY();
    checkBody(snake_link.next,x__,y__)

def checkBody(snake_link,snakeHead_x,snakeHead_y):
    global life;
    x__ = snake_link.getValue().getX();
    y__ = snake_link.getValue().getY();
    if x__ == snakeHead_x:
        if y__ == snakeHead_y:
            life = 0;
            return 1;
    if snake_link.getNext() == '':
        return 0;
    checkBody(snake_link.next,snakeHead_x,snakeHead_y)

def arrayMap(post):
    map = [];
    for i in range(0,map_length):
        x_map = []
        for j in range(0,map_length):
            checked = 0
            for k in range (0,len(post)):
                if post[k].getX() == j:
                    if post[k].getY() == i:
                        x_map.append(snake_pattern);
                        checked = checked+1;
            if checked == 0:
                if i == food_y_post and food_x_post ==j:
                    x_map.append('*')
                else:
                    x_map.append(field_empty);

        map.append(x_map);
    return map;

def gameConfig():
    global field_empty,snake_pattern,map_length
    print("Welcome to Snake Game")
    print("=========================================================")
    map_length = int(input("Please Input Length of your Snake Map []:"));
    while map_length % 2 == 1 :
        map_length = int(input("Please Input Length of your Snake Map []:"));
    snake_pattern = input("input your snake pattern")
    while snake_pattern ==" ":
        snake_pattern = input("input your snake pattern")
    print('Your Game will Start in 3 Seconds')
    sleep(3)
    clearScreen()

if __name__ == '__main__':

    gameConfig()

    movement_maps = threading.Thread(name='Movement', target=movement_map)
    wait_for_input = threading.Thread(name='input', target=readInput)
    try:
        movement_maps.start()
        wait_for_input.start()
        # check.start()
        movement_maps.join()
        wait_for_input.join()
    except KeyboardInterrupt:
        input();
