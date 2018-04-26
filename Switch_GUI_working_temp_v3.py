#!/usr/bin/python3.4
import time
time.sleep(1)

from tkinter import *
import RPi.GPIO as GPIO
#import time
import pygame
from functools import partial
class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        
        pygame.init()
        pygame.mixer.init()
        self.success = pygame.mixer.Sound('success_sound.wav')
        self.failSnd = pygame.mixer.Sound('8_button_failure_short.wav')
        self.clickSnd = pygame.mixer.Sound('8_button_click_b.wav')
		self.success1 = pygame.mixer.Sound('8b-success1.wav')
		self.success2 = pygame.mixer.Sound('8b-success2.wav')
		self.success3 = pygame.mixer.Sound('8b-success3.wav')
		self.success4 = pygame.mixer.Sound('8b-success4.wav')
		self.success5 = pygame.mixer.Sound('8b-success5.wav')
		self.success6 = pygame.mixer.Sound('8b-success6.wav')
		self.success7 = pygame.mixer.Sound('8b-success7.wav')
		self.success8 = pygame.mixer.Sound('8b-success8.wav')
		self.success9 = pygame.mixer.Sound('8b-success9open.wav')
		self.fail0 = pygame.mixer.Sound('8b-fail-0.wav')
		self.fail1 = pygame.mixer.Sound('8b-fail-1.wav')
		self.fail2 = pygame.mixer.Sound('8b-fail-2.wav')
		self.fail3 = pygame.mixer.Sound('8b-fail-3.wav')
        
        #vars
        self.locked = True
        self.code = ['2', '7', '4', '5', '8', '1', '3', '8', '6']
        self.progress = 0
        self.pressed = ''
		

        self.create_widgets()
        self.PiButtons()
        self.bttn1
		self.buttonSnd = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(5, GPIO.OUT)
        #GPIO.setup(2, GPIO.OUT) #this is used for an LED indicator
        GPIO.output(5, GPIO.HIGH)
        

        
        
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

        #changed button positions
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
        GPIO.setup(5, GPIO.OUT)

        
        
        if self.locked:
            self.success9.play()
						
            time.sleep(2.5) #to have the drawer open 3 seconds into the sound. Needs tested.
			GPIO.output(5, GPIO.LOW)
            self.locked = False
            self.lbl['text'] = "Status: Unlocked"
            self.bttn1['text'] = "Lock"
        else:
            GPIO.output(5, GPIO.HIGH)
            self.locked = True
            self.lbl['text'] = "Status: Locked"
            self.bttn1['text'] = "Unlock"
        
        time.sleep(6)
        self.progress = 0

    def PressButton(self, val):
        self.pressed = val
        print(self.pressed)
		#print(self.progress+1)
        self.CheckProgress()
        
    def CheckProgress(self):
        #Relock
        if self.locked == False:
            self.ToggleLock()
        
        if self.pressed == self.code[self.progress]:
            #self.clickSnd.play()
			#play music for how long they have successes
			if self.progress == 0:
				self.success1.play()
			if self.progress == 1:
				self.success2.play()
			if self.progress == 2:
				self.success3.play()
			if self.progress == 3:
				self.success4.play()
			if self.progress == 4:
				self.success5.play()
			if self.progress == 5:
				self.success6.play()
			if self.progress == 6:
				self.success7.play()
			if self.progress == 7:
				self.success8.play()
            time.sleep(1)
            self.lbl1['text'] = "Code Entered: "
            for x in range(len(self.code)):
                if x <= self.progress:
                    self.lbl1['text'] += self.code[x]
                else:
                    self.lbl1['text'] += "*"
            self.progress += 1
            
        else:
            self.fail2.play()
			time.sleep(2)
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
