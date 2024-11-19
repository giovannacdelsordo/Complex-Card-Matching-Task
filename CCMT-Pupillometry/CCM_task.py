from psychopy import visual, core, event, gui
from libcard import Card
from librule import RULE
from psychopy.iohub import launchHubServer
from psychopy.iohub.util import hideWindow, showWindow
import csv
import time
import random

def exitIfEscPressed():
    if event.getKeys(keyList=["escape"]):
        tracker.setConnectionState(False)
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

def showTextAndWaitSpaceOrCalibrate(text):
    textBox.text = text
    textBox.autoDraw = True
    win.flip()
    textBox.autoDraw = False
    if "c" in event.waitKeys(keyList=["space", "c"]):
        calibrationProcedure()

def fixationCrossProcedure(cross):
    cross.autoDraw = True
    win.flip()
    cross.autoDraw = False

# Convert pixel dimensions to height units
def pixels_to_height(pixels):
    return pixels / screen_height

def calibrationProcedure():
    tracker.runSetupProcedure() 
    win.flip()

def runExperiment(numberOfBlocks,numberOfTrialsPerBlock,blocksRules,difficulty,record):
    # Run conditions
    for blockIdx in range(numberOfBlocks):
        rule = blocksRules[blockIdx]
        for trialIdx in range(numberOfTrialsPerBlock):
            showTextAndWait( "Next trial will start in 3 seconds...",1) 
            showTextAndWait( "Next trial will start in 2 seconds...",1) 
            showTextAndWait( "Next trial will start in 1 seconds...",1) 
            if record:
                tracker.sendMessage('TRIALID')
                trialNum = trialIdx+1
                blockNum = blockIdx+1
                tracker.setRecordingState(True)
                tracker.sendMessage('fixation')
                fixationCrossProcedure(crossTextBox)
                core.wait(fixationCrossTime)
                tracker.sendMessage('experiment')
                result, reactionTimeMouse, rule = rules.runCondition(rule, difficulty)
                tracker.sendMessage('response')
                core.wait(1)
                win.flip()
                rules.clearCards()
                tracker.sendMessage('feedback')
                showTextAndWait("Correct" if result else "Incorrect", 2)
                tracker.sendMessage('!V TRIAL_VAR difficulty %s' % difficulty)
                tracker.sendMessage('!V TRIAL_VAR rule %s' % rule)
                tracker.sendMessage('!V TRIAL_VAR block %s' % blockNum)
                tracker.sendMessage('!V TRIAL_VAR accuracy %s' % int(result))
                tracker.sendMessage('!V TRIAL_VAR RT %s' % reactionTimeMouse)
                tracker.sendMessage('!V TRIAL_VAR trialNumber %s' % trialNum)
                tracker.sendMessage('TRIAL_RESULT')
                tracker.setRecordingState(False)
                csvFile.write("{},{},{},{},{},{},{},{:.3f}\n".format(age, gender.lower(), difficulty, blockNum, trialNum, rule, int(result), reactionTimeMouse))
                csvFile.flush()
            else: # No eye-tracker recordings during practice trials
                fixationCrossProcedure(crossTextBox)
                core.wait(fixationCrossTime)
                result, reactionTimeMouse, rule = rules.runCondition(rule, difficulty)
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
    

# File name for Eyelink file
file_name = "CCM_{}".format(participantNumber) # Limit participant numbers to 3 numbers otherwise the task will crash

# File name name for behavioral data
studyName = "CCM_"

# Create the window
win = visual.Window(units="height",
                    fullscr=True,
                    allowGUI=False,
                    colorSpace='rgb255',
                    color=[128,128,128]
                    )
w = win.size[0] / 2
h = win.size[1] / 2

# To change calibration procedure screen to "height"
# Get screen resolution in pixels
screen_width, screen_height = win.size  # Width and height in pixels
# Define calibration target attributes in height units
outer_diameter_height = pixels_to_height(33)  # Convert outer diameter
inner_diameter_height = pixels_to_height(6)   # Convert inner diameter

# Eyetracker configuration
eyetracker_config = dict(name='tracker')
eyetracker_config['model_name'] = 'EYELINK 1000 DESKTOP'
eyetracker_config['default_native_data_file_name'] = file_name
eyetracker_config['monitor_event_types'] = ['MonocularEyeSampleEvent', 'FixationStartEvent', 'FixationEndEvent', 'BlinkStartEvent', 'BlinkEndEvent']
eyetracker_config['sample_filtering'] = dict(FILTER_ALL='FILTER_LEVEL_2')
eyetracker_config['vog_settings'] = dict(pupil_measure_types='PUPIL_DIAMETER', tracking_mode='PUPIL_CR_TRACKING', pupil_center_algorithm='ELLIPSE_FIT')
eyetracker_config['runtime_settings'] = dict(sampling_rate=250, track_eyes='RIGHT')
#eyetracker_config['calibration'] = dict(screen_background_color=[128,128,128], text_color=[0,0,0])
eyetracker_config['calibration'] = dict(
    screen_background_color=[128, 128, 128],
    text_color=[0, 0, 0],
    target_attributes=dict(
        outer_diameter=outer_diameter_height,
        inner_diameter=inner_diameter_height,
        outer_color=[255, 255, 255, 255],
        inner_color=[0, 0, 0, 255]
    ))
devices_config = dict()
devices_config['eyetracker.hw.sr_research.eyelink.EyeTracker'] = eyetracker_config

# Create librule to choose rules and run the experiment
rules = RULE(win)

# Create io hub 
io = launchHubServer(window=win, **devices_config)
tracker = io.getDevice('tracker')

# Calibration procedure
calibrationProcedure()

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
                            (0,-0.5*h),
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
                                "You will have to guess the rule being played and match the bottom card with one of the four cards at the top.",
                                (0,0.3), 
                                "Press the space bar to continue",
                                (0,-0.4),
                                "easy_color_number.png",
                                (0, -0.15),
                                defaultImageSize)
        
        showTextImgTextAndWaitSpace("The rule will not be given to you, however you will receive feedback on each trial to let you know if you were right or wrong in guessing the current rule.\n"  +
                                "If the feedback is incorrect, you need to adjust your answer (try another rule). If it is correct, you can keep answering using the same rule.\n\n" +
                                "After a certain number of trials the rule will change to a different one but you won't be told when it is\n (this means that for X number of trials, the same rule will be played).\n\n" + 
                                "To select your response: click on one of the four cards presented at the top of the screen (you cannot change your choice after clicking!).\n\n" +
                                "Try your best to guess what rule is being played on each trial and please privilege accuracy rather than speed." +
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
                                    "The only unique answer is to consider the color-number rule and that would be correct.\n The first card at the top has both the same color and same number of shapes as the bottom card.",
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
        runExperiment(numberOfBlocks,numberOfTrialsPerBlock,blocksRules,difficulty, False)

        # More instructions for rules before the real trials
        showTextTextAndWaitSpace("It is important that you remember the possible rules. Take a minute to remember the rules.\n" + 
                                " There are 6 rules:.\n\n\n" +
                                "- Match cards based on their color only (blue, green, red, yellow).\n\n" +
                                "- Match cards based on their shapes only (square, diamond, circle, triangle).\n\n" +
                                "-Match cards based on their number of shapes only (1,2,3,4).\n\n" +
                                "- Match cards based on 2 rules combined: color and shape.\n\n" +
                                "- Match cards based on 2 rules combined: color and number of shapes.\n\n" +
                                "- Match cards based on 2 rules combined: shape and shape number of shapes.\n\n",
                                (0,0), 
                                "Press the space bar to continue",
                                (0,-0.4))
        
        # Real trials instructions
        showTextAndWaitSpaceOrCalibrate("The real experiment is now going to start.\n" +
                                "We ask you that, until you see the next set of instructions, you DO NOT move your head from the headrest.\n" +
                                "Please stay as still as you can.\n" +
                                "This part of the game will take around 15 minutes.\n\n" +
                                "Participant: Please keep your hand on the mouse during the entirety of the game. \n\n" + 
                                "Researcher: press c to calibrate or space to continue.")
        
        numberOfBlocks = 2#6 # Change number of blocks
        numberOfTrialsPerBlock = 1#10 # Change number of trials per block
        blocksRules = rules.easyRules + rules.easyRules
        random.shuffle(blocksRules)
        while not checkNoConsecutive(blocksRules):
            random.shuffle(blocksRules) 
        runExperiment(numberOfBlocks,numberOfTrialsPerBlock,blocksRules,difficulty, True)
        
    elif difficulty == "hard":
        
        # Second instruction page
        showTextImgTextAndWaitSpace("In this game you will be required to sort the presented cards based on a rule i.e. the cards will have to be sorted based on the combimation of TWO characteristics:\n" +
                                "the color of the presented shapes, the shapes, the number of shapes, the size of shapes.\n\n" +
                                "The rule will be a combination of two rules such as: color-shape, color-number, shape-number, color-size, shape-size, number-size.\n" +
                                "You will have to guess the rule being played and match the bottom card with one of the cards at the top.\n\n", 
                                (0,0.3), 
                                "Press the space bar to continue",
                                (0,-0.4),
                                "hard_size_shape.png",
                                (0, -0.15),
                                defaultImageSize)
                                
        showTextImgTextAndWaitSpace("The rule will not be given to you, however you will receive feedback on each trial to let you know if you were right or wrong in guessing the current rule.\n"  +
                                "If the feedback is incorrect, you need to adjust your answer (try another rule). If it is correct, you can keep answering using the same rule.\n" +
                                "After a certain number of trials the rule will change to a different one but you won't be told when it is (this means that for X number of trials, the same rule will be played).\n\n" + 
                                "To select your response: click on one of the four cards presented at the top of the screen (you cannot change your answer after clicking!).\n\n" +
                                "Try your best to guess what rule is being played on each trial and please privelege accuracy rather than speed.\n" +
                                "Let's look at an example.", 
                                (0,0.3), 
                                "Press the space bar to continue",
                                (0,-0.4),
                                "hard_size_shape.png",
                                (0, -0.15),
                                defaultImageSize)
        
        # Third instruction page
        showTextImgTextAndWaitSpace("In this example, the bottom card has the following characteristics: orange, circle, 4 shapes, small size.\n" +
                                    "By trial and error, you need to guess what of the 10 possible rules is being played.\n" +
                                    "The 1st, 3rd and 4th cards follow the number rule. However, only one correct answer is possible.\n" +
                                    "It could be the shape rule, but the 2nd, 3rd, and 4th card would correspond si this is not the correct answer.\n" +
                                    "Another possibility is to consider the shape-size rule and that would be correct. The third card at the top has both the same shape and same size as the bottom card\n",
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
                                (0,-0.15))
        
        # Practice trials configuration
        numberOfBlocks = 0#2 # Change the number of blocks
        numberOfTrialsPerBlock = 6 # Change the number of trials per block
        blocksRules = rules.hardRules
        random.shuffle(blocksRules)
        runExperiment(numberOfBlocks,numberOfTrialsPerBlock,blocksRules,difficulty, False)

        # Instructions for rules
        showTextTextAndWaitSpace("It is important that you remember the possible rules. Take a minute to remember the rules.\n" + 
                                " There are 6 rules:\n\n\n" +
                                "- Match cards based on 2 rules combined: color and shape.\n\n" +
                                "- Match cards based on 2 rules combined: color and number of shapes.\n\n" +
                                "- Match cards based on 2 rules combined: color and size of shapes.\n\n" +
                                "- Match cards based on 2 rules combined: shape and shape number of shapes.\n\n" +
                                "- Match cards based on 2 rules combined: shape and size of shapes.\n\n" +
                                "- Match cards based on 2 rules combined: number of shapes and size of shapes.\n\n",
                                (0,0), 
                                "Press the space bar to continue",
                                (0,-0.4))


        # Real trials instructions
        showTextAndWaitSpaceOrCalibrate("The real experiment is now going to start.\n" +
                                "We ask you that, until you see the next set of instructions, you DO NOT move your head from the headrest.\n" +
                                "Please stay as still as you can.\n" +
                                "This part of the game will take around 15 minutes.\n\n" +
                                "Participant: Please keep your hand on the mouse for the entirety of the task.\n\n" +
                                "Researcher: press c to calibrate or space to continue.")
        
        numberOfBlocks = 2#6 # Change the number of blocks
        numberOfTrialsPerBlock = 1#10 # Change the number of trials within each block
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
 
tracker.setConnectionState(False)
core.quit()
