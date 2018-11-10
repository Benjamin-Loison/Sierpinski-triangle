#-------------------------------------------------------------------------------
# Name:        Sierpinski's triangle
# Purpose:     Draw the Sierpinski's triangle
#
# Author:      Benjamin Loison
#
# Created:     10/11/2018
# Copyright:   (c) Benjamin Loison 2018
# Licence:     No licence (quote the author)
#-------------------------------------------------------------------------------

## Load TKinter standard library which has graphical tools
from tkinter import *
## Load math standard module which has the sqrt (root) and trigonometric functions
from math import *
## from time import sleep as wait
from PIL import Image, ImageDraw

BLACK = "#000000"

def segmentDraw(x0, y0, x1, y1, color = BLACK):
    if enableRender:
        global canvas
        canvas.create_line(x0 + 1, y0 + 1, x1 + 2, y1 + 2, fill = color)
    draw.line([x0 + 1, y0 + 1, x1 + 2, y1 + 2], color)

# Beginning of the code for Sierpinski's triangle

enableRender = False
currentIterationSaving = 0

#WINDOW_WIDTH, WINDOW_HEIGHT = 1350, 1350
WINDOW_WIDTH, WINDOW_HEIGHT = 3840, 3840

class Point:
    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]

class Segment:
    def __init__(self, points):
        self.points = points

class Triangle:
    def __init__(self, segments):
        self.segments = segments

def drawSegment(segment):
    points = segment.points
    pt0 = points[0]
    pt1 = points[1]
    segmentDraw(pt0.x, pt0.y, pt1.x, pt1.y)

def middlePoint(segment):
    points = segment.points
    pt0 = points[0]
    pt1 = points[1]
    return Point(((pt0.x + pt1.x) / 2, (pt0.y + pt1.y) / 2))

def drawTriangle(triangle, iteration):
    global MAX_ITERATION
    if iteration > MAX_ITERATION:
        return
    segments = triangle.segments
    segmentTopCenterToBottomLeft = segments[0]
    segmentTopCenterToBottomRight = segments[1]
    segmentBottomLeftToBottomRight = segments[2]

    pointMiddleLeft = middlePoint(segmentTopCenterToBottomLeft)
    pointMiddleRight = middlePoint(segmentTopCenterToBottomRight)
    pointMiddleBottom = middlePoint(segmentBottomLeftToBottomRight)

    segmentMiddleTop = Segment((pointMiddleLeft, pointMiddleRight))
    segmentMiddleLeft = Segment((pointMiddleLeft, pointMiddleBottom))
    segmentMiddleRight = Segment((pointMiddleRight, pointMiddleBottom))

    drawSegment(segmentMiddleTop)
    drawSegment(segmentMiddleLeft)
    drawSegment(segmentMiddleRight)

    iteration += 1

    segmentTopCenterToMiddleLeft = Segment((segmentTopCenterToBottomLeft.points[0], pointMiddleLeft))
    segmentTopCenterToMiddleRight = Segment((segmentTopCenterToBottomRight.points[0], pointMiddleRight))
    triangleTop = Triangle((segmentTopCenterToMiddleLeft, segmentTopCenterToMiddleRight, segmentMiddleTop))
    drawTriangle(triangleTop, iteration)

    segmentMiddleLeftToBottomLeft = Segment((pointMiddleLeft, segmentBottomLeftToBottomRight.points[0]))
    segmentBottomLeftToMiddleBottom = Segment((segmentBottomLeftToBottomRight.points[0], pointMiddleBottom))
    triangleBottomLeft = Triangle((segmentMiddleLeftToBottomLeft, segmentMiddleLeft, segmentBottomLeftToMiddleBottom))
    drawTriangle(triangleBottomLeft, iteration)

    segmentMiddleRightToBottomRight = Segment((pointMiddleRight, segmentBottomLeftToBottomRight.points[1]))
    segmentMiddleBottomToRightBottom = Segment((pointMiddleBottom, segmentBottomLeftToBottomRight.points[1]))
    triangleBottomRight = Triangle((segmentMiddleRight, segmentMiddleRightToBottomRight, segmentMiddleBottomToRightBottom))
    drawTriangle(triangleBottomRight, iteration)

while True:
    if enableRender:
        ## Load TK Engine
        tkengine = Tk()
        ## Load twindow
        window = Frame(tkengine)
        window.pack()
        ## Background hexadecimal code: white
        canvas = Canvas(window, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, bg = "#FFFFFF")
        canvas.pack()

    ## PIL create an empty image and draw object to draw on
    ## memory only, not visible
    image = Image.new("RGBA", (WINDOW_WIDTH, WINDOW_HEIGHT + 3), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    if enableRender:
        MAX_ITERATION = int(input("Iteration"))
    else:
        MAX_ITERATION = currentIterationSaving

    pointTopCenter = Point((WINDOW_WIDTH // 2, 0))
    pointBottomLeft = Point((0, WINDOW_HEIGHT))
    pointBottomRight = Point((WINDOW_WIDTH, WINDOW_HEIGHT))

    segmentTopCenterToBottomLeft = Segment((pointTopCenter, pointBottomLeft))
    segmentTopCenterToBottomRight = Segment((pointTopCenter, pointBottomRight))
    segmentBottomLeftToBottomRight = Segment((pointBottomLeft, pointBottomRight))

    drawSegment(segmentTopCenterToBottomLeft)
    drawSegment(segmentTopCenterToBottomRight)
    drawSegment(segmentBottomLeftToBottomRight)

    drawTriangle(Triangle((segmentTopCenterToBottomLeft, segmentTopCenterToBottomRight, segmentBottomLeftToBottomRight)), 0)

    # End of the code for Sierpinski's triangle

    ## PIL image can be saved as .png .jpg .gif or .bmp file (among others)
    filename = str(MAX_ITERATION) + ".png"
    image.save(filename)

    if enableRender:
        ## Infinite loop to always display the window
        tkengine.mainloop()
    else:
        currentIterationSaving += 1
