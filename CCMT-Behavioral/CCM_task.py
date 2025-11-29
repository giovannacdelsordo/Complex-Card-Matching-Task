from psychopy import visual, core, event, gui
from libcard import Card
from librule import RULE
from psychopy.iohub import launchHubServer
from psychopy.iohub.util import hideWindow, showWindow
import csv
import time
import time
import random

def exitIfEscPressed():
    if event.getKeys(keyList=["escape"]):
        core.quit()

def showTextAndWaitSpace(text):
    textBox0.text = text
    textBox0.autoDraw = True
    win.flip()
    textBox0.autoDraw = False
    event.waitKeys(keyList=["space"])

def showTextAndWait(text, time):
    textBox0.text = text
    textBox0.autoDraw = True
    win.flip()
    textBox0.autoDraw = False
    core.wait(time)
    
def showTextImgTextAndWaitSpace(text0, pos0, text1, pos1, image, pos, size):
    textBox0.text = text0
    textBox0.pos = pos0
    image0.image = image
    image0.pos = pos
    image0.size = size
    textBox1.text = text1
    textBox1.pos = pos1
    textBox0.autoDraw = True
    textBox1.autoDraw = True
    image0.autoDraw = True
    win.flip()
    textBox0.autoDraw = False
    textBox1.autoDraw = False
    image0.autoDraw = False
    event.waitKeys(keyList=["space"])

def showTextTextAndWaitSpace(text0, pos0, text1, pos1):
    textBox0.pos = pos0
    textBox0.text = text0
    textBox1.pos = pos1
    textBox1.text = text1
    textBox0.autoDraw = True
    textBox1.autoDraw = True
    win.flip()
    textBox0.autoDraw = False
    textBox1.autoDraw = False
    event.waitKeys(keyList=["space"])

def checkNoConsecutive(l):
    n = len(l)
    for i in range(n-1):
        if l[i] == l[i+1]:
            return False
    return True

def showTextAndWaitSpace(text):
    textBox.text = text
    textBox.autoDraw = True
    win.flip()
    textBox.autoDraw = False
    event.waitKeys(keyList=["space"])

def fixationCrossProcedure(cross):
    cross.autoDraw = True
    win.flip()
    cross.autoDraw = False

def runExperiment(numberOfBlocks,numberOfTrialsPerBlock,blocksRules,difficulty, record):
    # Run conditions
    for blockIdx in range(numberOfBlocks):
        rule = blocksRules[blockIdx]
        for trialIdx in range(numberOfTrialsPerBlock):
            if record: 
                showTextAndWait( "Next trial will start in 3 seconds...",1) 
                showTextAndWait( "Next trial will start in 2 seconds...",1) 
                showTextAndWait( "Next trial will start in 1 seconds...",1) 
                trialNum = trialIdx+1
                blockNum = blockIdx+1
                fixationCrossProcedure(crossTextBox)
                core.wait(fixationCrossTime)
                result, reactionTimeMouse, rule = rules.runCondition(rule, difficulty)
                core.wait(1)
                win.flip()
                rules.clearCards()
                showTextAndWait("Correct" if result else "Incorrect", 2)
                csvFile.write("{},{},{},{},{},{},{},{:.3f}\n".format(age, gender.lower(), difficulty, blockNum, trialNum, rule, int(result), reactionTimeMouse))
                csvFile.flush()
            else: # Do not save data for practice trials
                fixationCrossProcedure(crossTextBox)
                core.wait(fixationCrossTime)
                result, reactionTimeMouse, rule = rules.runCondition(rule, difficulty)
                core.wait(1)
                win.flip()
                rules.clearCards()
                showTextAndWait("Correct" if result else "Incorrect", 2)
            exitIfEscPressed() # Task can be escaped during the feedback presentation

# User information
userInfoDlg = gui.Dlg(title="Participant information")
userInfoDlg.addField("Participant number")
userInfoDlg.addField("Age")
userInfoDlg.addField("Gender", choices=["Male", "Female", "Other"])
participantNumber, age, gender = None, None, None
while not (participantNumber and age and gender):
    userInfoDlg.show()
    if userInfoDlg.OK == False:
        core.quit()
    participantNumber, age, gender = userInfoDlg.data

# File name name for behavioral data
studyName = "CCMT"

# Create the window
win = visual.Window(units="height",
                    fullscr=True,
                    allowGUI=False,
                    colorSpace='rgb255',
                    color=[128,128,128]
                    )
w = win.size[0]/2
h = win.size[1]/2

# Create librule to choose rules and run the experiment
rules = RULE(win)

# Create the text boxes for instructions
textBox = visual.TextBox2(win, text="", autoDraw=False, pos=(0,0), alignment="center", letterHeight=0.02, size=[1.5, None])
textBox0 = visual.TextBox2(win, text="", autoDraw=False, pos=(0,0), alignment="center", letterHeight=0.02, size=[1.5, None])
textBox1 = visual.TextBox2(win, text="", autoDraw=False, pos=(0,0), alignment="center", letterHeight=0.02, size=[1.5, None])
crossTextBox = visual.TextBox2(win, text="+", pos=(0,0), color="white", alignment="center", autoDraw=False, letterHeight=0.025)

# Create the image for instructions
image0 = visual.ImageStim(win)
defaultImageSize = (0.5,0.4)

# Fixation cross, baseline recording before each trial in seconds
fixationCrossTime = 2

# INSTRUCTIONS
# Welcome page
showTextAndWaitSpace("Welcome to this experiment.\n\n\n" +
                     "Press the space bar to continue")
showTextAndWaitSpace("There is two different games in this experiment that will play one after the other.\n" +
                    "When you see instructions, make sure to read carefully as the instructions will slightly differ between the two games.\n" +
                     "Press the space bar to continue")

# First instruction page
showTextImgTextAndWaitSpace("In this experiment, you will be playing a card sorting game.\n" +
                            "You will see 4 cards at the top of the screen and 1 at the bottom, like in the example below.",
                            (0,0.3),
                            "Press the space bar to continue",
                            (0,-0.4),
                            "shape.png",
                            (0, 0),
                            defaultImageSize)

# Create CVS file for behavioral data
fileName = "{}{}.csv".format(studyName, participantNumber)
csvFile = open(fileName,"w")
csvFile.write("{},{},{},{},{},{},{},{}\n".format("age", "gender","difficulty", "blockNumber", "trialNumber", "rule", "accuracy", "reactionTime"))
csvFile.flush()

# Difficulty selection, counterbalanced between participants
difficulties = rules.difficulties
random.shuffle(difficulties)

for difficulty in difficulties:
    if difficulty == "easy":
        # Second instruction page
        showTextImgTextAndWaitSpace("In this game you will be required to sort the presented cards based on a rule\n i.e. the cards will have to be sorted based on either the color of the shapes, the shapes, or the number of shapes.\n\n" +
                                "In some cases, the rule will be a combination of two rules such as: color-shape, color-number of shapes, or shape-number of shapes.\n" +
                                "You will have to guess the rule being played and match the bottom card with one of the four cards at the top.\n",
                                (0,0.25), 
                                "Press the space bar to continue",
                                (0,-0.4),
                                "easy_color_number.png",
                                (0, -0.15),
                                defaultImageSize)
        
        showTextImgTextAndWaitSpace("The rule will not be given to you, however you will receive feedback on each trial to let you know if you were right or wrong in guessing the current rule.\n"  +
                                "If the feedback is incorrect, you need to adjust your answer (try another rule). If it is correct, you can keep answering using the same rule.\n" +
                                "After a certain number of trials the rule will change to a different one but you won't be told when it is\n (this means that for X number of trials, the same rule will be played).\n" + 
                                "To select your response: click on one of the four cards presented at the top of the screen (you cannot change your choice after clicking!).\n" +
                                "Try your best to guess what rule is being played on each trial and please privilege accuracy rather than speed.\n" +
                                "Let's look at an example.", 
                                (0,0.3), 
                                "Press the space bar to continue",
                                (0,-0.4),
                                "easy_color_number.png",
                                (0, -0.15),
                                defaultImageSize)
        
        # Third instruction page
        showTextImgTextAndWaitSpace("In this example, the bottom card has the following characteristics: red, square, 4 shapes.\n" +
                                    "By trial and error, you need to guess which of the 6 possible rules is being played.\n" +
                                    "Remember that the 6 rules are: color, shape, number of shapes, color-shape, color-number of shapes, or shape-number of shapes.\n" +
                                    "The 1st, and 3rd top cards follow the color rule. However, only one correct answer is possible.\n" +
                                    "It could be the number rule, but the 1st and 4th top cards would correspond so this is not the correct answer.\n" +
                                    "The only unique answer is to consider the color-number rule and that would be correct.\n The first card at the top has both the same color and same number of shapes as the bottom card.\n",
                                    (0,0.3),
                                    "Press the space bar to continue",
                                    (0,-0.4),
                                    "easy_color_number.png",
                                    (0, -0.15),
                                    defaultImageSize)
                                    
        # Fourth page instruction
        showTextImgTextAndWaitSpace("Let's look at another example.\n" +
                                    "Here, the bottom card has the following characteristics: yellow, square, 1 shape. \n" + 
                                    "The rule could be color, but two top cards match this rule (1st and 4rd cards).\n" + 
                                    "The rule could be shape, but three top cards also match this rule (1st, 3rd, and 4th cards).\n" +
                                    "The correct answer is to click on the third top card as the only solution left is to apply the number of shapes rule (1 shape).",
                                    (0,0.3),
                                    "Press the space bar to continue",
                                    (0,-0.4),
                                    "easy_number_shape.png",
                                    (0, -0.15),
                                    defaultImageSize)
        
        # Fifth page instruction
        showTextTextAndWaitSpace("You will have 6 seconds to guess what rule is being played.\n" + 
                                "To choose an answer, you need to click on one of the top cards.\n" +
                                "After each choice you make you will receive feedback on the correctness of your answer.\n" +
                                "You will not know when the rule is going to change.\n" +
                                "Please remember to try your best to be as accurate as possible.\n" +
                                "You are going to start with some practice trials. Let the researcher know if you have any question at this point",
                                (0,0), 
                                "Press the space bar to continue",
                                (0,-0.4))
        
        # Practice trials set up
        numberOfBlocks = 0#2 # Change the number of blocks (remember: each block contains several trials)
        numberOfTrialsPerBlock = 6 # Change the number of trials within each block
        blocksRules = rules.easyRules
        random.shuffle(blocksRules)
        runExperiment(numberOfBlocks,numberOfTrialsPerBlock,blocksRules,difficulty,False)

        # More instructions for rules before the real trials
        showTextTextAndWaitSpace("It is important that you remember the possible rules. Take a minute to remember the rules.\n" + 
                                " There are 6 rules:.\n\n\n" +
                                "- Match cards based on their color only (blue, green, red, yellow).\n\n" +
                                "- Match cards based on their shapes only (square, diamond, circle, triangle).\n\n" +
                                "- Match cards based on their number of shapes only (1,2,3,4).\n\n" +
                                "- Match cards based on 2 rules combined: color and shape.\n\n" +
                                "- Match cards based on 2 rules combined: color and number of shapes.\n\n" +
                                "- Match cards based on 2 rules combined: shape and shape number of shapes.\n\n",
                                (0,0), 
                                "Press the space bar to continue",
                                (0,-0.4))
        
        # Real trials instructions
        showTextAndWaitSpace("The real experiment is now going to start.\n" +
                                "This part of the game will take around 15 minutes.\n\n" +
                                "Press the space bar to start.")
        
        numberOfBlocks = 2#6 # Change number of blocks
        numberOfTrialsPerBlock = 2#10 # Change number of trials per block
        blocksRules = rules.easyRules + rules.easyRules
        random.shuffle(blocksRules)
        while not checkNoConsecutive(blocksRules):
            random.shuffle(blocksRules) 
        runExperiment(numberOfBlocks,numberOfTrialsPerBlock,blocksRules,difficulty,True)
        
    elif difficulty == "hard":
        
        # Second instruction page
        showTextImgTextAndWaitSpace("In this game you will be required to sort the presented cards based on a rule i.e. the cards will have to be sorted based on the combimation of TWO characteristics:\n" +
                                "the color of the presented shapes, the shapes, the number of shapes, the size of shapes.\n\n" +
                                "The rule will be a combination of two rules such as: color-shape, color-number, shape-number, color-size, shape-size, number-size.\n" +
                                "You will have to guess the rule being played and match the bottom card with one of the cards at the top.", 
                                (0,0.25), 
                                "Press the space bar to continue",
                                (0,-0.4),
                                "hard_size_shape.png",
                                (0, -0.15),
                                defaultImageSize)
                                
        showTextImgTextAndWaitSpace("The rule will not be given to you, however you will receive feedback on each trial to let you know if you were right or wrong in guessing the current rule.\n"  +
                                "If the feedback is incorrect, you need to adjust your answer (try another rule). If it is correct, you can keep answering using the same rule.\n" +
                                "After a certain number of trials the rule will change to a different one but you won't be told when it is (this means that for X number of trials, the same rule will be played).\n" + 
                                "To select your response: click on one of the four cards presented at the top of the screen (you cannot change your answer after clicking!).\n" +
                                "Try your best to guess what rule is being played on each trial and please privelege accuracy rather than speed." +
                                "Let's look at an example.", 
                                (0,0.3), 
                                "Press the space bar to continue",
                                (0,-0.4),
                                "hard_size_shape.png",
                                (0, -0.15),
                                defaultImageSize)
        
        # Third instruction page
        showTextImgTextAndWaitSpace("In this example, the bottom card has the following characteristics: orange, circle, 4 shapes, small size.\n" +
                                    "By trial and error, you need to guess which of the 6 possible rules is being played.\n" +
                                    "The 2nd and 4th cards follow the shape-number rule. However, only one correct answer is possible.\n" +
                                    "The rule could be number and size (four and small) but let's say that you try this rule and you get an 'incorrect' feedback.\n" +
                                    "It means that you should try another rule.\n" +
                                    "Another possibility is to consider the shape-size rule and that would be correct. The third card at the top has both the same shape and same size as the bottom card.",
                                    (0,0.3),
                                    "Press the space bar to continue",
                                    (0,-0.4),
                                    "hard_size_shape.png",
                                    (0, -0.15),
                                    defaultImageSize)
                                    
        
        # Fourth page instruction
        showTextImgTextAndWaitSpace("Let's look at another example.\n" +
                                    "Here, the bottom card has the following characteristics: orange, square, 3, medium size. \n" + 
                                    "The rule could be color-size (orange and medium size), but two top cards match this rule (1st and 4rd cards).\n" + 
                                    "The rule could be color and shape (orange and square) but let's say that you try this rule and you get an 'incorrect' feedback.\n" +
                                    "It means that you should try another rule.\n" +
                                    "The correct answer is to click on the third top card as the solution left is to apply the color-number rule (orange and 3 shapes).",
                                    (0,0.3),
                                    "Press the space bar to continue",
                                    (0,-0.4),
                                    "hard_color_number.png",
                                    (0, -0.15),
                                    defaultImageSize)
        
        # Fifth page instruction
        showTextTextAndWaitSpace("You will have 6 seconds to guess what rule is being played.\n" + 
                                "To choose an answer, you need to click on one of the top cards and to press space to confirm your choice.\n" +
                                "After each choice you make you will receive feedback on the correctness of your answer." +
                                "You will not know when the rule is going to change.\n" +
                                "Please remember to try your best to be as accurate as possible, rather than fast.\n" +
                                "You are going to start with some practice trials. Let the researcher know if you have any question at this point",
                                (0,0), 
                                "Press the space bar to continue",
                                (0,-0.4))
        
        # Practice trials configuration
        numberOfBlocks = 0#2 # Change the number of blocks
        numberOfTrialsPerBlock = 6 # Change the number of trials per block
        blocksRules = rules.hardRules
        random.shuffle(blocksRules)
        runExperiment(numberOfBlocks,numberOfTrialsPerBlock,blocksRules,difficulty,False)

        # Instructions for rules
        showTextTextAndWaitSpace("It is important that you remember the possible rules. Take a minute to remember the rules.\n" + 
                                " There are 6 rules:\n\n\n" +
                                "- Match cards based on 2 rules combined: color and shape.\n\n" +
                                "- Match cards based on 2 rules combined: color and number of shapes.\n\n" +
                                "- Match cards based on 2 rules combined: color and size of shapes.\n\n" +
                                "- Match cards based on 2 rules combined: shape and shape number of shapes.\n\n" +
                                "- Match cards based on 2 rules combined: shape and size of shapes.\n\n" +
                                "- Match cards based on 2 rules combined: number of shapes and size of shapes.",
                                (0,0), 
                                "Press the space bar to continue",
                                (0,-0.4))


        # Real trials instructions
        showTextAndWaitSpace("The real experiment is now going to start.\n" +
                                "This part of the game will take around 15 minutes.\n\n" +
                                "Press the space bar to start.\n\n")
        
        numberOfBlocks = 2#6 # Change the number of blocks
        numberOfTrialsPerBlock = 2#10 # Change the number of trials within each block
        blocksRules = rules.hardRules + rules.hardRules
        random.shuffle(blocksRules)
        while not checkNoConsecutive(blocksRules):
            random.shuffle(blocksRules) 
        runExperiment(numberOfBlocks,numberOfTrialsPerBlock,blocksRules,difficulty,True)
    else:
        print("Difficulty not supported: {}".format(difficulty))
        core.quit()

csvFile.close()

showTextAndWaitSpace("Thank you for participating.\n\n\n" +
                    "Please tell the researcher that you are done.\n" +
                     "Researcher: Press the space bar to end the task")
 
core.quit()
