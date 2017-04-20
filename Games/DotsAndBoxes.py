from tkinter import *

def init(data):
    data.cellsize = (data.width - 2*data.margin)/(data.dotCols-1)
    data.boxRows = data.dotRows -1
    data.boxCols = data.dotCols -1
    data.boxBoard = []
    data.player = []
    data.playerX = 0
    data.playerY = 0
    data.lines = []
    data.player1Score = 0
    data.player2Score = 0
    createBoxBoard(data)
    data.timeCounter = 0
    data.timeOut = False
    data.gameOver = False
########################### Helper function ###################################
#Create a board(2D List) to control the boxes ( when the number in the boxes 
# equal to 4, it means the box is ocuppied)
def createBoxBoard(data):
    data.boxBoard = [([0]*data.boxCols) for boxRow in range(data.boxRows)]

#To judge if the click is near a dot
def isLegalClick(data):
    for dotRow in range(data.dotRows):
        for dotCol in range(data.dotCols):
            dotX = data.margin+dotCol*data.cellsize
            dotY = data.margin+dotRow*data.cellsize
            if (data.playerX >= dotX - 5*data.dotRadius and \
            data.playerX <= dotX + 5*data.dotRadius) and \
            (data.playerY >= dotY - 5*data.dotRadius and \
                data.playerY <= dotY + 5*data.dotRadius):
                data.playerX = dotX
                data.playerY = dotY 
                return True
    return False

#To judge if two dots can be connected
def isLegalDot(data):
    if data.player ==[]:
        return True
    elif data.player !=[]:
        distance = ((data.playerX-data.player[0][0])**2\
        +(data.playerY-data.player[0][1])**2)**0.5
        if distance == data.cellsize:
            return True
        else:
            return False

#To judge if the connected line is existed
def isLegalLine(data):
    reversePlayer = []
    reversePlayer.append(data.player[1])
    reversePlayer.append(data.player[0])
    print(data.player)
    print(reversePlayer)
    if reversePlayer in data.lines or\
    data.player in data.lines:
        return False
    else:
        return True

# When a new line is created, trying to update the number in a box. When the 
# number in the box equals to 4, the box is ocuupied
def updateBoxBoard(data):
# Trying to use helper functions, but the logic is so tight that there is no 
#need to split it into different parts 
    firstDotRow = int((data.player[0][1] - data.margin)/data.cellsize)
    firstDotCol = int((data.player[0][0] - data.margin)/data.cellsize)
    secondDotRow = int((data.player[1][1] - data.margin)/data.cellsize)
    secondDotCol = int((data.player[1][0] - data.margin)/data.cellsize)
    if firstDotRow == secondDotRow: 
            dotRow = firstDotRow
            dotCol = min(firstDotCol,secondDotCol)
            firstBoxRow = dotRow-1
            secondBoxRow = dotRow
            firstBoxCol = dotCol
            secondBoxCol = dotCol
            if firstBoxRow < 0:
                data.boxBoard[secondBoxRow][secondBoxCol]+=1
            elif secondBoxRow >= data.boxRows:
                data.boxBoard[firstBoxRow][firstBoxCol]+=1
            else:
                data.boxBoard[firstBoxRow][firstBoxCol]+=1
                data.boxBoard[secondBoxRow][secondBoxCol]+=1
    elif firstDotCol == secondDotCol:
            dotRow = min(firstDotRow,secondDotRow)
            dotCol = firstDotCol
            firstBoxCol = dotCol-1
            secondBoxCol = dotCol
            firstBoxRow = dotRow
            secondBoxRow = dotRow
            if firstBoxCol < 0:
                data.boxBoard[secondBoxRow][secondBoxCol]+=1
            elif secondBoxCol >= data.boxCols:
                data.boxBoard[firstBoxRow][firstBoxCol]+=1
            else:
                data.boxBoard[firstBoxRow][firstBoxCol]+=1
                data.boxBoard[secondBoxRow][secondBoxCol]+=1
    data.player =[]

# check if the new created line is the fourth side of a box
def checkTheFourthSide(data):
    for boxRow in range(data.boxRows):
        for boxCol in range(data.boxCols):
            if data.boxBoard[boxRow][boxCol] == 4 and len(data.lines)%2==1:
                data.boxBoard[boxRow][boxCol] = 'Player1'
            elif data.boxBoard[boxRow][boxCol] == 4 and len(data.lines)%2==0:
                data.player2Score+=1
                data.boxBoard[boxRow][boxCol] = 'Player2'

# check if there is timeout
def checkTimeOut(data):
    if data.timeCounter%20==0:
        data.timeOut = True
        data.lines.append([(0,0),(0,0)])

# check if the game is over
def isGameOver(data):
    for boxRow in range(data.boxRows):
        for boxCol in range(data.boxCols):
            if data.boxBoard[boxRow][boxCol] != 'Player1'\
            and data.boxBoard[boxRow][boxCol] != 'Player2':
                return 
    data.gameOver = True

################################# Control #####################################
def mousePressed(event, data):
    data.timeCounter = 0
    data.playerX = event.x 
    data.playerY = event.y 
    if isLegalClick (data) and isLegalDot(data):
        data.player.append((data.playerX,data.playerY))
    if len(data.player) == 2 and isLegalLine(data):
        print(isLegalLine(data))
        data.lines.append(data.player)
        updateBoxBoard(data)
        checkTheFourthSide(data)
    elif len(data.player) ==2 and not isLegalLine(data):
        data.player.pop()

def keyPressed(event, data):
    if keysym == 'r':
        init(data)

def timerFired(data):
    if data.timeOut == True:
        data.timeOut = False
    data.timeCounter+=1
    if not data.gameOver:
        checkTimeOut(data)
    isGameOver(data)
###############################  View ########################################

def drawBackground(canvas,data):
    canvas.create_rectangle(0,0,data.width,data.height,fill='sea green')

def drawNodes(canvas,data):
    for dotRow in range(data.dotRows):
        for dotCol in range(data.dotCols):
            dotX = data.margin+dotCol*data.cellsize
            dotY = data.margin+dotRow*data.cellsize
            canvas.create_oval(dotX-data.dotRadius, dotY-data.dotRadius,\
                dotX+data.dotRadius,dotY+data.dotRadius,fill='black')

def drawLines(canvas,data):
    for i in range(len(data.lines)):
        firstX = data.lines[i][0][0]
        firstY = data.lines[i][0][1]
        secondX = data.lines[i][1][0]
        secondY = data.lines[i][1][1]
        if i%2 ==0:
            canvas.create_line(firstX, firstY, secondX, secondY,\
             fill='black', width = 2)
        elif i%2 ==1:
            canvas.create_line(firstX, firstY, secondX, secondY,\
             fill='red', width = 2)

def drawBoxBoard(canvas, data):
    for boxRow in range(data.boxRows):
        for boxCol in range(data.boxCols):
            if data.boxBoard[boxRow][boxCol] == 'Player1' \
            or data.boxBoard[boxRow][boxCol] == 'Player2': 
                topX = data.margin+boxCol*data.cellsize
                topY = data.margin+boxRow*data.cellsize
                bottomX = data.margin+(boxCol+1)*data.cellsize
                bottomY = data.margin+(boxRow+1)*data.cellsize
                centerX = (topX+bottomX)/2
                centerY = (topY+bottomY)/2
                canvas.create_text(centerX,centerY,\
                    text=data.boxBoard[boxRow][boxCol],fill='white',\
                    font="Helvetica 20 bold underline")

def drawScoreBoard(canvas,data):
    canvas.create_rectangle(1/5*data.width,5/7*data.height,4/5*data.width\
        ,6/7*data.height,fill='gray')
    canvas.create_text(1/3*data.width,5.4/7*data.height,text='Player1:',\
        fill='black',font="Helvetica 20 bold underline")
    canvas.create_text(2/3*data.width,5.4/7*data.height,text=data.player1Score,\
        fill='black',font="Helvetica 20 bold")
    canvas.create_text(1/3*data.width,5.8/7*data.height,text='Player2:',\
        fill='red',font="Helvetica 20 bold underline")
    canvas.create_text(2/3*data.width,5.8/7*data.height,text=data.player2Score,\
        fill='red',font="Helvetica 20 bold")
    if len(data.lines)%2==0:
        canvas.create_oval(1/4*data.width-data.dotRadius,5.4/7*data.height-\
            data.dotRadius,1/4*data.width+data.dotRadius,5.4/7*data.height+\
            data.dotRadius,fill='blue')
    elif len(data.lines)%2==1:
        canvas.create_oval(1/4*data.width-data.dotRadius,5.8/7*data.height-\
            data.dotRadius,1/4*data.width+data.dotRadius,5.8/7*data.height+\
            data.dotRadius,fill='blue')

def drawTimeOut(canvas,data):
    if data.timeOut:
        canvas.create_text(1/2*data.width,1/2*data.height,text='Time Out!',\
        fill='blue',font="Helvetica 50 bold")            

def drawResult(canvas,data):
    if data.gameOver:
        if data.player1Score > data.player2Score:
            canvas.create_text(4/5*data.width,5.4/7*data.height,text='Win!',\
            fill='red',font="Helvetica 50 bold")
        elif data.player2Score > data.player1Score:
            canvas.create_text(4/5*data.width,5.8/7*data.height,text='Win!',\
            fill='red',font="Helvetica 50 bold")
        elif data.player1Score == data.player2Score:
            canvas.create_text(4/5*data.width,5.6/7*data.height,text='Tie!',\
            fill='sea green',font="Helvetica 50 bold")

def redrawAll(canvas, data):
    drawBackground(canvas,data)
    drawNodes(canvas,data)
    drawLines(canvas,data)
    drawBoxBoard(canvas,data)
    drawScoreBoard(canvas,data)
    drawTimeOut(canvas,data)
    drawResult(canvas,data)
####################################
# use the run function as-is
####################################

def run(width=300, height=300,rows=30,cols=20,margin=10,radius=2.5):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.dotRows = rows
    data.dotCols = cols
    data.margin = margin
    data.dotRadius = radius
    data.timerDelay = 300 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

# run(300, 300)

####################################
# playTetris() [calls run()]
####################################

def playDotsAndBoxes():
    rows = 5
    cols = 5
    radius =2.5
    margin = 100 # margin around grid
    width = 600
    height = 800
    run(width, height,rows,cols,margin)

playDotsAndBoxes()