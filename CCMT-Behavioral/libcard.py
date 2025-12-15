# Complex Card Matching Task
# Copyright (C) 2025  Giovanna Del Sordo
# Licensed under the GNU General Public License v3.0 or later.
# See the LICENSE file or <https://github.com/giovannacdelsordo/Complex-Card-Matching-Task/blob/faf3ffe3f0b5109642ff9f68b086cc10bc26339c/LICENSE> for details.

#Libcard

from psychopy import visual, core, event, gui

class Card:
    
    # Features
    colors = ["darkblue","darkgreen","brown","darkgoldenrod"] # go to https://www.psychopy.org/_modules/psychopy/colors.html to change shapes' colors
    numbers = [1,2,3,4]
    shapes = ["circle","square","diamond","triangle"]
    sizes = ["small", "medium", "big"]

    def __init__(self, color, number, shape, size):
        self.color = color
        self.number = number
        self.shape = shape
        self.size = size
        
    def __str__(self):
        return "({},{},{},{})".format(self.color,self.number,self.shape,self.size)
        
    def __repr__(self):
        return str(self)

    def matchingFeatures(self, color, number, shape, size):
        result = 0
        if color != None:
            result = result + int(self.color == color)
        if number != None:
            result = result + int(self.number == number)
        if shape != None:
            result = result + int(self.shape == shape)
        if size != None:
            result = result + int(self.size == size)
        return result

    def matchNFeatures(self, n, color=None, number=None, shape=None, size=None):
        nMachedFeatures = self.matchingFeatures(color=color, number=number, shape=shape, size=size)
        return n == nMachedFeatures;

class CardVisual:
     
    def __init__(self, win, pos, size):
        # Window
        self.win = win
        # Mouse
        self.mouse = event.Mouse(visible=True)
        # Position
        self.x = pos[0]
        self.y = pos[1]
        # Card dimensions
        self.w = size[0] 
        self.h = size[1] *0.50
        # Card
        self.card = None
        # Background
        self.background = visual.rect.Rect(win,
            width=self.w, 
            height=self.h, 
            pos=(self.x, self.y), 
            fillColor="lightgrey", 
            lineColor="black")
        # Shapes 
        self.shapes = []
        vOff = self.h/4
        hOff = self.w/4
        self.shapesOffsets = [
            [(-hOff,vOff)], 
            [(-hOff,vOff), (hOff,-vOff)], 
            [(-hOff,vOff), (hOff,vOff), (0,-vOff)],
            [(-hOff,vOff), (hOff,vOff), (-hOff,-vOff), (hOff,-vOff)],
        ]
        self.shapesSizes = [self.w/15, self.w/7, self.w/4.5]

    def getShape(self, position, card):
        edges = 0
        orientation = 0
        radius = 0  
        x,y = position
        xOff = 0
        yOff = 0
        # Shape size
        if card.size == "small":
            radius = self.shapesSizes[0]
        elif card.size == "medium":
            radius = self.shapesSizes[1]
        elif card.size == "big":
            radius = self.shapesSizes[2] 
        else:
            printf("Unrecognized size {}".format(size))
            core.quit()
            
        # Shapes edges and orientation
        if card.shape == "circle": 
            edges = 50
            orientation = 0
            radius = radius * 1.05
        elif card.shape == "triangle":
            edges = 3
            orientation = 0
            radius = radius * 1.25
            yOff = -(radius * 0.2)
        elif card.shape == "square":
            edges = 4
            orientation = 45
            radius = radius * 1.4
        elif card.shape == "diamond":
            edges = 4
            orientation = 0
            radius = radius * 1.1
        else:
            printf("Unrecognized shape {}".format(shape))
            core.quit()
        return visual.Polygon(self.win, 
            edges=edges, 
            ori=orientation, 
            radius=radius,
            fillColor=card.color, 
            pos=(x+xOff, y+yOff))

    def setBorderThickness(self, thickness):
        self.background.lineWidth=thickness

    def selectCard(self, card):
        self.card = card
        self.setBorderThickness(0.005)
        self.shapes = []
        offsets = self.shapesOffsets[card.number-1]
        for i in range(card.number):
            offset = offsets[i]
            position = (self.x+offset[0], self.y+offset[1])
            shape = self.getShape(position, card)
            self.shapes.append(shape)
    
    def autoDraw(self, enable):
        self.background.autoDraw = enable
        for s in self.shapes:
            s.autoDraw = enable

    def isClicked(self):
        results = False
        results = results or self.mouse.isPressedIn(self.background)
        for s in self.shapes:
            results = results or self.mouse.isPressedIn(s)
        return results

        
