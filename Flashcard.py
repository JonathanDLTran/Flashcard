from RedBlackTree import *
from TextReader import *
from Parser import *


from Constants import *
import random


class Deck:
    
    def setAsRandom(self):
        self.randomCard = True
        
    def setAsNotRandom(self):
        self.randomCard = False
        
    def getIsRandom(self):
        return self.randomCard
    
    def getRandomCard(self):
        """
        current implementation just selects a randomly generated carf
        Next phase implementation will create some sort of clustering algorithm to
        suggest the next card for use
        """
        total = self.numCards
        randomIndex = random.randint(0, total - 1)
        return self.getCard(randomIndex)
        
    def getCard(self, index):
        if self.numCards == 0:
            return None
        return self.cardList[index]
        
    def removeCard(self, positionNum):
        # TODO need to fix the links
        num = self.numCards
        if num == 1:
            self.cardList.remove(self.cardList[positionNum])
        elif positionNum == 0:
            tail = self.getCard(num - 1)
            head = self.getCard(1)
            tail.setNext(head)
            head.setLast(tail)
            self.cardList.remove(self.cardList[positionNum])
        elif positionNum == num - 1:
            tail = self.getCard(num - 1)
            head = self.getCard(0)
            tail.setNext(head)
            head.setLast(tail)
            self.cardList.remove(self.cardList[positionNum])
        else:
            last = self.getCard(positionNum - 1)
            nextCard = self.getCard(positionNum + 1)
            last.setNext(nextCard)
            nextCard.setLast(last)
            self.cardList.remove(self.cardList[positionNum])
        self.numCards -= 1
    
    def addCard(self, card):
        assert type(card) == Card
        newCard = card
        numCards = len(self.cardList)
        self.cardList.append(newCard)
        self.numCards += 1
        if numCards > 0: #ALREADY MORE THAN ONE CARD IN DECK
            lastCard = self.cardList[numCards - 1 - 1] #subtract once more for the new card added
            firstCard = self.cardList[0]
            lastCard.setNext(newCard)
            newCard.setLast(lastCard)
            newCard.setNext(firstCard)
            firstCard.setLast(newCard)
        else:
            newCard.setLast(newCard)
            newCard.setNext(newCard)
        
    def editCard(self, positionNum):
        pass
    
    def __init__(self, name = None, isRandom = False):
        self.cardList = []
        self.numCards = 0
        self.deckName = name
        self.randomCard = isRandom
        
    def __str__(self):
        return self.deckName
    
    def __repr__(self):
        return self.deckName
    

class Card:
    
    def getName(self):
        return self.cardName
    
    def getFront(self):
        return self.frontText
    
    def getBack(self):
        return self.backText
    
    def getForward(self):
        return self.forwardChain

    def getRear(self):
        return self.rearChain
    
    def getNext(self):
        return self.nextCard
    
    def getLast(self):
        return self.lastCard
    
    def setName(self, name):
        assert type(name) == str
        self.cardName = name
        
    def setFront(self, text):
        assert type(text) == str
        self.frontText = text
        
    def setBack(self, text):
        assert type(text) == str
        self.backText = text
        
    def setForward(self, card):
        assert type(card) == Card
        self.forwardChain = card
        
    def setRear(self, card):
        assert type(card) == Card
        self.rearChain = card
        
    def setNext(self, card):
        assert type(card) == Card
        self.nextCard = card
    
    def setLast(self, card):
        assert type(card) == Card
        self.lastCard = card

    """
    Creates a new instance of a flash card 
    Attributes and Preconditions:
    front [str]/[None] is the forward side of card: the question
    back [str]/[None] is the back side of the card: the answer
    forward [Card]/[None] is the following card in this chain with the same or
        related answer (not every card with the same answer will be in the same chain)
    rear [Card]/[None] is the previous card in the chain
    following [Card]/[None] is the next card in the the pile of flashcards
    last [Card]/[None] is the previous card in the pile of flashcards
    
    statistics [List of [bool]] - list with each time card is answered correctly or not,
        where True is answered correctly, False is not
    
    Class invariants:
    After every single time the card is seen, the user must enter a statistic, or skip
    
    """
    def __init__(self, name = None, front = None, back = None, forward = None, rear = None, following = None, last = None):
        """
        Instantiates a new card with no connections
        """
        assert (name == None or type(name) == str)
        assert (front == None or type(front) == str)
        assert (back == None or type(back) == str)
        assert (forward == None or type(forward) == Card)
        assert (rear == None or type(rear) == Card)
        assert (following == None or type(following) == Card)
        assert (last == None or type(last) == Card)
        self.cardName = name
        self.frontText = front
        self.backText = back
        self.forwardChain = forward
        self.rearChain = rear
        self.nextCard = following
        self.lastCard = last
        
        self.statistics = []
        
    def addRear(self, backCard):
        assert type(backCard) == Card
        self.rearChain = backCard
        
    def addForward(self, forwardCard):
        assert type(forwardCard) == Card
        self.forwardChain = forwardCard
        
    def addFront(self, text):
        assert type(text) == str
        self.frontText = text
        
    def addBack(self, text):
        assert type(text) == str
        self.backText = text
    
    
    def addStatistic(self, boolean):
        assert (type(boolean) == bool or boolean == SKIP)
        self.statistics.append(boolean)
        
    def calculateStatistic(self):
        """
        calculate the percentage of times this card was answered correctly and incorrectly
        prints the percentage correct [float] and prints the percentage incorrect
        returns NONE
        """
        statistics = self.statistics
        total = len(statistics)
        if total == 0:
            print("No Statistics associated yet")
            return
        correct = 0
        incorrect = 0
        skip = 0
        for i in range(total):
            if statistics[i] == True:
                correct += 1
            elif statistics[i] == False:
                incorrect += 1
            else:
                skip += 1
        print("Number of times this card has been seen: " + str(total) + ".")
        print("The percentage correct is " + str(100 * correct/total) + "%.")
        print("The percentage incorrect is " + str(100 * incorrect/total) + "%.")
        print("The percentage skipped is " + str(100 * skip/total) + "%.")
        
                
    
    