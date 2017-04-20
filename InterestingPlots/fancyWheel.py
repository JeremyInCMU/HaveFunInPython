from tkinter import *
####################################
# FancyWheels
####################################
import math
def fancyWheelsInit(data):
    data.rows = 5
    data.cols = 5
    data.sides = 4
    data.margin = 40
    data.gridWidth = data.width - 2*data.margin
    data.gridHeight = data.height  - 2*data.margin
    data.cellSize = data.gridWidth // data.rows
    data.circleRadio = 40
    data.circleCenters = {}
    data.angle = 2*math.pi
    data.rotateAngle = data.angle/180
    data.counter = 0
    data.colorRow ='#00FF00'
    data.colorCol ='#00FF00'
    data.colorBoard = createColorBoard(data)

########################## Helper functions ####################################
def createColorBoard(data):
    board = [[data.colorRow]*data.cols for row in range(data.rows)]
    numVariationInRow = 255/ data.rows
    numVariationInCol = 255/ data.cols
    for row in range(data.rows):
        data.colorRow = updateColorString(data.colorRow,1,numVariationInRow)
        data.colorCol = data.colorRow
        for col in range(data.cols):
            data.colorCol = updateColorString(data.colorCol,3,-numVariationInCol)
            board[row][col] = data.colorCol
    return board

def updateColorString(color, targindex, numVariation):
    updateColorString = ''
    index = 0
    while(index < len(color)-1):
        if color[index] == '#':
            updateColorString+='#'
            index += 1
        elif index == targindex:
            num = transmitHexLetterToNum(color[index])*16
            num += transmitHexLetterToNum(color[index+1])
            num += numVariation
            if num//16 <= 0 and num%16 <=0:
                updateColorString += transmitNumToHexLetter(0)
                updateColorString += transmitNumToHexLetter(0)
            elif num//16<=0:
                updateColorString += transmitNumToHexLetter(0)
                updateColorString += transmitNumToHexLetter(num%16)
            elif num %16 <= 0:
                updateColorString += transmitNumToHexLetter(num//16)
                updateColorString += transmitNumToHexLetter(0)
            else:
                updateColorString += transmitNumToHexLetter(num//16)
                updateColorString += transmitNumToHexLetter(num%16)
            index+=2
        elif index!= targindex:
            updateColorString += color[index] + color[index+1]
            index+=2
    return updateColorString

import string 
def transmitHexLetterToNum(letter):
    if letter in string.digits:
        return int(letter)
    elif letter in string.ascii_uppercase:
        return (ord(letter) -  ord('A'))+10

def transmitNumToHexLetter(num):
    num = int(num)
    if num <= 9:
        return str(num)
    elif num == 10:
        return 'A'
    elif num == 11:
        return 'B'
    elif num == 12:
        return 'C'
    elif num == 13:
        return 'D'
    elif num == 14:
        return 'E'
    elif num == 15:
        return 'F'

def transmitPositioToCircleCenter(data,row, col):
    lefttopx = data.margin + col*data.cellSize
    lefttopy = data.margin + row*data.cellSize
    rightbottomx = data.margin + (col+1)*data.cellSize
    rightbottomy = data.margin + (row+1)*data.cellSize
    circleCenterx = (lefttopx+rightbottomx)/2
    circleCentery = (lefttopy+rightbottomy)/2
    return (circleCenterx, circleCentery)

def getCircleCenters(data):    
    for row in range(data.rows):
        for col in range(data.cols):
            (cx , cy) = transmitPositioToCircleCenter(data,row,col)
            data.circleCenters[(row, col)] = (cx , cy)   

def getMultiPoints(data,startpoint, row ,col):
    multiPoints = []
    data.sides = 4 + (row + col)
    angle = data.angle / data.sides
    if (row+col)%2==0:
        for i in range(data.sides):
            updatepointX = startpoint[0] + data.circleRadio*math.cos(i*angle\
                -data.counter*data.rotateAngle)
            updatepointY = startpoint[1] - data.circleRadio*math.sin(i*angle\
                -data.counter*data.rotateAngle)
            multiPoints.append((updatepointX,updatepointY))
    elif (row + col)%2==1:
        for i in range(data.sides):
            updatepointX = startpoint[0] + data.circleRadio*math.cos(i*angle\
                +data.counter*data.rotateAngle)
            updatepointY = startpoint[1] - data.circleRadio*math.sin(i*angle\
                +data.counter*data.rotateAngle)
            multiPoints.append((updatepointX,updatepointY))
    return multiPoints

################################################################################

def fancyWheelsMousePressed(event, data):
    # use event.x and event.y
    pass

def fancyWheelsKeyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym == 'Right' or event.keysym == 'Up':
        data.rows +=1
        data.cols +=1 
    elif event.keysym =='Left' or event.keysym =='Down':
        data.rows -=1
        data.cols -=1
    data.colorRow ='#00FF00'
    data.colorCol ='#00FF00'
    data.colorBoard = createColorBoard(data)

def fancyWheelsTimerFired(data):
    data.counter+=1

def fancyWheelsRedrawAll(canvas, data):
    getCircleCenters(data)
    for row in range(data.rows):
        for col in range(data.cols):
            Points = getMultiPoints(data, data.circleCenters[(row,col)],row,col)
            steps = data.sides    
            for step in range(steps):
                for i in range(len(Points)):
                    index1 = i%len(Points) 
                    index2 = (i+step)%len(Points)
                    canvas.create_line(Points[index1][0],Points[index1][1],\
                    Points[index2][0],Points[index2][1], width=1, fill = data.colorBoard[row][col])

    
####################################
# run function for FancyWheels
####################################

def runFancyWheels(width=800, height=800):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        fancyWheelsRedrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        fancyWheelsMousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        fancyWheelsKeyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        fancyWheelsTimerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 90 # milliseconds
    fancyWheelsInit(data)
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

runFancyWheels()