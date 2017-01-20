#-------------------------------------------------------------------------------
# squash.py - in-class demonstration of program design
# two player mode p1 up = w and down = s p2 up = Up down = Down
#-------------------------------------------------------------------------------
from graphics import *
from time import sleep
import winsound
import random

#constants
wallThickness = 0.05
batWidth = 0.15
batX = 0.85
batThickness = 0.05
ballRadius = 0.02

def main():
    game, colour = gameMode()
    court = makeCourt(game)
    ball = makeBall(court, "red")
    bat = makeBat(court, colour)
    if game == "two":
        bat2 = makeBat2(court)
        playTwoPlayer(court, ball, bat, bat2)
    elif game == "never":
        playNeverEndGame(court, ball, bat)
    elif game == "solo":
        playSoloMode(court, ball, bat)
    elif game == "npc":
        bat2 = makeBat2(court)
        playNPC(court, ball, bat, bat2)
    elif game == "power":
        playPowerMode(court, ball, bat)

        

def gameMode():
    win = GraphWin("game mode",500,300)
    for i in range(100,401,100):
        line = Line(Point(i,0), Point(i,300))
        line.draw(win)
    powers = Text(Point(450,150), "power mode")
    powers.setSize(8)
    powers.draw(win)
    npc = Text(Point(350,150), "player vs NPC")
    npc.setSize(8)
    npc.draw(win)
    never = Text(Point(250,150), "Time mode")
    never.setSize(8)
    never.draw(win)
    solo = Text(Point(150,150), "Solo mode")
    solo.setSize(8)
    solo.draw(win)
    two = Text(Point(50,150), "Two player mode")
    two.setSize(8)
    two.draw(win)
    colour = Entry(Point(150,50),10)
    colour.setText("blue")
    while True:
        mosue = win.getMouse()
        if (mosue.getX() >100 and mosue.getX()<200) and mosue.getY() < 50:
            colour.draw(win)
        elif mosue.getX() > 400:
            game = "power"
            break
        elif mosue.getX() > 300:
            game = "npc"
            break
        elif mosue.getX() > 200:
            game = "never"
            break
        elif mosue.getX() >100:
            game = "solo"
            break
        else:
            game = "two"
            break
    win.close()
    return game, colour.getText()

def control(win):
    message = Text(Point(0.5,0.9), \
    "what key do you want to use for up? click when done")
    message.draw(win)
    up = Entry(Point(0.5,0.8),10)
    up.draw(win)
    win.getMouse()
    up.undraw()
    message.setText("what key do you want to use for down? click when done")
    down = Entry(Point(0.5,0.8),10)
    down.draw(win)
    win.getMouse()
    down.undraw()
    message.undraw()
    return up.getText(), down.getText()
            
def makeCourt(game):
    court = GraphWin("Squash", 600, 600)
    court.setCoords(0, 0, 1, 1)
    drawRectangle(court, Point(0, 0), Point(1, wallThickness), "black")
    drawRectangle(court, Point(0, 1), Point(1, 1 - wallThickness), "black")
    if game == "never" or game == "solo" or game == "power":
        drawRectangle(court, Point(0, wallThickness), Point(wallThickness, 1-wallThickness), "black")
    return court
    
def makeBall(court, colour):
    ball = drawCircle(court, Point(0.5, 0.5), ballRadius, colour)
    return ball
    
def makeBat(court, colour):
    bat = drawRectangle(court, Point(batX, 0.5-batWidth/2),
                        Point(batX+batThickness, 0.5+batWidth/2), colour)
    return bat
    
def makeBat2(court):
    bat = drawRectangle(court, Point(1-batX, 0.5-batWidth/2),
                        Point((1-batX)+batThickness, 0.5+batWidth/2), "black")
    return bat

def checkBallHitWall(ball, speedX, speedY):
    centre = ball.getCenter()
    if centre.getX() - ballRadius <= wallThickness:
        speedX = -speedX
        winsound.PlaySound("pong.wav", winsound.SND_ASYNC)
    if centre.getY() + ballRadius >= 1 - wallThickness or \
       centre.getY() - ballRadius <= wallThickness:
        speedY  = -speedY
        winsound.PlaySound("pong.wav", winsound.SND_ASYNC)
    return speedX, speedY

def checkBallHitBat(ball, bat, speedX, speedY):
    ballCentre = ball.getCenter()
    ballX = ballCentre.getX() + ballRadius
    ballY = ballCentre.getY()
    topBat = bat.getP2().getY()
    botBat = bat.getP1().getY()
    frontBat = bat.getP1().getX()
    
    if (ballX >= frontBat and ballX <= frontBat + speedX and \
    ballY + ballRadius >= botBat and ballY - ballRadius <= topBat):
        speedX = -speedX
        import random
        speedY = random.random() * 0.0001 - 0.00005
        winsound.PlaySound("pong.wav", winsound.SND_ASYNC)
    return speedX, speedY
    
def checkMoveBat(court, bat, up, down):
    key = court.checkKey()
    batCentre = bat.getCenter()
    if (batCentre.getY() + batWidth) > (1):
        bat.move(0, -0.01)
    elif (batCentre.getY() - batWidth) < (0):
        bat.move(0, 0.01)
    elif key == up:
        bat.move(0, 0.08)
    elif key == down:
        bat.move(0, -0.08)

def drawRectangle(win, point1, point2, colour):
    rectangle = Rectangle(point1, point2)
    rectangle.setFill(colour)
    rectangle.setOutline(colour)
    rectangle.draw(win)  
    return rectangle  
    
def drawCircle(win, centre, radius, colour):
    circle = Circle(centre, radius)
    circle.setFill(colour)
    circle.setOutline(colour)
    circle.draw(win) 
    return circle

def playNeverEndGame(court, ball, bat):
    up, down = control(court)
    text = Text(Point(0.5,0.8), \
    "enter a difficulty level from 1 being slow and 10 being fast")
    text.draw(court)
    level = Entry(Point(0.5,0.6),10)
    level.draw(court)
    while True:
        court.getMouse()
        if eval(level.getText()) >=1 and eval(level.getText()) <=10:
            text.undraw()
            level.undraw()
            speedMult = eval(level.getText())
            break
        else:
            text.setText("invalid number. enter difficulty level from 1 being slow and 10 being fast") 
    sleep(1)
    timeBox = Text(Point(0.5,0.9),"")
    timeBox.draw(court)
    time = 0
    speedX = -0.00004 * speedMult
    speedY = 0.00000 * speedMult
    while True:
        centre = ball.getCenter()
        speedX, speedY = checkBallHitWall(ball, speedX, speedY)
        speedX, speedY = checkBallHitBat(ball, bat, speedX, speedY)
        checkMoveBat(court, bat, up, down)
        ball.move(speedX, speedY)
        time = time + 0.00025
        if centre.getX() > 1:
            ball.undraw()
            ball = makeBall(court, "red")
            speedX = -0.00004 * speedMult
            speedY = 0.00000 * speedMult
            time = int(time)
            timeBox.setText(("you lasted", time, "seconds"))
            time = 0
            sleep(1)
    court.close()
    
    
def playTwoPlayer(court, ball, bat, bat2):
    text = Text(Point(0.5,0.8),\
    "enter a difficulty level from 1 being normal and 5 being fast. click when done")
    text.draw(court)
    level = Entry(Point(0.5,0.6),10)
    level.draw(court)
    while True:
        court.getMouse()
        if eval(level.getText()) >=1 and eval(level.getText()) <=5:
            text.undraw()
            level.undraw()
            speedMult = eval(level.getText())+5
            break
        else:
            text.setText("invalid number. enter difficulty level from 1 being normal and 5 being fast") 
    sleep(1)
    speedX = -0.00004 * speedMult
    speedY = 0.00000 * speedMult
    p1score = 0
    p2score = 0
    p1ScoreBox = Text(Point(0.1,0.8),p1score)
    p1ScoreBox.draw(court)
    p2ScoreBox = Text(Point(0.9,0.8),p2score)
    p2ScoreBox.draw(court)
    while gameOver(p1score, p2score):
        centre = ball.getCenter()
        speedX, speedY = checkBallHitWall2(ball, speedX, speedY)
        speedX, speedY = checkBallHitBat(ball, bat, speedX, speedY)
        speedX, speedY = checkBallHitBat2(ball, bat2, speedX, speedY)
        checkMoveBat1(court, bat, bat2)
        ball.move(speedX, speedY)
        if ball.getCenter().getX() > 1 or ball.getCenter().getX() < 0:
            ball.undraw()
            if ball.getCenter().getX() > 1:
                p1score = p1score + 1
                p1ScoreBox.setText(p1score)
                ball = makeBall(court, "red")
            elif ball.getCenter().getX() < 0:
                p2score = p2score + 1
                p2ScoreBox.setText(p2score)
                ball = makeBall(court, "red")
            sleep(1)
            speedX = speedX
            speedY = 0.00000 * speedMult
    if p1score > p2score:
        winner = "player 1"
    else:
        winner = "player 2"
    game = Text(Point(0.5, 0.9), "Game over and the winner is")
    result = Text(Point(0.5,0.8), winner)
    game.draw(court)
    result.draw(court)
    result.setSize(25)
    winsound.PlaySound("win.wav", winsound.SND_ASYNC)
    sleep(10)
    court.close()
            
def gameOver(p1,p2):
    if (p1 >=  6 and p1 >= p2+2) or (p2 >=  6 and p2 >= p1+2):
        return False
    else:
        return True

def checkMoveBat1(court, bat1, bat2):
    key = court.checkKey()
    batCentre1 = bat1.getCenter()
    batCentre2 = bat2.getCenter()
    if (batCentre1.getY() + batWidth) > (1):
        bat1.move(0, -0.01)
    elif (batCentre1.getY() - batWidth) < (0):
        bat1.move(0, 0.01)
    elif key == "Up":
        bat1.move(0, 0.08)
    elif key == "Down":
        bat1.move(0, -0.08)
    elif (batCentre2.getY() + batWidth) > (1):
        bat2.move(0, -0.01)
    elif (batCentre2.getY() - batWidth) < (0):
        bat2.move(0, 0.01)
    elif key == "w":
        bat2.move(0, 0.08)
    elif key == "s":
        bat2.move(0, -0.08)

def checkBallHitBat2(ball, bat, speedX, speedY):
    ballCentre = ball.getCenter()
    ballX = ballCentre.getX() - ballRadius
    ballY = ballCentre.getY()
    topBat = bat.getP2().getY()
    botBat = bat.getP1().getY()
    frontBat = bat.getP2().getX()
    
    if (ballX <= frontBat and ballX >= frontBat + speedX and \
    ballY >= botBat and ballY <= topBat) or (ballX <= frontBat and ballX >= frontBat + speedX and \
    ballY + ballRadius >= botBat and ballY - ballRadius <= topBat):
        speedX = -speedX
        import random
        speedY = random.random() * 0.0001 - 0.00005
        winsound.PlaySound("pong.wav", winsound.SND_ASYNC)
    return speedX, speedY
        
def checkBallHitWall2(ball, speedX, speedY):
    centre = ball.getCenter()
    if centre.getY() + ballRadius >= 1 - wallThickness or \
       centre.getY() - ballRadius <= wallThickness:
        speedY  = -speedY
        winsound.PlaySound("pong.wav", winsound.SND_ASYNC)
    return speedX, speedY
    

def playSoloMode(court, ball, bat):
    up, down = control(court)
    sleep(1)
    score = 0
    scoreBox = Text(Point(0.2,0.9), ("Points:", score))
    scoreBox.draw(court)
    speedY = 0.00000
    for level in range(1,11,1):
        speedX = -0.00004 * level
        speedY = 0.00000
        while not soloOver(score, level, ball):
            centre = ball.getCenter()
            speedX, speedY = checkBallHitWall(ball, speedX, speedY)
            speedX, speedY, score = checkBallHitBatSolo(ball, bat, speedX, speedY, score, scoreBox)
            checkMoveBat(court, bat, up, down)
            ball.move(speedX, speedY)
            if centre.getX() > 1:
                ball.undraw()
        if ball.getCenter().getX() > 1:
            over = Text(Point(0.5,0.9), "Game Over") 
            over.setSize(25)
            over.draw(court)
            winLose = Text(Point(0.5,0.8), "You Loss") 
            winLose.setSize(25)
            winLose.draw(court)
            sleep(2)
            court.close()
        elif score == 100:
            over = Text(Point(0.5,0.9), "Game Over") 
            over.setSize(25)
            over.draw(court)
            winLose = Text(Point(0.5,0.8), "You Win") 
            winLose.setSize(25)
            winLose.draw(court)
            winsound.PlaySound("win.wav", winsound.SND_ASYNC)
            sleep(2)
            court.close()
        else:
            over = Text(Point(0.5,0.9), ("level:", level, "completed")) 
            over.setSize(25)
            over.draw(court)
            winsound.PlaySound("win.wav", winsound.SND_ASYNC)
            sleep(2)
            over.undraw()
 
def checkBallHitBatSolo(ball, bat, speedX, speedY, score, scoreBox):
    ballCentre = ball.getCenter()
    ballX = ballCentre.getX() + ballRadius
    ballY = ballCentre.getY()
    topBat = bat.getP2().getY()
    botBat = bat.getP1().getY()
    frontBat = bat.getP1().getX()
    
    if (ballX >= frontBat and ballX <= frontBat + speedX and \
    ballY >= botBat and ballY <= topBat) or (ballX >= frontBat and ballX <= frontBat + speedX and \
    ballY + ballRadius >= botBat and ballY - ballRadius <= topBat):
        speedX = -speedX
        import random
        speedY = random.random() * 0.0001 - 0.00005
        winsound.PlaySound("pong.wav", winsound.SND_ASYNC)
        score = score + 1
        scoreBox.setText(("Points:",score))
    return speedX, speedY, score
            
def soloOver(score, level, ball):
    return score == 10 * level or ball.getCenter().getX() > 1


def playNPC(court, ball, bat, bat2):
    up, down = control(court)
    text = Text(Point(0.5,0.8),\
    "enter a difficulty level from 1 being normal and 5 being fast. click when done")
    text.draw(court)
    level = Entry(Point(0.5,0.6),10)
    level.draw(court)
    while True:
        court.getMouse()
        if eval(level.getText()) >=1 and eval(level.getText()) <=5:
            text.undraw()
            level.undraw()
            speedMult = eval(level.getText()) + 5
            break
        else:
            text.setText("invalid number. enter difficulty level from 1 being normal and 5 being fast") 
    sleep(1)
    speedX = -0.00004 * speedMult
    speedY = 0.00000 * speedMult
    p1score = 0
    p2score = 0
    p1ScoreBox = Text(Point(0.1,0.8),p1score)
    p1ScoreBox.draw(court)
    p2ScoreBox = Text(Point(0.9,0.8),p2score)
    p2ScoreBox.draw(court)
    while gameOver(p1score, p2score):
        centre = ball.getCenter()
        speedX, speedY = checkBallHitWall2(ball, speedX, speedY)
        speedX, speedY = checkBallHitBat(ball, bat, speedX, speedY)
        speedX, speedY = checkBallHitBat2(ball, bat2, speedX, speedY)
        checkMoveBat3(court, bat, bat2, ball,speedY, up, down)
        ball.move(speedX, speedY)
        if ball.getCenter().getX() > 1 or ball.getCenter().getX() < 0:
            ball.undraw()
            if ball.getCenter().getX() > 1:
                p1score = p1score + 1
                p1ScoreBox.setText(p1score)
                ball = makeBall(court, "red")
            elif ball.getCenter().getX() < 0:
                p2score = p2score + 1
                p2ScoreBox.setText(p2score)
                ball = makeBall(court, "red")
            sleep(1)
            speedX = speedX
            speedY = 0.00000 * speedMult
    if p1score > p2score:
        winner = "the NPC"
    else:
        winner = " the player"
    game = Text(Point(0.5, 0.9), "Game over and the winner is")
    result = Text(Point(0.5,0.8), winner)
    game.draw(court)
    result.draw(court)
    result.setSize(25)
    winsound.PlaySound("win.wav", winsound.SND_ASYNC)
    sleep(10)
    court.close()
            

def checkMoveBat3(court, bat1, bat2, ball,speedY, up, down):
    key = court.checkKey()
    batCentre1 = bat1.getCenter()
    batCentre2 = bat2.getCenter()
    ballCentre = ball.getCenter()
    if (batCentre1.getY() + batWidth) > (1):
        bat1.move(0, -0.01)
    elif (batCentre1.getY() - batWidth) < (0):
        bat1.move(0, 0.01)
    elif key == up:
        bat1.move(0, 0.08)
    elif key == down:
        bat1.move(0, -0.08)
    if (batCentre2.getY() + batWidth) > (1):
        bat2.move(0, -0.01)
    elif (batCentre2.getY() - batWidth) < (0):
        bat2.move(0, 0.01)
    elif batCentre2.getY() >0.5 and speedY == 0 :
        bat2.move(0, -0.00007)
    elif batCentre2.getY() <0.5 and speedY == 0:
        bat2.move(0, 0.00007)
    elif batCentre2.getY() < ballCentre.getY() and speedY > 0:
        bat2.move(0, 0.000013)
    elif batCentre2.getY() > ballCentre.getY() and speedY > 0:
        bat2.move(0, -0.000013)
    elif batCentre2.getY() > ballCentre.getY() and speedY < 0:
        bat2.move(0, -0.000013)

def playPowerMode(court, ball, bat):
    up, down = control(court)
    sleep(1)
    score = 0
    scoreBox = Text(Point(0.2,0.9), ("Points:", score))
    scoreBox.draw(court)
    speedY = 0.00000
    for level in range(1,11,1):
        speedX = -0.00004 * level
        speedY = 0.00000
        speedX2 = -0.00004 * level
        speedY2 = 0.00000
        power = 0
        while not powerOver(score, level, ball):
            if power == 0:
                powerBall = random.random()
                if powerBall < 0.000035:
                    ball2 = makeBall(court, "green")
                    power = 1
                elif powerBall > 0.9997:
                    ball3 = makeBall(court, "black")
                    power = 5
            centre = ball.getCenter()
            if power == 5:
                speedX, speedY = checkBallHitWall(ball, speedX, speedY)
                speedX, speedY, score = checkBallHitBatSolo(ball, bat, speedX, speedY, score, scoreBox)
                power = checkBallHitBatPower(ball3, power, bat, level)
                checkMoveBat(court, bat, up, down)
                ball.move(speedX, speedY)
                ball3.move(0.00004 * level, speedY)
                if power == 2:
                    speedX = speedX*2
                    speedX2 = speedX2*2
                    power = 0
            elif power == 1:
                speedX, speedY = checkBallHitWall(ball, speedX, speedY)
                speedX, speedY, score = checkBallHitBatSolo(ball, bat, speedX, speedY, score, scoreBox)
                power = checkBallHitBatPower(ball2, power, bat, level)
                checkMoveBat(court, bat, up, down)
                ball.move(speedX, speedY)
                ball2.move(0.00004 * level, speedY)
            elif power == 2:
                ball2 = makeBall(court, "red")
                power = 3
                centre2 = ball2.getCenter()
            elif power == 3:
                centre2 = ball2.getCenter()
                speedX, speedY = checkBallHitWall(ball, speedX, speedY)
                speedX2, speedY2 = checkBallHitWall(ball2, speedX2, speedY2)
                speedX, speedY, score = checkBallHitBatSolo(ball, bat, speedX, speedY, score, scoreBox)
                speedX2, speedY2, score = checkBallHitBatSolo(ball2, bat, speedX2, speedY2, score, scoreBox)
                checkMoveBat(court, bat, up, down)
                ball.move(speedX, speedY)
                ball2.move(speedX2, speedY2)
            elif power == 4:
                centre2 = ball2.getCenter()
                speedX2, speedY2 = checkBallHitWall(ball2, speedX2, speedY2)
                speedX2, speedY2, score = checkBallHitBatSolo(ball2, bat, speedX2, speedY2, score, scoreBox)
                checkMoveBat(court, bat, up, down)
                ball2.move(speedX2, speedY2)
                if centre2.getX() > 1:
                    break
            else:
                speedX, speedY = checkBallHitWall(ball, speedX, speedY)
                speedX, speedY, score = checkBallHitBatSolo(ball, bat, speedX, speedY, score, scoreBox)
                checkMoveBat(court, bat, up, down)
                ball.move(speedX, speedY)
            if power == 0:
                if centre.getX() > 1:
                    break
            if power == 3:
                if centre2.getX() > 1 and centre.getX() > 1:
                    break
                elif centre2.getX() > 1:
                    ball2.undraw()
                    power = 0
                elif centre.getX() > 1:
                    ball.undraw()
                    power = 4
        if power == 5:
            ball3.undraw()
        if power == 4:
            if ball2.getCenter().getX() > 1:
                over = Text(Point(0.5,0.9), "Game Over") 
                over.setSize(25)
                over.draw(court)
                winLose = Text(Point(0.5,0.8), "You Loss") 
                winLose.setSize(25)
                winLose.draw(court)
                sleep(2)
                court.close() 
            else:
                over = Text(Point(0.5,0.9), ("level:", level, "completed")) 
                over.setSize(25)
                over.draw(court)
                winsound.PlaySound("win.wav", winsound.SND_ASYNC)
                if power == 3 :
                    ball2.undraw()
                if power == 4:
                    ball = makeBall(court, "red")
                    ball2.undraw()
                sleep(2)
                over.undraw()
        elif ball.getCenter().getX() > 1:
            over = Text(Point(0.5,0.9), "Game Over") 
            over.setSize(25)
            over.draw(court)
            winLose = Text(Point(0.5,0.8), "You Loss") 
            winLose.setSize(25)
            winLose.draw(court)
            sleep(2)
            court.close()
        elif score == 100:
            over = Text(Point(0.5,0.9), "Game Over") 
            over.setSize(25)
            over.draw(court)
            winLose = Text(Point(0.5,0.8), "You Win") 
            winLose.setSize(25)
            winLose.draw(court)
            winsound.PlaySound("win.wav", winsound.SND_ASYNC)
            sleep(2)
            court.close()
        else:
            over = Text(Point(0.5,0.9), ("level:", level, "completed")) 
            over.setSize(25)
            over.draw(court)
            winsound.PlaySound("win.wav", winsound.SND_ASYNC)
            if power == 3 :
                ball2.undraw()
            if power == 4:
                ball = makeBall(court, "red")
                ball2.undraw()
            sleep(2)
            over.undraw()
 
def checkBallHitBatPower(ball, power, bat, level):
    ballCentre = ball.getCenter()
    ballX = ballCentre.getX() + ballRadius
    ballY = ballCentre.getY()
    topBat = bat.getP2().getY()
    botBat = bat.getP1().getY()
    frontBat = bat.getP1().getX()
    
    if (ballX >= frontBat and ballX <= frontBat + 0.00004 * level and \
    ballY + ballRadius >= botBat and ballY - ballRadius <= topBat):
        ball.undraw()
        power = 2
    if ballCentre.getX() > 1:
        power = 0
        ball.undraw()
    return power
    


def powerOver(score, level, ball):
    return score == 10 * level


main()



