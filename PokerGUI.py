"""
PokerGUI.py
establishes the GUI for the game.
"""

from Tkinter import *
from tkMessageBox import *
from tkSimpleDialog import *
from pokerplayer import *

class StatusBar(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

class PokerWindow:
    
    def __init__ (self, master, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.turn = 0
        self.p1bet = 0
        self.p2bet = 0
        self.dice = [[], []]
        self.p1selected = []
        self.p2selected = []
        self.HEIGHT = 300
        self.WIDTH = 400
        self.root = master
        
        frame = Frame(master)
        frame.pack()
        
        self.status = StatusBar(master)
        self.status.pack(side=BOTTOM, fill=X)
        self.status.set("Welcome to Poker Dice.")
        
        self.status2 = StatusBar(master)
        self.status2.pack(side=BOTTOM, fill=X)
        self.refresh2()
                
        self.makeDice(frame)
        
    def refresh2(self):
        self.status2.set("Player 1: " + str(self.p1.funds) + ", Player 2: " + str(self.p2.funds) + ", pot: " + str(self.p1bet + self.p2bet))
        
        
    def makeDice(self, frame):
        """ Draw the dice """
        boardFrame = Frame(frame) 
        boardFrame.pack(side=TOP) 
        
        self.button = Button(frame, text="Start New Game", command=self.newgame)
        self.button.pack(side=BOTTOM) 
        
        gameFrame = Frame(boardFrame)
        p1Dice = Frame(gameFrame)
        p2Dice = Frame(gameFrame)
        p1Dice.pack(side=TOP)
        p2Dice.pack(side=BOTTOM)
        
        for i in range(5):
            c = Canvas(p1Dice, width=80, height=80)
            c.pack(side=LEFT)
            self.dice[0] += [c]    
            
            c = Canvas(p2Dice, width=80, height=80)
            c.pack(side=LEFT)
            self.dice[1] += [c]
        
        self.r = Canvas(p1Dice, width=80, height=80)
        self.r.pack(side=LEFT)
        
        self.r2 = Canvas(p2Dice, width=80, height=80)
        self.r2.pack(side=LEFT)
            
        gameFrame.pack()
        #self.enableBoard()
        
    def refresh_dice(self):
        self.p1.hand = self.p1.hand_sort(self.p1.hand)
        self.p2.hand = self.p2.hand_sort(self.p2.hand)
        for i in range(5):
            c = self.dice[0][i]
            c.create_rectangle(20, 20, 60, 60, fill="#F00")
            c.create_text(40, 40, text=self.p1.hand[i])     
            c = self.dice[1][i]
            c.create_rectangle(20, 20, 60, 60, fill="#F00")
            c.create_text(40, 40, text=self.p2.hand[i])
        
        self.r.create_rectangle(20, 20, 60, 60, fill="#00F")
        self.r.create_text(40, 40, text="Roll")   
        
        
    def select_to_roll(self, p, i):
        self.dice[p][i].create_rectangle(20, 20, 60, 60, fill="#FF0")
        if p == 0:
            self.dice[p][i].create_text(40, 40, text=self.p1.hand[i])
            self.p1selected.append(i)
        else:
            self.dice[p][i].create_text(40, 40, text=self.p2.hand[i])
            self.p2selected.append(i)
        self.dice[p][i].unbind("<Button-1>")
        
    def roll_selected(self):
        print self.p1selected
        print self.p2selected
        
        self.p1.roll(self.p1selected)
        self.p2.roll(self.p2selected)
        
        self.refresh_dice()
        
        self.betting_round()
        
        
    def enableBoard(self):
        """ Allow a human player to make moves by clicking"""
        for i in [0, 1]:
            for j in range(5):
                self.dice[i][j].bind("<Button-1>", self.callback)
        self.r.bind("<Button-1>", self.callback)
                
    def disableBoard(self):
        """ Prevent the human player from clicking the dice during the betting round or when it's the AI's turn"""
        for i in [0, 1]:
            for j in range(5):
                self.dice[i][j].unbind("<Button-1>")
        self.r.unbind("<Button-1>")
    
    def callback(self, event):
        for i in range(5):
            if self.dice[0][i] == event.widget:
                self.select_to_roll(0, i)
        for i in range(5):
            if self.dice[1][i] == event.widget:
                self.select_to_roll(1, i)
        if self.r == event.widget:
            isSure = askyesno("Confirm roll", "Are you sure?")
            if isSure: self.roll_selected()
            else: 
                self.p1selected = []
                self.p2selected = []
                self.refresh_dice()
                self.enableBoard()
            
    def newgame(self):
        self.p1.roll(range(5))
        self.p2.roll(range(5))        
        self.refresh_dice()      
        self.turn = 0
        #self.p1.bettor = True
        #self.p2.bettor = False
        self.betting_round()
        
    def betting_round(self):
        self.disableBoard()
        
        self.p1bets(0)
        self.refresh2()
        if self.turn < 1: 
            self.turn += 1
            self.diceround()
        else:
            p1score = score(self.p1.hand)
            p2score = score(self.p2.hand)
            if p1score > p2score:
                self.p1.funds += self.p1bet + self.p2bet
            elif p2score > p1score:
                self.p2.funds += self.p2bet + self.p1bet
            elif p1score == p2score:
                self.p1.funds += self.p1bet
                self.p2.funds += self.p2bet
            if self.p1.funds > 0 or self.p2.funds > 0:
                self.turn = 0
                self.p1.roll(range(5))
                self.p2.roll(range(5))
                self.refresh_dice()
                self.betting_round()
                s =self.check_win(p1score,p2score)
                print "AI: "+str(self.p2.AI)+ "\nIterations: " +str(self.p2.it)+ "\nFunds: "+ str(self.p2.funds)
                        
    
    def p1bets(self, callcount):
        call = self.p2bet - self.p1bet
        self.status.set("Player 1, place bet for round " + str(self.turn) + " p1bet: " + str(self.p1bet) + " p2bet: " + str(self.p2bet))
        if self.p1.AI == 0:
            bet = self.getHumanBet(call, self.p1.funds)
        else:
            bet = self.p1.choose_bet(self.p1.hand, call)
        if bet < call: 
            self.p2.funds += self.p1bet + self.p2bet
            self.p1bet = 0
            self.p2bet = 0
            turn = 2
            return
        
        if bet > self.p1.funds:
            bet = self.p1.funds            
        if bet == call:
            callcount += 1
        self.p1.funds -= bet        
        self.p1bet += bet
        print self.p1bet
        self.refresh2()
        if callcount < 2:
            self.p2bets(callcount)
        return
    
    def p2bets(self, callcount):
        call = self.p1bet - self.p2bet
        self.status.set("Player 2, place bet for round " + str(self.turn) + " p1bet: " + str(self.p1bet) + " p2bet: " + str(self.p2bet))
        if self.p2.AI == 0:
            bet = self.getHumanBet(call, self.p2.funds)
        else:
            bet = self.p2.bet(call)
        if bet < call:
            self.p1.funds += self.p1bet + self.p2bet
            self.p1bet = 0
            self.p2bet = 0
            turn = 2
            return
        
        if bet > self.p2.funds:
            bet = self.p2.funds
        if bet == call:
            callcount += 1        
        self.p2.funds -= bet
        self.p2bet += bet
        self.refresh2()
        if callcount < 2:
            self.p1bets(callcount)
        return
            
    def getHumanBet(self, call, maxval):
        if call > 0:
            isFolding = askyesno("Fold?", "Call = " + str(call) + ".\nDo you want to fold?")
        else: isFolding = False
        if isFolding: return -1
        else:
            return askinteger("Enter bet", "Call = " + str(call), minvalue=call, maxvalue=maxval)
        
    def diceround(self):
        self.p1selected = []
        self.p2selected = []
        self.refresh_dice()        
        self.status.set("Select dice to roll")
        
        if self.p1.AI != 0:
            self.p1selected = self.p1.search(self.p1.hand)
        if self.p2.AI != 0:
            self.p2selected = self.p2.search(self.p2.hand)
        if self.p1.AI != 0 and self.p2.AI != 0:
            self.roll_selected()
        else:
            self.enableBoard()

    def check_win(self,score_1,score_2):
        if score_1 > score_2:
            return self.p1
        elif score_2 > score_1:
            return self.p2
        else:
            if self.p1.bettor:
                return self.p1
            else:
                return self.p2
            
        
def startGame(p1, p2):
    
    root = Tk()
    app = PokerWindow(root, p1, p2)
    root.mainloop()

def test_AI():
    startGame(PokerPlayer (100, False, 1, 0), PokerPlayer (100, False, 2, 1))
