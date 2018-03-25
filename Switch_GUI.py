#!/usr/bin/python3.4

from tkinter import *
import RPi.GPIO as GPIO
import time
import pygame
from functools import partial
class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        
        pygame.init()
        pygame.mixer.init()
        self.chime = pygame.mixer.Sound('success_sound.wav')
        self.failSnd = pygame.mixer.Sound('8_button_failure_short.wav')
        self.clickSnd = pygame.mixer.Sound('8_button_click_b.wav')
        
        #vars
        self.locked = True
        self.code = ['1', '2', '1', '2', '1', '2', '1', '2']
        self.progress = 0
        self.pressed = ''

        self.create_widgets()
        self.PiButtons()
        self.bttn1

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(5, GPIO.OUT)
        GPIO.setup(2, GPIO.OUT)
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(2, GPIO.LOW)

        #button states
        self.state1 = True
        self.state2 = True
        self.state3 = True
        self.state4 = True
        self.state5 = True
        self.state6 = True
        self.state7 = True
        self.state8 = True
        

        
        
    def create_widgets(self):
        #labels
        self.lbl = Label(self, text = "Status: Locked")
        self.lbl.grid(row = 0, column = 1)
        self.lbl1 = Label(self, text = "Code Entered: ")
        self.lbl1.grid(row = 1, column = 1)
        for x in self.code:
            self.lbl1['text'] += "*"
            
        
        #buttons
        self.bttn = Button(self, text = "Reset Entry", command = self.Reset)
        self.bttn.grid(row = 2, column = 0)
        #text will change between Lock and Unlock
        self.bttn1 = Button(self, text = "Unlock", command = self.ToggleLock)
        self.bttn1.grid(row = 2, column = 2)
        #number pad
        self.bttnum1 = Button(self, text = "1", command = partial(self.PressButton, "1"))
        self.bttnum1.grid(row = 3, column = 0)
        self.bttnum2 = Button(self, text = "2", command = partial(self.PressButton, "2"))
        self.bttnum2.grid(row = 3, column = 2)
        self.bttnum3 = Button(self, text = "3", command = partial(self.PressButton, "3"))
        self.bttnum3.grid(row = 4, column = 0)
        self.bttnum4 = Button(self, text = "4", command = partial(self.PressButton, "4"))
        self.bttnum4.grid(row = 4, column = 2)
        self.bttnum5 = Button(self, text = "5", command = partial(self.PressButton, "5"))
        self.bttnum5.grid(row = 5, column = 0)
        self.bttnum6 = Button(self, text = "6", command = partial(self.PressButton, "6"))
        self.bttnum6.grid(row = 5, column = 2)
        self.bttnum7 = Button(self, text = "7", command = partial(self.PressButton, "7"))
        self.bttnum7.grid(row = 6, column = 0)
        self.bttnum8 = Button(self, text = "8", command = partial(self.PressButton, "8"))
        self.bttnum8.grid(row = 6, column = 2)

    def PiButtons(self):
        #GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(3, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		#button position 8
        GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		#button position 6
        GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		#button position 3
        GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		#button position 1
        GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		#button position 5
        GPIO.setup(10, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		#button position 2
        GPIO.setup(9, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		#button position 4
        GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		#button position 7

        self.button1 = GPIO.input(27)
        self.button2 = GPIO.input(10)
        self.button3 = GPIO.input(17)
        self.button4 = GPIO.input(9)
        self.button5 = GPIO.input(22)
        self.button6 = GPIO.input(4)
        self.button7 = GPIO.input(11)
        self.button8 = GPIO.input(3)
        
        
        if self.button1 == False:
            if self.state1:
                self.PressButton("1")
                self.state1 = False
        else:
            self.state1 = True
            
        if self.button2 == False:
            if self.state2:
                self.PressButton("2")
                self.state2 = False
        else:
            self.state2 = True
            
        if self.button3 == False:
            if self.state3:
                self.PressButton("3")
                self.state3 = False
        else:
            self.state3 = True
            
        if self.button4 == False:
            if self.state4:
                self.PressButton("4")
                self.state4 = False
        else:
            self.state4 = True
            
        if self.button5 == False:
            if self.state5:
                self.PressButton("5")
                self.state5 = False
        else:
            self.state5 = True
            
        if self.button6 == False:
            if self.state6:
                self.PressButton("6")
                self.state6 = False
        else:
            self.state6 = True
            
        if self.button7 == False:
            if self.state7:
                self.PressButton("7")
                self.state7 = False
        else:
            self.state7 = True
            
        if self.button8 == False:
            if self.state8:
                self.PressButton("8")
                self.state8 = False
        else:
            self.state8 = True
        self.PiButtons
        
        
    def Reset(self):
        self.progress = 0
        self.lbl1['text'] = "Code Entered: "
        for x in range(len(self.code)):
            self.lbl1['text'] += "*"

    def ToggleLock(self):
        #GPIO out
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(2, GPIO.OUT)
        GPIO.setup(5, GPIO.OUT)
        
        GPIO.output(2, GPIO.HIGH)

        
        
        if self.locked:
            self.chime.play()
            GPIO.output(5, GPIO.LOW)
            self.locked = False
            self.lbl['text'] = "Status: Unlocked"
            self.bttn1['text'] = "Lock"
        else:
            GPIO.output(5, GPIO.HIGH)
            self.locked = True
            self.lbl['text'] = "Status: Locked"
            self.bttn1['text'] = "Unlock"
        
        GPIO.output(2, GPIO.LOW)
        self.progress = 0

    def PressButton(self, val):
        self.pressed = val
        print(self.pressed)
        self.CheckProgress()
        
    def CheckProgress(self):
        #Relock
        if self.locked == False:
            self.ToggleLock()
        
        if self.pressed == self.code[self.progress]:
            self.clickSnd.play()
            self.lbl1['text'] = "Code Entered: "
            for x in range(len(self.code)):
                if x <= self.progress:
                    self.lbl1['text'] += self.code[x]
                else:
                    self.lbl1['text'] += "*"
            self.progress += 1
            
        else:
            self.failSnd.play()
            self.progress = 0
            self.lbl1['text'] = "Code Entered: "
            for x in range(len(self.code)):
                self.lbl1['text'] += "*"

        #code is complete
        if self.progress == len(self.code):
            self.ToggleLock()
            self.lbl1['text'] = "Code Entered: "
            for x in range(len(self.code)):
                self.lbl1['text'] += "*"
        
            

#main
root = Tk()
root.title("Switch Remote")
root.geometry('325x200')

app = Application(root)
root.mainloop()
