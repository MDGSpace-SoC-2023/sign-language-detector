
# Live Sign Language Detector with Quiz
This project is of tkinter based GUI app that can be used to do live sign language detection alongsode of which it ther is a quiz feautre that gives a user an interactive way to learn sign language 

# Features 
* The `main.py` is a live sign language translation app that will when user will make a certain sign based on american sign language , the user can see the it translated it on to text on the given panel . 
* The `quiz.py` is a quiz app where there is a first a start button , on starting the quiz the quiz will get started then the question asking the user to make a specific sign will be asked , the user will make the required and then click on capture image the captuered image is passed to the model and on verifying the option to move to the next option activates , there is a skip option in case the user don't know the sign , finally a total score is given and the total time  the user took to complete the quiz.

# Screenshots

# Link to Demo Video 

# Installation 

* First clone the library using :
`git clone https://github.com/MDGSpace-SoC-2023/sign-language-detector.git`

* then `cd sign-language-detector`

* now create  a virtual environment and download the following dependencies :

these are also given in training notebook  , if still some module is not Installed then knidly install it 
* Then download the model and required files from the following link and paste the folder in the same directory :

* Now ,run `main.py` for the live sign language translation 
* Or run    `quiz.py` for the quiz .

NOTE :
* At a time either of one the app will run , both can't be run together 
* Also, currently the model is trained for letter [A,B,C,D,E,F] as it was computationally heavy to train all the alphabets and having great accuracy (Only these 6 letters required around 40000 steps for having this accuracy which still needs to be better) 


