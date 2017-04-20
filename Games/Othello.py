from tkinter import *

####################################
# Othello
####################################

def othelloInit(data):
    data.rows = 8
    data.cols = 8
    data.board = createBoard(data.rows,data.cols)
    data.margin = 100
    data.boardWidth = data.width - 2*data.margin
    data.boardHeight = data.height - 2*data.margin
    data.cellSize = data.boardWidth//data.rows
    data.cellColor1 = "sea green"
    data.cellColor2 = "dark olive green"
    data.nodeRadio = 0.9*data.cellSize/2
    data.listOfLegalRoutes = []
    data.nodeColor = 'black'
    data.playerCounter1 = 2
    data.playerCounter2 = 2
    data.player1 = 1
    data.player2 = -1
    data.winner = ''
########################## Helper functions ####################################
def createBoard(rows, cols):
    return [([0]*cols) for row in range(rows)]

def transmitColorToDigits(color):
    if color == 'black':
        return 1
    elif color == 'white':
        return -1
def transmitDigitsToColor(digit):
    if digit == 1:
        return 'black'
    elif digit == -1:
        return 'white'

def checkElementOf2DList(board , element):
    rows = len(board)
    cols = len(board[0])
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == element:
                continue
            else:
                return False
    return True

def transmitPositioToCircleCenter(data,row, col):
    lefttopx = data.margin + col*data.cellSize
    lefttopy = data.margin + row*data.cellSize
    rightbottomx = data.margin + (col+1)*data.cellSize
    rightbottomy = data.margin + (row+1)*data.cellSize
    nodeCenterx = (lefttopx+rightbottomx)/2
    nodeCentery = (lefttopy+rightbottomy)/2
    return (nodeCenterx, nodeCentery)

# This function is built to create the four nodes (two black and two white) at the 
# center of the board
def othelloNodesInitilize(data):
    initialrow = 0
    initialcol = 0
    for row in range(data.rows):
        for col in range(data.cols):
            if row+(row+1) == data.rows-1 and col+(col+1) == data.cols-1:
                initialrow = row
                initialcol = col
    for row in range(initialrow, initialrow+2):
        for col in range(initialcol, initialcol+2):
            if (row+col)%2 == 0:
                data.board[row][col] = -1
            elif (row+col)%2 ==1:
                data.board[row][col] = 1

def updateNodesAfterPress(data,row,col):
    if row < 0 or row >= data.rows or col < 0 or col >= data.cols\
     or data.board[row][col] != 0: 
        pass
    elif (row >=0 or row < data.rows or col >= 0 or col < data.cols) \
    and (bool(legalRoutes(data,row,col))):
        if data.nodeColor == 'black':
            data.board[row][col] = 1
        elif data.nodeColor == 'white':
            data.board[row][col] = -1
        if data.nodeColor == 'black':
            data.nodeColor = 'white'
        else:
            data.nodeColor = 'black'

def legalRoutes(data,row,col):
    for drow in [-1,0,1]:
        for dcol in [-1,0,1]:
            if drow == 0 and dcol == 0:
                continue
            elif detectLegalRouteInOneDir(data, row, col, drow, dcol):
                data.listOfLegalRoutes.append(detectLegalRouteInOneDir\
                    (data, row, col, drow, dcol))
    if data.listOfLegalRoutes == []:
        return False
    else:
        # print(data.listOfLegalRoutes)
        return data.listOfLegalRoutes

def detectLegalRouteInOneDir(data, row, col, drow, dcol):
    singleRoute={}
    listOfNodeColor = []
    index = 1
    singleRoute[(row,col)] = data.nodeColor
    while(1):
        updaterow = row + index*drow
        updatecol = col + index*dcol
        if updaterow < 0 or updaterow >= len(data.board) or\
         updatecol < 0 or updatecol >= len(data.board):
            break;
        elif data.board[updaterow][updatecol] == 0:
            break;
        elif data.board[updaterow][updatecol] == transmitColorToDigits(data.nodeColor):
            listOfNodeColor.append(data.board[updaterow][updatecol])
            singleRoute[(updaterow,updatecol)] = data.board[updaterow][updatecol]
            break;
        else:
            listOfNodeColor.append(data.board[updaterow][updatecol])
            singleRoute[(updaterow,updatecol)] = data.board[updaterow][updatecol]
        index+=1
    if len(listOfNodeColor) <= 1:
        return False
    elif data.nodeColor == 'black':
        if sum(listOfNodeColor) > -len(listOfNodeColor):
            return singleRoute
        else:
            return False
    elif data.nodeColor == 'white':
        if sum(listOfNodeColor)< len(listOfNodeColor):
            return singleRoute
        else:
            return False

def updateNodesOnLegalRoutes(data):
    for d in data.listOfLegalRoutes:
        for value in d.values():
            if value == 'black' or value == 'white':
                updateColorOfNodesInRoute(data, d, value)
    data.listOfLegalRoutes = []
# Destructive function without return values
def updateColorOfNodesInRoute( data, route, color):  
    for key in route.keys():
        if route[key] != transmitColorToDigits(color) and route[key] != color:
            data.board[key[0]][key[1]] = transmitColorToDigits(color)

def updateCounterOfPlayers(data,palyer):
    result = 0
    for row in range(data.rows):
        for col in range(data.cols):
            if data.board[row][col] == palyer:
                result+=1
    return result

def checkIfAllCeilsAreOccupied(data):
    for row in range(data.rows):
        for col in range(data.cols):
            if data.board[row][col] !=0:
                continue
            elif data.board[row][col] == 0:
                return False
    return True

def isWin(data):
    if data.playerCounter1 > data.playerCounter2:
        data.winner = 'player1'
    elif data.playerCounter1 < data.playerCounter2:
        data.winner = 'player2'
    elif data.playerCounter1 == data.playerCounter2:
        data.winner = 'Tie'

################################################################################
def othelloMousePressed(event, data): 
    col = (event.x - data.margin)//data.cellSize
    row = (event.y - data.margin)//data.cellSize
    updateNodesAfterPress(data, row, col)
    updateNodesOnLegalRoutes(data)
    data.playerCounter1 = updateCounterOfPlayers(data,data.player1)
    data.playerCounter2  = updateCounterOfPlayers(data,data.player2)
    if checkIfAllCeilsAreOccupied(data):
        isWin(data)

def othelloKeyPressed(event, data):
    # use event.char and event.keysym
    pass

def othelloTimerFired(data):
    pass

def othelloRedrawAll(canvas, data):
    # draw in canvas
################ Initialize the grids ##########################################
    for row in  range(data.rows):
        for col in  range(data.cols):
            lefttopx = data.margin + col*data.cellSize
            lefttopy = data.margin + row*data.cellSize
            rightbottomx = data.margin + (col+1)*data.cellSize
            rightbottomy = data.margin + (row+1)*data.cellSize
            if (row+col)%2==0:
                canvas.create_rectangle(lefttopx,lefttopy,rightbottomx,\
                    rightbottomy,fill=data.cellColor1)
            elif (row+col)%2==1:
                canvas.create_rectangle(lefttopx,lefttopy,rightbottomx,\
                    rightbottomy,fill=data.cellColor2)

#################### Initialize the initial nodes ##############################
    if checkElementOf2DList(data.board,0):
        othelloNodesInitilize(data)

##################### Update nodes on grids (board) ############################
    for row in range(data.rows):
        for col in range(data.cols):
            if data.board[row][col] == 0:
                continue
            else:
                (cx ,cy) = transmitPositioToCircleCenter(data, row, col)
                color = transmitDigitsToColor(data.board[row][col])
                canvas.create_oval(cx-data.nodeRadio,cy-data.nodeRadio,cx\
                    +data.nodeRadio,cy+data.nodeRadio, fill=color)

###################  Draw counters #############################################
    canvas.create_rectangle(100,510,500,600, fill = "dark green")
    
    canvas.create_text(250,540, text="Player1:  x" + str(data.playerCounter1 ), fill='black',\
        font='Helvetica 15 bold underline')
    canvas.create_oval(150-data.nodeRadio*0.75,540-data.nodeRadio*0.75,150+data.nodeRadio*0.75,\
        540+data.nodeRadio*0.75,fill="black")
    canvas.create_text(250,580, text="Player2:  x" + str(data.playerCounter2 ), fill='white',\
        font='Helvetica 15 bold underline')
    canvas.create_oval(150-data.nodeRadio*0.75,580-data.nodeRadio*0.75,150+data.nodeRadio*0.75,\
        580+data.nodeRadio*0.75,fill="white")
############  The codes below is written for judge the result in the window
    if data.nodeColor == 'black':
        canvas.create_oval(190-data.nodeRadio*0.2,540-data.nodeRadio*0.2,190+data.nodeRadio*0.2,\
            540+data.nodeRadio*0.2, fill='yellow')
    elif data.nodeColor == 'white':
        canvas.create_oval(190-data.nodeRadio*0.2,580-data.nodeRadio*0.2,190+data.nodeRadio*0.2,\
            580+data.nodeRadio*0.2, fill='yellow')

    if data.winner == 'player1':
        canvas.create_text(400,540, text= "Win!", fill='red',font='Helvetica 25 bold')
    elif data.winner == 'player2':
        canvas.create_text(400,580, text= "Win!", fill='red',font='Helvetica 25 bold')
    elif data.winner == 'Tie':
        canvas.create_text(400,550, text= "Tie", fill='blue',font='Helvetica 50 bold')
########canvas.create_text()  to count player1's nodes and player2's nodes Player1 with a black node and player2 with a white node

####################################
# run function for Othello
####################################

def runOthello(width=600, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        othelloRedrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        othelloMousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        othelloKeyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        othelloTimerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    othelloInit(data)
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

runOthello()