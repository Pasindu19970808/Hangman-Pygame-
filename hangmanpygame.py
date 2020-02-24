import pygame
from random import randint
from string import ascii_lowercase

wordlist = open('hangman.txt')

smallest = None
biggest = None
secretwords = []
for word in wordlist:
    secretwords.append(word.strip())
    if smallest is None:
        smallest = len(word.strip())
    elif len(word.strip()) < smallest:
        smallest = len(word.strip())
    if biggest is None:
        biggest = len(word.strip())
    elif len(word.strip()) > biggest:
        biggest = len(word.strip())

amountofwords = len(secretwords)        
#attempts for this game will be fixed
remainingattempts = 6
#Minimum length
def get_minimumlength():
    while True:
        #statement = "Enter the minimum length you prefer: Has to be between {0} ".format(smallest) + "and {0}".format(biggest)
        min_length = input("Enter the minimum length you prefer: Has to be between {0} ".format(smallest) + "and {0}:".format(biggest))
        try:
            min_length = int(min_length)
            if min_length >= smallest and min_length <= biggest:
                return min_length
            else:
                print(str(min_length) + " is not between {0}".format(smallest) + " and {0}".format(biggest))
        except ValueError:
            print (str(min_length) + " is not an integer between {0}".format(smallest) + " and {0}".format(biggest))
            
minimum_length = get_minimumlength()

pygame.init()
screen = pygame.display.set_mode((1000,800))
pygame.display.set_caption("Hangman")
hangmanicon = pygame.image.load("hangman-game.png")
pygame.display.set_icon(hangmanicon)
backgroundIMG = pygame.image.load("background.png")
#hangmanpole = pygame.image.load('initial.png')
#displayfont = pygame.font.Font(pygame.font.get_default_font(),64)

#loading the images
penalties = list()
for i in range(remainingattempts + 1):
    penalties.append(pygame.image.load('hangman'+str(i)+'.png'))
    


#gives the hidden format of the guessword
def initializeword(secretwords,minimum_length):
    idx = []
    temp0 = []
    while True:
        guessword = secretwords[randint(0,amountofwords)]
        if len(guessword)>= minimum_length:
            for (k,v) in enumerate(guessword):
                if guessword[k] in ascii_lowercase:
                    temp0.append("*")
                    idx.append(False)
            hiddenword = "".join(temp0)
            return{'initialized':hiddenword,'index':idx,'guessword':guessword}
            
            
def processword(pressedkey,indx,guessword,remainingattempts,guessed,displayword):    
        paused = False
        displayevent0 = pygame.USEREVENT + 1
        displayevent1 = pygame.USEREVENT + 2
        displayevent2 = pygame.USEREVENT + 3
        displayevent3 = pygame.USEREVENT + 4 
        if (pressedkey not in guessed) and (pressedkey in ascii_lowercase) and (pressedkey in guessword):
            remainingattempts = remainingattempts
            paused = True
            guessed.append(pressedkey)
            displaywordtemp = list(displayword)
            position = [i for i, f in enumerate(guessword) if f == pressedkey]
            for val0 in position:
                indx[val0] = True
                displaywordtemp[val0] = pressedkey
            pygame.time.set_timer(displayevent3,1000)
            while paused is True:
                errormsg3 = pygame.font.SysFont('candara',30).render("Well done! You guessed correct. Enter your next guess",True,(255,255,255))
                screen.blit(errormsg3,(100,400))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == displayevent3:
                        pygame.time.set_timer(displayevent3,0)
                        paused = False   
            takeinletterstate = True
            displayword = "".join(displaywordtemp)
            return{'index':indx,'displayword':displayword,'guessedletters':guessed,'remattempts':remainingattempts,'takeinletterstate':takeinletterstate}
            
        elif (pressedkey in guessed) and (pressedkey in ascii_lowercase):
            remainingattempts = remainingattempts
            paused = True
            pygame.time.set_timer(displayevent0,1000)
            while paused is True:
                errormsg0 = pygame.font.SysFont('candara',30).render("You've guessed this letter before. Enter your next guess",True,(255,255,255))
                screen.blit(errormsg0,(100,400))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == displayevent0:
                        pygame.time.set_timer(displayevent0,0)
                        paused = False
            takeinletterstate = True
            return{'index':indx,'displayword':displayword,'guessedletters':guessed,'remattempts':remainingattempts,'takeinletterstate':takeinletterstate}
            
        elif (pressedkey not in guessword) and (pressedkey in ascii_lowercase): 
            remainingattempts = remainingattempts - 1
            #screen.blit(penalties[remainingattempts],(310,507))
            paused = True
            pygame.time.set_timer(displayevent1,1000)
            while paused is True:
                errormsg1 = pygame.font.SysFont('candara',30).render("This is a wrong guess. Enter your next guess",True,(255,255,255))
                screen.blit(errormsg1,(100,400))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == displayevent1:
                        pygame.time.set_timer(displayevent1,0)
                        paused = False
            takeinletterstate = True
            return{'index':indx,'displayword':displayword,'guessedletters':guessed,'remattempts':remainingattempts,'takeinletterstate':takeinletterstate}
            
        elif (pressedkey not in ascii_lowercase):
            remainingattempts = remainingattempts - 1
            #screen.blit(penalties[remainingattempts],(310,507))
            paused = True
            pygame.time.set_timer(displayevent2,1000)
            while paused is True:
                 errormsg2 = pygame.font.SysFont('candara',30).render("This is not a letter. Enter your next guess",True,(255,255,255))
                 screen.blit(errormsg2,(100,400))
                 pygame.display.update()
                 for event in pygame.event.get():
                    if event.type == displayevent2:
                        pygame.time.set_timer(displayevent2,0)
                        paused = False
            takeinletterstate = True
            return{'index':indx,'displayword':displayword,'guessedletters':guessed,'remattempts':remainingattempts,'takeinletterstate':takeinletterstate}
                   
                
def display_word(displayword): #this is used to display the word to guess(through processing of word too)
    displaywordvar = pygame.font.SysFont('candara',30).render("Word to guess: " + displayword,True,(255,255,255))
    screen.blit(displaywordvar,(100,50))
    #pygame.display.update()


def gamewin_text(running):
    if running == True:
        winvar = pygame.font.SysFont('candara',40).render("WELL DONE! YOU WIN!",True,(255,255,255))
        screen.blit(winvar,(100,400))
        #pygame.display.update()
        
def gameover_text(guessword,running):
    if running == True:
        gameovervar = pygame.font.SysFont('candara',40).render("You Lost. The word was " + guessword,True,(255,255,255))
        screen.blit(gameovervar,(100,400))
        #pygame.display.update()


def remaining_attempts(remainingattempts):
    remattemptsvar = pygame.font.SysFont('candara',30).render("Remaining attempts: " + str(remainingattempts),True,(255,255,255))
    screen.blit(remattemptsvar,(100,10))
    #pygame.display.update()
    

    
pressedkey = None
running = True
firstrun = True
guessed = list()
takeinletterstate = True #to keep the pressedkey to only one input and event
firstguess = True
while running:
        
    if firstrun is True:
        result0 = initializeword(secretwords,minimum_length)
        indx = result0['index']
        displayword = result0['initialized'] #the output from initialize word is a string, but we make it to a list
        guessword = result0['guessword']
        
    #display_word(displayword)
    screen.fill((0,0,0))
    screen.blit(backgroundIMG,(0,0)) 
    screen.blit(penalties[remainingattempts],(310,507))
    remaining_attempts(remainingattempts)
    display_word(displayword)  
    
    #place all wordprocessing functions here 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()
        if event.type == pygame.KEYDOWN and (takeinletterstate == True) and (firstrun == False):
            pressedkey = event.unicode
            takeinletterstate = False
            
    if (takeinletterstate is False) and (running is True) and (False in indx) and (firstrun == False) and (remainingattempts >= 1):
        result1 = processword(pressedkey,indx,guessword,remainingattempts,guessed,displayword)
        indx = result1['index']
        displayword = result1['displayword']
        guessed = result1['guessedletters']
        remainingattempts = result1['remattempts']
        takeinletterstate = result1['takeinletterstate']
    elif remainingattempts >= 1 and False not in indx:
        gamewin_text(running)
    elif remainingattempts == 0 and False in indx:
        gameover_text(guessword,running)
        
        
    firstrun = False
    if running == True:
       pygame.display.update()