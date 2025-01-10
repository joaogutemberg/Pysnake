import curses
import random
import time
def game_loop(window, game_speed): #The argument of the function is the game window

    # Setup Inicial 
    curses.curs_set(0) #Remove the cursor from the screen.
    snake = [          #Coordinates Y and X (ATENTION: curses starts counting from the top-left corner, from top to bottom).
        [10, 15],
        [9, 15],
        [8, 15],
        [7, 15],
     ]
    fruit = get_new_fruit(window=window)
    current_direction = curses.KEY_DOWN #Start with the character moving downward
    snake_ate_fruit = False #Otherwise, the snake starts the game growing
    score = 0
    while True:
        draw_screen(window=window) #Draws the window. The argument is the window for screen delimitation
        draw_snake(snake=snake, window=window) #Draws the caracter
        draw_actor(actor=fruit, window=window, char= '♥') #Draws the fruit
        direction = get_new_direction(window=window, timeout=game_speed) #Gets direction, window argument is for screen delimitation, and timeout to set the speed
        if direction is None: #If direction is null, continue with the previous direction
            direction = current_direction
        if direction_is_opposite(direction=direction, current_direction=current_direction): #If the direction is opposite to the current direction, it will be ignored. This prevents the snake from running into itself
            direction=current_direction
        move_snake(snake=snake, direction=direction,snake_ate_fruit=snake_ate_fruit) #Arguments: "subject" is the snake, the direction for movement, and snake_ate_fruit to grow the snake.
        if snake_hit_border(snake=snake, window=window): #If it hits the border, breaks
            break 
        if snake_hit_itself(snake=snake): #if it hits itself, breaks
            break
        if snake_hit_fruit(snake=snake, fruit=fruit):
            snake_ate_fruit = True #The moment the snake eats the fruit (it becomes True)
            fruit = get_new_fruit(window=window)
            score +=1 #Increases player's score
        else: 
            snake_ate_fruit = False #It returns the value to false, otherwise, if the snake eats one fruit, it will keep growing forever
        current_direction = direction #Make the indicated direction become the current direction, so that if nothing is pressed, it continues to move in the current direction

    finish_game(score=score, window=window)

def finish_game(score,window):
    height, width = window.getmaxyx()
    s = f'Game over! You collected {score} fruits ♥'
    y = int(height/ 2)
    x = int((width - len(s)) / 2)
    window.addstr(y, x , s) #Shows it on screen
    window.refresh() #Updates the window so that the text appears
    time.sleep(2.5) #Freezes the code for 2.5 seconds, so the user can read


def direction_is_opposite(direction, current_direction):
    match direction: 
            case curses.KEY_UP:
                return current_direction == curses.KEY_DOWN #Checks if the direction (inputted) is opposite to the current_direction
            case curses.KEY_DOWN:
                return current_direction == curses.KEY_UP
            case curses.KEY_LEFT:
                return current_direction == curses.KEY_RIGHT
            case curses.KEY_RIGHT:
                return current_direction == curses.KEY_LEFT



def get_new_fruit(window):
    height, width = window.getmaxyx() #Gets the maximum of Y and X
    return [random.randint(1, height-2), random.randint(1, width -2)] #Returns a fruit randomly within the marked spaces

def snake_hit_fruit(snake, fruit):
    return fruit in snake #That is, if the fruit is in the same position (within) the snake

def snake_hit_itself(snake):
    head = snake[0]
    body = snake[1:]
    return head in body #That is, if the head is in the same position(within) the body

def snake_hit_border(snake, window):
    head = snake[0]
    return actor_hit_border(actor=head, window=window)

def draw_screen(window):
    window.clear()
    window.border(0) #Draws the border
            
def draw_snake(snake, window):
    head = snake[0]
    draw_actor(actor=head, window=window, char='@')
    body = snake[1:]
    for body_part in body:
        draw_actor(actor=body_part, window=window, char=curses.ACS_DIAMOND)

def draw_actor(actor, window, char):
    window.addch(actor[0], actor[1], char) #Displays a specific character (Y position, X position, defined character) 
   
def get_new_direction(window, timeout):
    window.timeout(timeout) 
    direction = window.getch() #Gets the character inputted by the user   
    if direction in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
        return direction
    return None

def move_snake(snake, direction, snake_ate_fruit): #Snake movement with body
    head = snake[0].copy() #Creates a copy of the head 
    move_actor(actor=head, direction = direction) #The actor is the head, and the direction is the direction the user inputs
    snake.insert(0, head) #Inserts the head (copy) at position 0
    if not snake_ate_fruit: #If the snake doesn't eat the fruit, it will pop the last element
        snake.pop() #Removes the last element (from the end) all this will create the feeling of movement
    
def move_actor(actor, direction):        
        match direction: #It's a type of if and else; it will check if the char matches: 
            case curses.KEY_UP:
                actor[0] -= 1 #Move up
            case curses.KEY_DOWN:
                actor[0] += 1 #Move down
            case curses.KEY_LEFT:
                actor[1] -= 1 #Move left
            case curses.KEY_RIGHT:
                actor[1] += 1 #Move right

def actor_hit_border(actor, window): 
    height, width = window.getmaxyx()         
    if (actor[0]) <= 0 or (actor[0] >= height - 1):
        return True #It ends the game
    if (actor[1]) <= 0 or (actor[1] >= width - 1):
        return True #It also ends the game
    return False

def select_difficulty():
    difficulties = { #Dictionary to set the difficulty by timeout (game_speed)
        'easy': 500,
        'normal': 250,
        'hard': 100,
        'very hard': 50,
        'insane': 10,
    }
    while True:
        print(f'Difficulties: {', '.join(difficulties.keys())}') #Performs a join of the keys separated by commas
        answer = input('Choose the difficulty: ').strip().lower() # strip().lower() converts the character to lowercase
        game_speed = difficulties.get(answer)
        if game_speed is not None:
            return game_speed
        print('Invalid Input!')

if __name__ == '__main__':  
    curses.wrapper(game_loop, game_speed = select_difficulty())
