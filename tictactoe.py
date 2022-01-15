#import modules
import pygame
import numpy as np
import pickle
import itertools
from pygame.locals import *
np.seterr(divide='ignore', invalid='ignore')
pygame.init()

screen_height = 300
screen_width = 300
line_width = 6
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tic Tac Toe')



#define colours
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#define font
font = pygame.font.SysFont(None, 40)

#define variables
clicked = False
player = 1
pos = (0,0)
markers = []
game_over = False
winner = 0

#setup a rectangle for "Play Again" Option
again_rect = Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)

#create empty 3 x 3 list to represent the grid
for x in range (3):
	row = [0] * 3
	markers.append(row)



def draw_board():
	bg = (255, 255, 210)
	grid = (50, 50, 50)
	screen.fill(bg)
	for x in range(1,3):
		pygame.draw.line(screen, grid, (0, 100 * x), (screen_width,100 * x), line_width)
		pygame.draw.line(screen, grid, (100 * x, 0), (100 * x, screen_height), line_width)

def draw_markers():
	x_pos = 0
	for x in markers:
		y_pos = 0
		for y in x:
			if y == 1:
				pygame.draw.line(screen, red, (x_pos * 100 + 15, y_pos * 100 + 15), (x_pos * 100 + 85, y_pos * 100 + 85), line_width)
				pygame.draw.line(screen, red, (x_pos * 100 + 85, y_pos * 100 + 15), (x_pos * 100 + 15, y_pos * 100 + 85), line_width)
			if y == -1:
				pygame.draw.circle(screen, green, (x_pos * 100 + 50, y_pos * 100 + 50), 38, line_width)
			y_pos += 1
		x_pos += 1	


def check_game_over(markers = markers):
	global game_over
	global winner

	x_pos = 0
	for x in markers:
		#check columns
		if sum(x) == 3:
			winner = 1
			game_over = True
		if sum(x) == -3:
			winner = 2
			game_over = True
		
		#check rows
		if markers[0][x_pos] + markers [1][x_pos] + markers [2][x_pos] == 3:
			winner = 1
			game_over = True
		if markers[0][x_pos] + markers [1][x_pos] + markers [2][x_pos] == -3:
			winner = 2
			game_over = True
		x_pos += 1

	#check cross
	if markers[0][0] + markers[1][1] + markers [2][2] == 3 or markers[2][0] + markers[1][1] + markers [0][2] == 3:
		winner = 1
		game_over = True
	if markers[0][0] + markers[1][1] + markers [2][2] == -3 or markers[2][0] + markers[1][1] + markers [0][2] == -3:
		winner = 2
		game_over = True

	#check for tie
	if game_over == False:
		tie = True
		for row in markers:
			for i in row:
				if i == 0:
					tie = False
		#if it is a tie, then call game over and set winner to 0 (no one)
		if tie == True:
			game_over = True
			winner = 0



def draw_game_over(winner):

	if winner != 0:
		end_text = "Player " + str(winner) + " wins!"
	elif winner == 0:
		end_text = "You have tied!"

	end_img = font.render(end_text, True, blue)
	pygame.draw.rect(screen, green, (screen_width // 2 - 100, screen_height // 2 - 60, 200, 50))
	screen.blit(end_img, (screen_width // 2 - 100, screen_height // 2 - 50))

	again_text = 'Play Again?'
	again_img = font.render(again_text, True, blue)
	pygame.draw.rect(screen, green, again_rect)
	screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 10))


def check_game_over_2(x):
		y = x.copy()
		y = np.array(y).reshape(3,3)
		y[np.where(y==2)] = -1
		# check for game over
		game_over = False
		check_game_over(y)

''' Defining STATE SPACE and required parameters'''

states_0 = [[0]*9]

states_1 = []
board_pos = [i for i in range(9)]
for i in board_pos:
  for j in board_pos:
    if i!=j:
      x = [0]*9
      x[i] = 1
      x[j] = 2
      states_1.append(x)

# states_2
states_2 = []
for s in states_1:
  indices = [i for i, x in enumerate(s) if x == 1 or x == 2]
  board_pos = [i for i in range(9)]
  board_pos = list(set(board_pos) - set(indices))
  for i in board_pos:
    for j in board_pos:
      if i!=j:
        x = s.copy()
        x[i] = 1
        x[j] = 2
        if x not in states_2:
          states_2.append(x)

# states_3
TERMINAL_STATES = []
states_3 = []
for s in states_2:
  indices = [i for i, x in enumerate(s) if x == 1 or x == 2]
  board_pos = [i for i in range(9)]
  board_pos = list(set(board_pos) - set(indices))
  # print(len(board_pos))
  for i in board_pos:
    for j in board_pos:
      if i!=j:
        x = s.copy()
        # print(x,i,j)
        x[i] = 1
        # y = x.copy()
        # y = np.array(y).reshape(3,3)
        # y[np.where(y==2)] = -1
        # # check for game over
        game_over = False
        check_game_over_2(x)
        # if game is over then state_3.append(x) else
        if(game_over == True):
          # print("matrix\n",y)
          if x not in TERMINAL_STATES:
            TERMINAL_STATES.append(x)
            break
        else:
          x[j] = 2
          if x not in states_3:
            states_3.append(x)

# states_4
states_4 = []
# check for the
for s in states_3:
  indices = [i for i, x in enumerate(s) if x == 1 or x == 2]
  board_pos = [i for i in range(9)]
  board_pos = list(set(board_pos) - set(indices))
  for i in board_pos:
    for j in board_pos:
      if i!=j:
        x = s.copy()
        x[i] = 1
        x[j] = 2
        if x not in states_4:
          states_4.append(x)
'''
with open('states-new.data', 'rb') as filehandle:
    # read the data as binary data stream
    STATES = pickle.load(filehandle)
'''
# STATES = states_0+states_1+states_2+states_3+states_4+TERMINAL_STATES
ACTION_SPACE = [i for i in range(9)]

STATE_SPACE_SIZE = len(STATES)
ACTION_SPACE_SIZE = len(ACTION_SPACE)

transition_probability = np.array([[[0.0]*STATE_SPACE_SIZE]*ACTION_SPACE_SIZE]*STATE_SPACE_SIZE)


def generate_transition_prob():
  for i in range(STATE_SPACE_SIZE):
  	if STATES[i] in TERMINAL_STATES:
  		continue
  	for j in range(ACTION_SPACE_SIZE):
  		for k in range(STATE_SPACE_SIZE):
  			bd = STATES[i]
  			bd_2 = STATES[k]
  			if(bd[j] == 0 and bd_2[j]==1):
  				a = bd.copy()
  				a[j] = 1
  				game_over=False
  				check_game_over_2(a)
  				if game_over==True:
  					t_index = np.where((STATES==a).all(-1))[0][0]
  					transition_probability[i][j][t_index]=1.0
  				else:
  					check = np.subtract(bd_2,a)
  					if(np.sum(check)==2 and np.min(check)==0 and np.max(check)==2):
  						transition_probability[i][j][k] = np.random.randint(1,100,size=1)[0]


generate_transition_prob()

for i in range(STATE_SPACE_SIZE):
  for j in range(ACTION_SPACE_SIZE):
  	prob_sum = np.sum(transition_probability[i][j])
  	if prob_sum>0:
	    transition_probability[i][j] = transition_probability[i][j]/prob_sum
	    # print("sum=",np.sum(transition_probability[i][j]))
# print(transition_probability[0][2])

'''
STATES = np.asarray(STATES) 
with open('transition_prob.data', 'rb') as filehandle:
    # read the data as binary data stream
    transition_probability = pickle.load(filehandle)
##################################################

'''
#main loop
run = True
current_state = STATES[0]
ind = 0
while run:
	#draw board and markers first
	draw_board()
	draw_markers()
	
	#handle events
	for event in pygame.event.get():
		# print(markers)
		#handle game exit
		if event.type == pygame.QUIT:
			run = False
		#run new game
		if game_over == False:
			#check for mouseclick
			if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
				clicked = True
			if event.type == pygame.MOUSEBUTTONUP and clicked == True:
				clicked = False
				pos = pygame.mouse.get_pos()
				cell_x = pos[0] // 100 # cell_x = pos[0]
				cell_y = pos[1] // 100 # cell_y = pos[1]
				print("cell_x=",cell_x)
				print("cell_y=",cell_y)
				if markers[cell_x][cell_y] == 0:
					markers[cell_x][cell_y] = 1
					game_over=False
					check_game_over(markers)
						# draw_markers()
					if game_over == False:

						print("markers_1=",markers)

						print("ind=",ind)	
						y = np.random.choice(np.arange(STATE_SPACE_SIZE),1,p= transition_probability[ind][cell_x*3+cell_y])[0]
						
						print("index=",y)
						next_state = STATES[y].copy()
						current_state = next_state.copy()
						print("current_state = ", current_state)
						next_state[np.where(next_state==2)] = -1
						markers = next_state.reshape(3,3).tolist()
						print("markers_2-",markers)
						ind = np.where((STATES==current_state).all(-1))[0][0]
						# draw_markers()
						# player *= -1
					
						check_game_over(markers)

	#check if game has been won
	if game_over == True:
		current_state = STATES[0]
		ind = 0
		draw_game_over(winner)
		#check for mouseclick to see if we clicked on Play Again
		if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
			clicked = True
		if event.type == pygame.MOUSEBUTTONUP and clicked == True:
			clicked = False
			pos = pygame.mouse.get_pos()
			if again_rect.collidepoint(pos):
				#reset variables
				game_over = False
				player = 1
				pos = (0,0)
				markers = []
				winner = 0
				#create empty 3 x 3 list to represent the grid
				for x in range (3):
					row = [0] * 3
					markers.append(row)

	#update display
	pygame.display.update()

pygame.quit()
