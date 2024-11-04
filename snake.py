from tkinter import *
import random

game_width = 700
game_height = 700
speed = 100
space_size = 50
body_parts = 3
snake_color = "#00FF00"
food_color = "red"
BKG_color = "black"




class Snake:
    def __init__(self):
        self.body_size = body_parts
        self.coordinates = []
        self.squares = []

        for i in range (0, body_parts):
            self.coordinates.append([0, 0])

        for x, y  in self.coordinates:
            square = canvas.create_rectangle(x, y, x +space_size, y + space_size, fill = snake_color, tag="snake")
            self.squares.append(square)
        
class Food:
    def __init__(self):

        x = random.randint(0, int(game_width / space_size)-1)*space_size
        y = random.randint(0, int(game_height / space_size)-1)*space_size
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + space_size, y + space_size, fill = food_color, tag="food")
# print(type(x))
def next_turn(snake, food):

    x, y = snake.coordinates[0]
    if direc == 'up':
        y -= space_size
    elif direc == 'down':
        y += space_size
    elif direc == 'left':
        x -= space_size
    elif direc == 'right':
        x += space_size

    if x < 0:
        x = game_width - space_size
    elif x >= game_width:
        x = 0
    if y < 0:
        y = game_height - space_size
    elif y >= game_height:
        y = 0

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + space_size, y + space_size, fill = snake_color)
    snake.squares.insert(0,square)
    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score
        score += 1
        label.config(text = "Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    
    else:
# delete the last body part of the snake
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_coll(snake):
        game_over()
    else:
        window.after(speed, next_turn, snake, food)


def change_dir(new_direc):

    global direc

    if new_direc == 'left':
        if direc != 'right':
            direc = new_direc
    if new_direc == 'right':
        if direc != 'left':
            direc = new_direc
    if new_direc == 'up':
        if direc != 'down':
            direc = new_direc
    if new_direc == 'down':
        if direc != 'up':
            direc = new_direc



  
def check_coll(snake):

    x, y =snake.coordinates[0]
    if x <0 or x>= game_width:
        return True
    elif y <0 or y>= game_height:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True



def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, text="Game Over", fill = "pink")

window = Tk()
window.title("Snake")
window.resizable(False, False)

score = 0
direc = 'down'

label = Label(window, text="score:{}".format(score), font=('consolas', 40))
label.pack()
canvas = Canvas(window, bg=BKG_color, height=game_height, width=game_width)
canvas.pack()

window.update()
window_width = window.winfo_width()
window_heigh = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_heigh = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_heigh/2) - (window_heigh/2))

window.geometry(f"{window_width}x{window_heigh}+{x}+{y}")

window.bind('<Left>', lambda event: change_dir('left'))
window.bind('<Right>', lambda event: change_dir('right'))
window.bind('<Up>', lambda event: change_dir('up'))
window.bind('<Down>', lambda event: change_dir('down'))

snake = Snake()
food = Food()

next_turn(snake, food)


window.mainloop()