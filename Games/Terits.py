from tkinter import *
from random import randint
import copy

def init(data):
    # set board dimensions and margin
    # make board
    data.emptyColor = "blue"
    data.board = [([data.emptyColor] * data.cols) for row in range(data.rows)]
    # create a falling piece and sotre its structure(2d list) and color in a list
    data.fallingPiece=[]
    # define the head (left top) of the falling piece which is the control point
    data.pieceHeadRow = 0
    data.pieceHeadCol = 0
    # store the standard pieces and colors respecitively into a dict and a list
    data.standardPiecesName = []
    data.standardPieces = {}
    standardPieces(data)
    data.piecesColor=[]
    piecesColor(data)
    # define init moving direction
    data.direction = (1,0)
    createTheFallingPiece(data)
    # define the step of moving down 
    data.moveDownStep = 2
    data.centerPoint = []
    data.previousRotate = []
    data.gameOver = False
    data.fullRowCounter = 0
    data.score = 0
########################### Helper function ###################################
# getCellBounds from grid-demo.py
def getCellBounds(row, col, data):
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    x0 = data.margin + gridWidth * col / data.cols
    x1 = data.margin + gridWidth * (col+1) / data.cols
    y0 = data.margin + gridHeight * row / data.rows
    y1 = data.margin + gridHeight * (row+1) / data.rows
    return (x0, y0, x1, y1)

# define standard pieces
def standardPieces(data):
    #Seven "standard" pieces (tetrominoes)
  iPiece = [
    [ True,  True,  True,  True]
  ]
  
  jPiece = [
    [ True, False, False ],
    [ True, True,  True]
  ]
  
  lPiece = [
    [ False, False, True],
    [ True,  True,  True]
  ]
  
  oPiece = [
    [ True, True],
    [ True, True]
  ]
  
  sPiece = [
    [ False, True, True],
    [ True,  True, False ]
  ]
  
  tPiece = [
    [ False, True, False ],
    [ True,  True, True]
  ]

  zPiece = [
    [ True,  True, False ],
    [ False, True, True]
  ]

  data.standardPieces['iPiece']=iPiece
  data.standardPieces['jPiece']=jPiece
  data.standardPieces['lPiece']=lPiece
  data.standardPieces['oPiece']=oPiece
  data.standardPieces['sPiece']=sPiece
  data.standardPieces['tPiece']=tPiece
  data.standardPieces['zPiece']=zPiece
  data.standardPiecesName = ['iPiece','jPiece', 'lPiece', 'oPiece','sPiece',\
  'tPiece','zPiece']

# define piece colors
def piecesColor(data):
    data.piecesColor = [ "red", "yellow", "magenta", "pink", "cyan", \
    "green", "orange" ]
 
def createTheFallingPiece(data):
    # randomly select a piece from the piece set:
    randomIndexPiece = randint(0,100000)%len(data.standardPiecesName)
    data.fallingPiece.append(data.standardPieces\
        [data.standardPiecesName[randomIndexPiece]])
    # randomly select a type of color from the data.piececolor
    randomIndexColor = randint(0,1000)%len(data.piecesColor)
    data.fallingPiece.append(data.piecesColor[randomIndexColor])
    data. pieceHeadRow = 0
    data. pieceHeadCol = (data.cols-len(data.fallingPiece[0][0]))//2  

def isMoveLegal(data):
    # Check if the move out of rows' bounds:
    if data.pieceHeadRow < 0 or data.pieceHeadRow + len(data.fallingPiece[0])\
     + data.direction[0] >= data.rows:
        return False
    # Check if the move out of cols' bounds :
    elif data.pieceHeadCol + data.direction[1] < 0 or data.pieceHeadCol + \
    len(data.fallingPiece[0][0]) + data.direction[1] > data.cols:
        return False
    # Then check if there will be collison with existed pieces if there is,
    # the move is forbidden and the pieces will go straight down
    updateRow = data.pieceHeadRow + data.direction[0] 
    updateCol = data.pieceHeadCol + data.direction[1]
    for row in range(updateRow, updateRow+len(data.fallingPiece[0])):
        for col in range(updateCol, updateCol\
            +len(data.fallingPiece[0][0])):
            if row > data.rows or col > data.cols:
                return False
            elif data.board[row][col] != data.emptyColor:
               if data.fallingPiece[0][row-data.pieceHeadRow\
                    -data.direction[0]][col-data.pieceHeadCol\
                    -data.direction[1]] == True:
                    return False
    return True

def doesMoveReachBottomOrObject(data):
    # Check if the falling piece is at the bottom of the board
    if data.pieceHeadRow + len(data.fallingPiece[0]) >= data.rows:
        return True
    else:    
        updateRow = data.pieceHeadRow + data.direction[0]//data.direction[0]
        updateCol = data.pieceHeadCol + data.direction[1] 
        for row in range(updateRow, updateRow+len(data.fallingPiece[0])):
            for col in range(updateCol, updateCol\
                +len(data.fallingPiece[0][0])):
                if data.board[row][col] != data.emptyColor:
                    if data.fallingPiece[0][row-data.pieceHeadRow\
                    -data.direction[0]][col-data.pieceHeadCol\
                    -data.direction[1]]== True:
                        return True
        return False

def moveFallingPiece(data):
    drow = data.direction[0]
    dcol = data.direction[1]
    data.pieceHeadRow += drow
    data.pieceHeadCol += dcol
    data.direction = (1,0)

def rotateFallingPiece(data):
    rows = len(data.fallingPiece[0])
    cols = len(data.fallingPiece[0][0])
    # calculate and sotre the center point 
    centerRow = data.pieceHeadRow + rows//2
    centerCol = data.pieceHeadCol + cols//2
    if data.centerPoint == []:
        data.centerPoint.append((centerRow,centerCol))
    # create a new 2d list to store the rotated 2d list
    updateFallingPiece = [(['-']*rows) for col in range(cols)]
    for row in range(rows):
        for col in range(cols):  
            updateFallingPiece[cols-1-col][row] = data.fallingPiece[0][row][col]
    data.previousRotate = []
    data.previousRotate.append(data.fallingPiece[0])
    data.previousRotate.append((data.pieceHeadRow,data.pieceHeadCol))
    data.fallingPiece[0] = updateFallingPiece
    # update the pieceHeadRow and pieceHeadCol to get the position of the falling pieces
    updatedpieceHeadRow = data.pieceHeadRow + (rows-cols)//2
    updatedpieceHeadCol = data.pieceHeadCol + (cols-rows)//2
    #calculate the updated center point
    updatedCenterRow = updatedpieceHeadRow + cols//2
    updatedCenterCol = updatedpieceHeadCol + rows//2
    #calucalte the shifted row
    shiftRow = updatedCenterRow - centerRow
    shiftCol = updatedCenterCol - centerCol
    #shift the piece head to the right place
    data.pieceHeadRow = updatedpieceHeadRow - shiftRow
    data.pieceHeadCol = updatedpieceHeadCol - shiftCol

def placeFallingPiece(data):
    for row in range(data.pieceHeadRow, data.pieceHeadRow\
     + len(data.fallingPiece[0])):
        for col in range(data.pieceHeadCol, data.pieceHeadCol\
         + len(data.fallingPiece[0][0])):
            if data.fallingPiece[0][row-data.pieceHeadRow]\
            [col-data.pieceHeadCol] == True:
                data.board[row][col] = data.fallingPiece[1]

def checkGameOver(data):
    for col in range(data.cols):
        if data.board[0][col] != data.emptyColor:
            return True
    return False

def checkFullOrNot(Row,data):
    for element in Row:
        if element == data.emptyColor:
            return False
    return True

def removeFullRows(data):
    newRows = []
    removeRowsCounter = 0
    data.fullRowCounter=0
    for row in range(data.rows):
       oldRow = data.board[data.rows-1-row]
       data.board.pop()
       if not checkFullOrNot(oldRow,data):
            newRows.insert(0,copy.deepcopy(oldRow))
       elif checkFullOrNot(oldRow,data):
            data.fullRowCounter+=1
    for i in range(data.fullRowCounter):
        newRows.insert(0,[data.emptyColor]*data.cols)  
    data.board += newRows
    if data.fullRowCounter !=0:
        data.score+=data.fullRowCounter**2

################################# Control #####################################
def mousePressed(event, data):
    pass

def keyPressed(event, data):
    if event.keysym == 'a':
        data.direction = (1,-1)
        if not isMoveLegal(data): data.direction = (1,0)
    elif event.keysym == 'd':
        data.direction = (1,1)
        if not isMoveLegal(data): data.direction = (1,0)
    elif event.keysym == 's':
        data.direction = (data.moveDownStep,0)   # There is still bugs here the bug is about out of list index 
        if not isMoveLegal(data): data.direction = (1,0)  
    elif event.keysym == 'w':
        rotateFallingPiece(data)
        if not isMoveLegal(data):
            data.fallingPiece[0] = data.previousRotate[0]
            data.pieceHeadRow = data.previousRotate[1][0]
            data.pieceHeadCol = data.previousRotate[1][1]
    elif event.keysym == 'r':
        init(data)

def timerFired(data):
    if not doesMoveReachBottomOrObject(data):
        moveFallingPiece(data)
    elif doesMoveReachBottomOrObject(data):
        placeFallingPiece(data)
        data.fallingPiece = []
        createTheFallingPiece(data)
        data.direction=(1,0)
    if checkGameOver(data):
        data.gameOver = True
    removeFullRows(data)
###############################  View ########################################

def drawGame(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="orange")
    drawBoard(canvas, data)
    drawFallingPiece(canvas,data)
    drawScore(canvas,data)
    if data.fullRowCounter!=0:
        drawGetScore(canvas,data)
    if data.gameOver == True:
        drawGameover(canvas,data)

def drawBoard(canvas, data):
    # draw grid of cells
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, data, row, col)

def drawCell(canvas, data, row, col):
    (x0, y0, x1, y1) = getCellBounds(row, col, data)
    m = 1 # cell outline margin
    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
    canvas.create_rectangle(x0+m, y0+m, x1-m, y1-m, fill=data.board[row][col])

def drawFallingPiece(canvas, data):
    m = 1 # cell outline margin
    rows = len(data.fallingPiece[0])
    cols = len(data.fallingPiece[0][0])
    for row in range(rows):
        for col in range(cols):
            updateRow = data.pieceHeadRow + row
            updateCol = data.pieceHeadCol + col
            (x0 ,y0, x1, y1) = getCellBounds(updateRow,updateCol,data)
            if data.fallingPiece[0][row][col] == True:
                canvas.create_rectangle(x0+m, y0+m, x1-m, y1-m, \
                    fill=data.fallingPiece[1])

def drawGameover(canvas,data):
    canvas.create_text(data.width/2,data.height/2, text = "Game Over"\
        ,fill='white', font = "Helvetica 30 bold underline")

def drawScore(canvas,data):
    canvas.create_text(data.width*4/5,data.height/10, text = data.score\
        ,fill='white', font = "Helvetica 50 bold")

def drawGetScore(canvas, data):
    canvas.create_text(data.width*2/5,data.height/2,text='X',\
        fill = 'orange',font= "Helvetica 60 bold underline")
    canvas.create_text(data.width*3/5,data.height/2,text=data.fullRowCounter,\
        fill = 'orange',font= "Helvetica 60 bold underline")

def redrawAll(canvas, data):
    drawGame(canvas, data)

####################################
# use the run function as-is
####################################

def run(width=300, height=300,rows=30,cols=20,margin=10):
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
    data.rows = rows
    data.cols = cols
    data.margin = margin
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

def playTetris():
    rows = 20
    cols = 15
    margin = 10 # margin around grid
    cellSize = 25 # width and height of each cell
    width = 2*margin + cols*cellSize
    height = 2*margin + rows*cellSize
    run(width, height,rows,cols,margin)

playTetris()