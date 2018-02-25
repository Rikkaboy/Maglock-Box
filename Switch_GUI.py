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
        GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(10, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(9, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)

        self.button1 = GPIO.input(3)
        self.button2 = GPIO.input(4)
        self.button3 = GPIO.input(17)
        self.button4 = GPIO.input(27)
        self.button5 = GPIO.input(22)
        self.button6 = GPIO.input(10)
        self.button7 = GPIO.input(9)
        self.button8 = GPIO.input(11)
        
        
        if self.button1 == False:
            self.PressButton("1")
        if self.button2 == False:
            self.PressButton("2")
        if self.button3 == False:
            self.PressButton("3")
        if self.button4 == False:
            self.PressButton("4")
        if self.button5 == False:
            self.PressButton("5")
        if self.button6 == False:
            self.PressButton("6")
        if self.button7 == False:
            self.PressButton("7")
        if self.button8 == False:
            self.PressButton("8")
        self.after(250, self.PiButtons)
        
        
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
        
        time.sleep(12)
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
