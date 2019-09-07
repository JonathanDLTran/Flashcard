from Constants import *
import random


class Deck:
    
    ##########MOVING CARDS##############
    def nextCard(self):
        """
        there must be a card in the deck
        sets the next card in the main chain as current as called
        returns true if done, false otherwise
        """
        if self.numCards == 0:
            print("The deck is currently empty.")
            return False
        currentCard = self.getCurrentCard()
        nextCard = currentCard.getNext()
        if nextCard == None:
            print("There is no next card in the main chain.")
            return False
        self.setCurrentCard(nextCard)
        return True
    
    def lastCard(self):
        """
        there must be a card in the deck
        sets the last card in the main chain as current as called
        returns true if done, false otherwise
        """
        if self.numCards == 0:
            print("The deck is currently empty.")
            return False
        currentCard = self.getCurrentCard()
        lastCard = currentCard.getLast()
        if lastCard == None:
            print("There is no last card in the main chain.")
            return False
        self.setCurrentCard(lastCard)
        return True
    
    def forwardCard(self):
        if self.numCards == 0:
            print("The deck is currently empty.")
            return False
        currentCard = self.getCurrentCard()
        forwardCard = currentCard.getForward()
        if forwardCard == None:
            print("There is no forward card in the side chain.")
            return False
        self.setCurrentCard(forwardCard)
        return True
    
    def rearCard(self):
        if self.numCards == 0:
            print("The deck is currently empty.")
            return False
        currentCard = self.getCurrentCard()
        rearCard = currentCard.getRear()
        if rearCard == None:
            print("There is no rear card in the side chain.")
            return False
        self.setCurrentCard(rearCard)
        return True
    
    def frontCard(self):
        if self.numCards == 0:
            print("The deck is currently empty.")
            return False
        currentCard = self.getCurrentCard()
        text = currentCard.getFront()
        print(SEPARATOR)
        print("This is the front of the card: \n")
        print(text)
        print(SEPARATOR)
        return True
    
    def backCard(self):
        if self.numCards == 0:
            print("The deck is currently empty.")
            return False
        currentCard = self.getCurrentCard()
        text = currentCard.getBack()
        print(SEPARATOR)
        print("This is the back of the card: \n")
        print(text)
        print(SEPARATOR)
        return True
    ####################
    
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
        the random card will always be on the main chain
        """
        total = len(self.cardList)
        randomIndex = random.randint(0, total - 1)
        randomCard = self.getCard(randomIndex)
        assert randomCard.getMain()
        self.setCurrentCard(randomCard)
        return randomCard
        
    def getCard(self, index):
        """
        index must be in the main chain
        """
        assert type(index) == int and (index < len(self.cardList) or len(self.cardList) == 0)
        if self.numCards == 0:
            return None
        return self.cardList[index]
        
    def removeCard(self, positionNum):
        """
        only removes cards form the main line
        """
        # TODO need to deal with Main cards removal and chain cards removal
        
        num = len(self.cardList)
        if num == 0:
            print("No cards to remove")
            return
        if num == 1:
            self.cardList.remove(self.cardList[positionNum])
            self.setCurrentCard(None)
        elif positionNum == 0:
            tail = self.getCard(num - 1)
            head = self.getCard(1)
            tail.setNext(head)
            head.setLast(tail)
            self.cardList.remove(self.cardList[positionNum])
            self.setCurrentCard(head)
        elif positionNum == num - 1:
            tail = self.getCard(num - 2)
            head = self.getCard(0)
            tail.setNext(head)
            head.setLast(tail)
            self.cardList.remove(self.cardList[positionNum])
            self.setCurrentCard(tail)
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
        numCards1 = len(self.cardList)
        self.cardList.append(newCard)
        self.numCards += 1
        if numCards1 == 1:
            firstCard = self.cardList[0]
            newCard.setLast(firstCard)
            newCard.setNext(firstCard)
            firstCard.setNext(newCard)
            firstCard.setLast(newCard)
        elif numCards1 > 1: #ALREADY MORE THAN ONE CARD IN DECK
            lastCard = self.cardList[numCards1- 1 - 1] #subtract once more for the new card added
            firstCard = self.cardList[0]
            lastCard.setNext(newCard)
            newCard.setLast(lastCard)
            newCard.setNext(firstCard)
            firstCard.setLast(newCard)
        else:
            newCard.setLast(newCard)
            newCard.setNext(newCard)
            
            
    def create_card_chain(self, questionsList, answer):
        firstQuestion = questionsList[0]
        firstCard = self.createCardHelper(firstQuestion, answer)
        firstCard.setMain(True) # part of main chain of cards
        self.setCurrentCard(firstCard)
        
        remainingQuestions = questionsList[1:]
        previousCard = firstCard
        for question in remainingQuestions:
            #newCard = self.createCardHelper(question, answer)
            newCard = Card()
            newCard.addFront(question)
            newCard.addBack(answer)
            newCard.setMain(False)
            self.numCards += 1
            previousCard.addForward(newCard)
            newCard.addRear(previousCard)
            previousCard = newCard
        
            
    def text_to_cards(self, processed_text_list):
        assert type(processed_text_list) == list
        for qaTuple in processed_text_list:
            questionsList = qaTuple[0]
            answer = qaTuple[1]
            if len(questionsList) == 1:
                question = questionsList[0]
                newCard = self.createCardHelper(question, answer)
                newCard.setMain(True) # main chain card
                self.setCurrentCard(newCard)
            else: 
                self.create_card_chain(questionsList, answer)
                
        
            
    def createCardHelper(self, question, answer):
        newCard = Card()
        newCard.addFront(question)
        newCard.addBack(answer)
        self.addCard(newCard)
        return newCard
    
    def custom_chain_card_creation(self, main_index, question, answer):
        """
        main index is int position of the card of which you want to add a side chain to
        """
        mainCard = self.cardList[main_index]
        newCard = Card()
        newCard.addFront(question)
        newCard.addBack(answer)
        self.numCards += 1
        self.setMain(False)
        self.setCurrentCard(newCard)
        # TODO
        
    def find_main_card(self, card):
        assert type(card) == Card or type(card) == None
        if card.getMain():
            return card
        forward = self.search_forward_chain(card)
        backward = self.search_rear_chain(card)
        return forward if forward != None else backward #one forward or backward must be on the main chain
        
    def search_forward_chain(self, card):
        assert type(card) == Card or card == None
        if card == None:
            return None
        if card.getMain():
            return card
        newCard = card.getForward()
        return self.search_forward_chain(newCard)

    def search_rear_chain(self, card):
        assert type(card) == Card or card == None
        if card == None:
            return None
        if card.getMain():
            return card
        newCard = card.getRear()
        return self.search_rear_chain(newCard)
    
    def custom_main_card_creation(self, question, answer):
        newCard = self.createCardHelper(question, answer)
        newCard.setMain(True)
        self.numCards += 1
        self.setCurrentCard(newCard)
        
    def setCurrentCard(self, card):
        assert (type(card) == Card) or (card == None)
        self.currentCard = card
        
    def getCurrentCard(self):
        return self.currentCard
    
    def __init__(self, name = None, isRandom = False):
        self.currentCard = None
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
    
    def getMain(self):
        return self.mainChain
    
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
        
    def setMain(self, main):
        assert type(main) == bool
        self.mainChain = main

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
    main [bool] is whether the card is the main chain - the command main will take you from any card in the chain to the main card in the chain
    
    statistics [List of [bool]] - list with each time card is answered correctly or not,
        where True is answered correctly, False is not
    
    Class invariants:
    After every single time the card is seen, the user must enter a statistic, or skip
    
    """
    def __init__(self, name = None, front = None, back = None, forward = None, rear = None, following = None, last = None, main = True):
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
        
        self.mainChain = main
        
        self.statistics = []
        
    def editCard(self, card_face, edits):
        """
        self card is a valid [Card] object
        card_face is a [bool], true for front, false for back,
        edits is a [string]
        changes the text on the card at the given positionNum, and on the card face
        specified with the requested edits
        """
        if card_face:
            self.setFront(edits)
        else:
            self.setBack(edits)
        
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
        
    def resetStatistic(self):
        print("All Statistics for this current card are about to be cleared. ")
        self.statistics = []
    
    
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
        
    def __str__(self):
        return "Card ID: \n" + str(id(self)) + "\nThis is the front: \n " + self.getFront() + "\nThis is the back: \n" + self.getBack() + "\n" + "Main Card " if self.mainChain else "Card ID: \n" + str(id(self)) + "\nThis is the front: \n " + self.getFront() + "\nThis is the back: \n" + self.getBack() + "\n" +" Not Main Card"
        
    def __repr(self):
        return "Card ID: \n" + str(id(self)) + "\nThis is the front: \n " + self.getFront() + "\nThis is the back: \n" + self.getBack() + "\n" + "Main Card " if self.mainChain else "Card ID: \n" + str(id(self)) + "\nThis is the front: \n " + self.getFront() + "\nThis is the back: \n" + self.getBack() + "\n" +" Not Main Card"

                
    
    