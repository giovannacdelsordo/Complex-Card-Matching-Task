# librule
from libcard import CardVisual, Card
import random
from psychopy import visual, core, event, gui
import time

def xor(a, b):
    return (a == True and b == False) or (a == False and b == True)

class RULE: 
    difficulties = ["easy","hard"]
    easyRules = ["color","number","shape","color+number","color+shape","number+shape"]
    hardRules = ["color+size","number+size","shape+size","color+number","color+shape","number+shape"]
    
    def __init__(self, win):
        # Window
        self.win = win
        # Offsets
        self.vOff = 0.25
        self.hOff = 0.25
        # Card dimensions
        self.cardSize = (0.2, 0.5)
        # Top cards
        self.correctTopCardIndex = None
        self.topCards = []
        for i in range(4):
            # Calculate x position based on offsets
            x = -0.5 + self.hOff/2 + (i * self.hOff)  # Start from -0.5 and space out by hOff
            pos = (x, self.vOff)
            c = CardVisual(win, pos, self.cardSize)
            self.topCards.append(c) 
        # Bottom card
        self.bottomCard = CardVisual(win, (0,-0.5*self.vOff), self.cardSize)
        # All cards 
        self.allCards = []
        for c in Card.colors:
            for n in Card.numbers:
                for sh in Card.shapes:
                    for sz in Card.sizes:
                        self.allCards.append(Card(c,n,sh,sz))
        random.shuffle(self.allCards)
        # Wrong and correct cards
        self.cBottom = None
        self.cTop = None
        self.wTop1 = None
        self.wTop2 = None
        self.wTop3 = None
        # Times
        self.selectionTimeOut = 6
        self.responseDelay = 1
    
    def applyRule(self, rule, difficulty):
        targetColor = random.choice(Card.colors)
        targetNumber = random.choice(Card.numbers)
        targetShape = random.choice(Card.shapes) 
        targetSize = ""
        similarCards = []
        if difficulty == "hard":
            targetSize = random.choice(Card.sizes)
            similarCards = [c for c in self.allCards if c.matchNFeatures(2,color=targetColor,number=targetNumber,shape=targetShape,size=targetSize)]
        elif difficulty == "easy":
            targetSize = "medium"
            similarCards = [c for c in self.allCards if c.matchNFeatures(1,size=targetSize) and c.matchNFeatures(2,color=targetColor,number=targetNumber,shape=targetShape)]
        else:
            print("Difficulty not supported: {}".format(difficulty))
            core.quit()
        correctCards = []
        wrongCards = []
        if rule == "color":
            correctCards = [c for c in similarCards if c.matchNFeatures(1,color=targetColor)]
            wrongCards  = [c for c in similarCards if c.matchNFeatures(0,color=targetColor)]
        elif rule == "number":
            correctCards = [c for c in similarCards if c.matchNFeatures(1,number=targetNumber)]
            wrongCards  = [c for c in similarCards if c.matchNFeatures(0,number=targetNumber)]
        elif rule == "shape":
            correctCards = [c for c in similarCards if c.matchNFeatures(1,shape=targetShape)]
            wrongCards  = [c for c in similarCards if c.matchNFeatures(0,shape=targetShape)]
        elif rule == "size" and difficulty == "hard":
            correctCards = [c for c in similarCards if c.matchNFeatures(1,size=targetSize)]
            wrongCards  = [c for c in similarCards if c.matchNFeatures(0,size=targetSize)]
        elif rule == "color+number":
            correctCards = [c for c in similarCards if c.matchNFeatures(2,color=targetColor,number=targetNumber)]
            wrongCards  = [c for c in similarCards if c.matchNFeatures(1,color=targetColor,number=targetNumber)]
        elif rule == "color+shape":
            correctCards = [c for c in similarCards if c.matchNFeatures(2,color=targetColor,shape=targetShape)]
            wrongCards  = [c for c in similarCards if c.matchNFeatures(1,color=targetColor,shape=targetShape)]
        elif rule == "color+size" and difficulty == "hard":
            correctCards = [c for c in similarCards if c.matchNFeatures(2,color=targetColor,size=targetSize)]
            wrongCards  = [c for c in similarCards if c.matchNFeatures(1,color=targetColor,size=targetSize)]
        elif rule == "number+shape":
            correctCards = [c for c in similarCards if c.matchNFeatures(2,number=targetNumber,shape=targetShape)]
            wrongCards  = [c for c in similarCards if c.matchNFeatures(1,number=targetNumber,shape=targetShape)]
        elif rule == "number+size" and difficulty == "hard":
            correctCards = [c for c in similarCards if c.matchNFeatures(2,number=targetNumber,size=targetSize)]
            wrongCards  = [c for c in similarCards if c.matchNFeatures(1,number=targetNumber,size=targetSize)]
        elif rule == "shape+size" and difficulty == "hard":
            correctCards = [c for c in similarCards if c.matchNFeatures(2,shape=targetShape,size=targetSize)]
            wrongCards  = [c for c in similarCards if c.matchNFeatures(1,shape=targetShape,size=targetSize)]
        else:
            core.quit()
        self.cBottom = Card(targetColor,targetNumber,targetShape,targetSize)
        self.cTop = random.choice(correctCards)
        self.wTop1, self.wTop2, self.wTop3 = random.sample(wrongCards,3)
      
    
    def visualizeCards(self):
        self.bottomCard.autoDraw(True)
        for i in range(4):
            self.topCards[i].autoDraw(True)
    
    def clearCards(self):
        self.bottomCard.autoDraw(False)
        for i in range(4):
            self.topCards[i].autoDraw(False)

    def selectCards(self):
        # Bottom card selection
        self.bottomCard.selectCard(self.cBottom)
        # Top card selection
        topCardsSet = [self.cTop,self.wTop1,self.wTop2,self.wTop3]
        random.shuffle(topCardsSet)
        self.correctTopCardIndex = topCardsSet.index(self.cTop)
        for i in range(4):
            card = topCardsSet[i]
            self.topCards[i].selectCard(card)

    def runCondition(self, rule, difficulty):
        self.clearCards()
        self.win.flip()
        self.applyRule(rule, difficulty)
        self.selectCards()
        self.visualizeCards()
        self.win.flip()
        # Running
        reactionStartTime = time.perf_counter()
        reactionElapsedTimeMouse = 0
        selectedCard = None
        # Clear pressed space
        event.getKeys(keyList=["space"])
        while selectedCard == None and reactionElapsedTimeMouse <= self.selectionTimeOut:
            reactionElapsedTimeMouse = time.perf_counter() - reactionStartTime
            for i in range(4):
                if self.topCards[i].isClicked():
                    selectedCard = i
            if selectedCard != None:
                for i in range(4):
                    if i == selectedCard:
                        self.topCards[i].setBorderThickness(10)
                    else:
                        self.topCards[i].setBorderThickness(1.5)
                self.win.flip()
        correctAnswer = selectedCard == self.correctTopCardIndex
        return correctAnswer, reactionElapsedTimeMouse, rule

    def runTest(self, shapes, sizes, numbers):
        self.clearCards()
        self.win.flip()
        
        self.cTop = Card(Card.colors[0],numbers[0],shapes[0],sizes[0])
        self.wTop1 = Card(Card.colors[0],numbers[1],shapes[1],sizes[1])
        self.wTop2 = Card(Card.colors[0],numbers[2],shapes[2],sizes[2])
        self.wTop3 = Card(Card.colors[0],numbers[3],shapes[3],sizes[3])
        self.cBottom = Card(Card.colors[0],numbers[0],shapes[0],sizes[0])
            
        self.selectCards()
        self.visualizeCards()
        self.win.flip()
        





