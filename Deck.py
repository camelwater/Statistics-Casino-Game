import random as rand
from Card import Card, Color

class Deck:
    def __init__(self, deck = None, extra=False):
        if deck:
            self.deck = list(deck)
        else:
            self.deck = list()
            if extra:
                self.init_red_deck()

    
    def shuffle(self):
        rand.shuffle(self.deck)
    
    def init_red_deck(self):
        for i in range(6):
            if i == 0:
                self.deck.append(Card(Color.RED, i))
            elif i == 1:
                for n in range(3):
                    self.deck.append(Card(Color.RED, i))
            elif i == 2:
                for n in range(2):
                    self.deck.append(Card(Color.RED, i))
            elif i == 3:
                for n in range(1):
                    self.deck.append(Card(Color.RED, i))
            elif i==4:
                for n in range(6):
                    self.deck.append(Card(Color.RED, i))
            elif i ==5 :
                for n in range(2):
                    self.deck.append(Card(Color.RED, i))
    
    def pop(self):
        return self.deck.pop()

    def push(self, card):
        self.deck.append(card)
    
    def getDeck(self):
        return self.deck
    
