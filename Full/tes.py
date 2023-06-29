from PyQt5 import QtCore, QtWidgets, QtGui
import sys
import speech_recognition as sr
import pyttsx3
import requests

class SimpleWindow(QtWidgets.QMainWindow):

    recognized = QtCore.pyqtSignal(str)
    # Initialize the speech recognizer
    r = sr.Recognizer()

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowFlags(
            QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowStaysOnTopHint
        )
        self.setGeometry(1750, 100, 50, 50)

        # Set the background color to black
        self.setStyleSheet("background-color: black;")

        self.label = QtWidgets.QLabel()
        self.movie = QtGui.QMovie("pop.gif")
        self.label.setMovie(self.movie)
        self.movie.start()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.label)

        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(self.layout)

        self.setCentralWidget(self.central_widget)

        self.show()

        # Apply rounded shape to the window
        self.setWindowShape()

        self.recognized = QtCore.pyqtSignal(str)
        # Initialize the speech recognizer
        self.r = sr.Recognizer()

        # Connect the clicked signal to the custom slot
        self.clicked.connect(self.handle_button_click)

        # Add an attribute to store the recognized text
        self.recognized_text = None

    def setWindowShape(self):
        # Create a rounded mask
        mask = QtGui.QRegion(self.central_widget.rect(), QtGui.QRegion.Ellipse)
        self.setMask(mask)

    def mousePressEvent(self, event):
        # Emit the clicked signal when the window is clicked
        self.clicked.emit()

    # Function to speak out text
    def speak(self, text):
        engine = pyttsx3.init()
        # Set the voice ID to a female voice
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()

    def handle_button_click(self):
        # Call the print_hello function from the other_file module
        # Use the speech recognizer to convert speech to text
        try:
            with sr.Microphone() as source:
                print("Say something!")
                self.speak("Say something!")
                audio = self.r.listen(source)
                prompt = str(self.r.recognize_google(audio)).lower()
                payload = {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are Cleo, a helpful cat assistant, created by Jaideep!"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }

                headers = {
                    "content-type": "application/json",
                    "X-RapidAPI-Key": "a8a6c43cfdmsh303fe224450a8cbp1e6c35jsnc06fa427c031",
                    "X-RapidAPI-Host": "openai80.p.rapidapi.com"
                }
                url = "https://openai80.p.rapidapi.com/chat/completions"

                response = requests.post(url, json=payload, headers=headers).json()["choices"][0]["message"]["content"]

                print(response)
                self.speak(response)


        # If the speech is not recognized, ask for user input
        except sr.UnknownValueError:
            print("Speech not recognized. Please try again.")
            self.speak("Speech not recognized. Please try again.")



    clicked = QtCore.pyqtSignal()

app = QtWidgets.QApplication(sys.argv)
window = SimpleWindow()
sys.exit(app.exec_())