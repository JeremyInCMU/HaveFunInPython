# H-fractals.py

from tkinter import *

def init(data):
    data.level = 1

def drawhFractal(canvas, x, y, size, level):
    # (x,y) is the center of H
    # size is the length of an edge
    # base case
    if (level == 0):
        canvas.create_line(x-size/2,y,x+size/2,y)
        canvas.create_line(x-size/2,y-size/2,x-size/2,y+size/2)
        canvas.create_line(x+size/2,y-size/2,x+size/2,y+size/2)

    else:
        drawhFractal(canvas, x-size/2,y-size/2,size/2,level-1)
        drawhFractal(canvas, x-size/2,y+size/2,size/2,level-1)
        drawhFractal(canvas, x+size/2,y-size/2,size/2,level-1)
        drawhFractal(canvas, x+size/2,y+size/2,size/2,level-1)

def keyPressed(event, data):
    if (event.keysym in ["Up", "Right"]):
        data.level += 1
    elif ((event.keysym in ["Down", "Left"]) and (data.level > 0)):
        data.level -= 1

def redrawAll(canvas, data):
    for level in range(data.level+1):
        drawhFractal(canvas, data.width/2, data.height/2, data.size,level)
    canvas.create_text(data.width/2, data.height/20,
                       text = "Level %d Sierpinsky Triangle" % (data.level),
                       font = "Arial 26 bold")
    canvas.create_text(data.width/2, data.height/10,
                       text = "Use arrows to change level",
                       font = "Arial 10")

def mousePressed(event, data): pass

def timerFired(data): pass

####################################
# use the run function as-is
####################################

def run(width=300, height=300, size=100):
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
    data.size = 200
    data.timerDelay = 100 # milliseconds
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

def hFractal():
    run(500,500)

hFractal()

