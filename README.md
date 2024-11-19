This repository contains PsychoPy to run the Complex Card Matching Task (CCMT), a cognitive flexibility task to investigate the exploration-exploitation trade-off at different
difficulty levels. It also contains Python notebook to pre-process data after data collection was performed. 

For more detailed information about the task and how to use it, please read: (cite article)

Note that you will need to install PsychoPy (https://www.psychopy.org/) to run the task. The task can be run on Windows, MacOS, and Linux. 

Two versions of the task are available: 

(1) _CCMT - Behavioral_: this version can run on any computer and does not require any other hardware. Collected data is only behavioral (accuracy, reaction time). 

(2) _CCMT - Pupillometry_: this version is specifically designed to be used with an EyeLink eye-tracker to record pupil size measures. A connected eye-tracker is necessary to run this task.
The code can be changed to adapt to other types of eye-tracker (e.g. Tobii). For each participants, two files are created: a behavioral data set (.csv) and a pupillometry dataset (.edf). 
The EDF file must be converted using the EyeLink Data Viewer before further processing (https://www.sr-research.com/). 

Python notebooks were created, one for handling the behavioral data and one for handling the pupillometry data. The purpose of these notebokks is to classify each trial within each 
participant file as either "Exploration" or "Exploitation". Once each file is classified, further pre-processing (for pupillometry data) or data analysis is possible from the Excel output
that are generated. 

Any part of the provided code can be changed to adjust the task to different research needs. 
