import turtle
import random
from time import time


screen = None
pen = None
monster = None
snake = None		
isMoving = False
pauseGame = False
stampID = []
stampPosition = []
foodList = []
isEaten = [False]*9
bodyLength = 5
contact = 0


#details part (including intialize and upadte the screen, check the game status(over), count the contact and user interaction)
#initialize the screen
def setScreen(width = 500,height = 500):
    global screen,pen
    screen = turtle.Screen()
    screen.setup(width,height)		#set the screen to be 500*500
    screen.title('Snake    Designed by CC')
    pen = turtle.Turtle()
    pen.up()
    pen.hideturtle()
    pen.goto(-230,120)
    pen.write('Welcome to play the Snake designed by CC. \n\nYou are supposed to use the 4 arrow keys to move the snake\naround the screen. When you press "space", the snake will\nstop moving. If you click again, it will start moving. \nTry to consume all the food before the monster catch you.\n\nClick anywhere on the screen to start the game.',font='aerial 10 bold')
    screen.tracer(0)		#close the automatic refresh
    return screen

#update the title and screen
def update():
    currentTime = time()		#get the time of the current status
    runTime = currentTime - startTime		#calculate how many time has used
    contactNum = countContact()		#get the contact number
    screen.title('Snake  Contacted:'+ str(int(contactNum))+'   Time:'+ str(int(runTime)))
    screen.update()

#game status
def gameOver():		#check the distance between monster and snake head, if the distance is too small, then you lose
    return abs(snake.xcor()-monster.xcor()) < 20 and abs(snake.ycor()-monster.ycor()) < 20

#count the contact
def countContact():
	global contact
	for i in stampPosition:		#calulate the distance between snake body and monster
		if abs(monster.xcor() - i[0]) < 20 and abs(monster.ycor() - i[1]) < 20:
			contact +=1		#if they overlap, contact will + 1
		else: 
			pass
	return contact

#configure the key
def configureKey():
	screen.onkey(snakeUp,'Up')	
	screen.onkey(snakeDown,'Down')
	screen.onkey(snakeLeft,'Left')
	screen.onkey(snakeRight,'Right')
	screen.onkey(changeStatus,'space')

#onclick
def onClick(x,y):
    global startTime
    pen.clear()		#clear the instruction on the screen
    pen.up()		#hide the pen
    startTime = time()		#get the starting time
    configureKey()		#correspond each function with the keyboard
    setFood()		#set the food on the screen
    screen.title('Snake  Contacted: 0   Time: 0')		#initialize the title
    moveMonster()		#start automatically move the monster
    screen.onclick(None)


#monster part
#define the heading direction of the monster
def monsterHeading():		#calculate the distance of x and y, then deside the heading direction of the monster
    distanceX = snake.xcor() - monster.xcor()
    distanceY = snake.ycor() - monster.ycor()
    if distanceX >= 0 and distanceY >= 0:
        if abs(distanceX) >= abs(distanceY):
            heading = 0
        else:
            heading = 90
    elif distanceX >= 0 and distanceY < 0:
        if abs(distanceX) >= abs(distanceY):
            heading = 0
        else:
            heading = 270
    elif distanceX < 0 and distanceY >= 0:
        if abs(distanceX) >= abs(distanceY):
            heading = 180
        else:
            heading = 90
    else:
        if abs(distanceX) >= abs(distanceY):
            heading = 180
        else:
            heading = 270
    return heading

#automatically move the monster
def moveMonster():
    global pauseGame
    if gameOver() == True:		#if game over, write game over and stop moving
        pen.goto((-50,0))
        pen.color('red')
        pen.write('Game Over',font='aerial 20 bold')
    elif pauseGame == True:
        pass
    else:
        if len(stampID) == 50: 		#if snake has consumed all the food, write winner
            pen.goto((-50,0))
            pen.color('red')
            pen.write('WINNER',font='aerial 20 bold')
        else:		#if nothing happen (in the common status)
            monster.setheading(monsterHeading())		#set the heading of monster
            monster.forward(20)		#monster move forward
    update()
    speed = random.randint(380,600)		#make sure the monster is moving slower or slightly faster than the snake randomly
    screen.ontimer(moveMonster,speed)		#automatically move


#snake part
#status of the snake (heading direction & pause/un-pause)
def snakeUp():
    snake.setheading(90)
    if isMoving == False:		#make sure the snake will not set up too much ontimer function, which will make it move faster and faster
        moveSnake()

def snakeDown():
    snake.setheading(270)
    if isMoving == False:
        moveSnake()	

def snakeLeft():
    snake.setheading(180)
    if isMoving == False:
        moveSnake()

def snakeRight():
    snake.setheading(0)
    if isMoving == False:
        moveSnake()

def changeStatus():
	global pauseGame
	pauseGame = not pauseGame		#change the moving/un-moving status
	if pauseGame ==  False:
		moveSnake()
	return pauseGame

#extend the snake
def extend():
    snakeColor = snake.color()		#get the snake head color
    snake.color('green','orange')		#change the color for body(stamp)
    stampID.append(snake.stamp())		#stamp and also append its ID to the list
    stampPosition.append(snake.position())		#append its coordinates to the location list
    snake.color(*snakeColor)		#change back the color of the snake
    snake.forward(20)		#move forward to achieve the extend

#check whether the snake is movable or not (in case it moves outside the screen)
def movable(x=230):
	global isMoving
	if snake.heading() == 0  and snake.xcor() > x:		#if it hit the wall, stop moving
		isMoving = False
		return False
	if snake.heading() == 90 and snake.ycor() > x:
		isMoving = False
		return False
	if snake.heading() == 180 and snake.xcor() < -x:
		isMoving = False
		return False
	if snake.heading() == 270 and snake.ycor() < -x:
		isMoving = False
		return False
	return True		#if the player change the direction, it can start moving

#move snake function (set the heading of the snake, extend and move)
def moveSnake():
	global isMoving,bodyLength 
	if gameOver() == False and pauseGame == False and movable() == True and len(stampID) != 50:		#in the common status, it can start moving
		isMoving = True
		bodyLength = updateSnakeLength(bodyLength)		#get the current body length
		if len(stampID) < bodyLength :		#decide to extend or simply move the body
			extend()
			screen.ontimer(moveSnake,500)		#when extending, slow down the speed
		else:
			extend()
			snake.clearstamp(stampID[0])		
			stampID.pop(0)
			stampPosition.pop(0)
			screen.ontimer(moveSnake,400)
	update()


#food part
#set the food location
def setFood():
    global foodList
    for i in range(9):
        foodList.append(turtle.Turtle(visible=False))		#use invisible turtle to set the food
    for i in range(0,len(foodList)):
        foodList[i].up()
        foodList[i].goto((random.randint(-230,230),random.randint(-230,230)))
        for j in range (0,i):		#make sure food is far away from each other
            while abs(foodList[i].xcor()-foodList[j].xcor()) <= 50 and abs(foodList[i].ycor()-foodList[j].ycor()) <= 50:
                foodList[i].goto((random.randint(-230,230),random.randint(-230,230)))
        foodList[i].write(str(i+1),  font="aerial 12 bold")		#write down the number to reprensent food

#consume the food and update the body length of the snake
def updateSnakeLength(bodyLength):
    for i in range(0,len(foodList)):
        if snake.distance(foodList[i])<=15 and isEaten[i]==False:		#if the food is consumed
            isEaten[i]=True		#mark its data to has being eaten
            bodyLength=bodyLength+i+1		#update the body length
            foodList[i].clear()		#clear the food on the screen
            return bodyLength
    return bodyLength


#mainloop function
if __name__ == "__main__":
	#set the snake
	snake=turtle.Turtle('square')
	snake.up()
	snake.color('red')
	#set the monster
	monster=turtle.Turtle('square')
	monster.penup()
	monster.color('black','purple')
	monster.setposition(-200,-200)
	#initialize the screen
	setScreen()
	screen.onclick(onClick)
	screen.listen()
	screen.mainloop()