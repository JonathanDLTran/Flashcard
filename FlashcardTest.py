from Flashcard import *

def initializeCard():
    print("testing card initializatiion")
    c = Card()
    assert c.getFront() == None
    assert c.getBack() == None
    assert c.getForward() == None
    assert c.getRear() == None
    assert c.getNext() == None
    assert c.getLast() == None
    
    c.addFront("This city is the capital of Maine.")
    c.addBack("Augusta")
    assert c.getFront() == "This city is the capital of Maine."
    assert c.getBack() == "Augusta"
    
    c.calculateStatistic()
    c.addStatistic(True)
    c.calculateStatistic()
    c.addStatistic(False)
    c.calculateStatistic()
    c.addStatistic(True)
    c.calculateStatistic()
    c.addStatistic(SKIP)
    c.calculateStatistic()
    c.addStatistic(SKIP)
    c.calculateStatistic()
    
    cF = Card()
    cF.addRear(c)
    c.addForward(cF)
    assert cF.getRear() == c
    assert c.getForward() == cF
    
    cB = Card()
    cB.addForward(c)
    c.addRear(cB)
    assert c.getRear() == cB
    assert cB.getForward() == c
    assert cF.getRear().getRear() == cB
    assert cB.getForward().getForward() == cF
    
    print("Pass card initialization")
    
def initializeDeck():
    print("testing Deck")
    d = Deck()
    c1 = Card()
    d.addCard(c1)
    assert d.cardList[0] == c1
    assert len(d.cardList) == 1
    assert d.numCards == 1
    c2 = Card()
    d.addCard(c2)
    assert d.cardList[0] == c1
    assert d.cardList[1] == c2
    assert len(d.cardList) == 2
    assert d.numCards == 2
    c3 = Card()
    d.addCard(c3)
    c4 = Card()
    d.addCard(c4)
    c5 = Card()
    d.addCard(c5)
    assert d.cardList[0] == c1
    assert d.cardList[1] == c2
    assert d.cardList[2] == c3
    assert d.cardList[3] == c4
    assert d.cardList[4] == c5
    assert len(d.cardList) == 5
    assert d.numCards == 5
    
    assert d.getIsRandom() == False
    print(d.getRandomCard())
    print(d.getRandomCard())
    print(d.getRandomCard())
    print(d.getRandomCard())
    print(d.getRandomCard())
    
    d.removeCard(4)
    assert d.cardList[0] == c1
    assert d.cardList[1] == c2
    assert d.cardList[2] == c3
    assert d.cardList[3] == c4
    d.removeCard(2)
    assert d.cardList[0] == c1
    assert d.cardList[1] == c2
    assert d.cardList[2] == c4
    print("Pass deck")
    d.removeCard(0)
    assert d.cardList[0] == c2
    assert d.cardList[1] == c4
    d.removeCard(0)
    assert d.cardList[0] == c4
    d.removeCard(0)
    assert d.numCards == 0
    assert d.cardList == []
    print("Pass deck")
    
def initializeQuestions():
    print("Initialize questions")
    d = Deck()
    assert d.numCards == 0
    assert d.getCurrentCard() == None
    assert d.cardList == []
    qList = [(["this man was imre thokoly.", "Hello this man was imre thokoly."], "IMRE THOKOLY"), (["This hungarian rebel."], "Ferenc Rakoszi")]
    d.text_to_cards(qList)
    assert d.numCards == 3
    c1 = d.getCurrentCard()
    print(c1)
    assert c1.getMain() == True
    c2 = c1.getLast()
    print(c2)
    assert c2 is not c1
    assert c2.getNext() == c1
    assert c2.getMain() == True
    c3 = c2.getForward()
    print(c3)
    assert c3 is not c2
    assert c3.getMain() == False
    assert c3.getRear() == c2
    
    assert c3.getFront() == "Hello this man was imre thokoly."
    assert c3.getBack() == "IMRE THOKOLY"
    assert c2.getFront() == "this man was imre thokoly."
    assert c2.getBack() == "IMRE THOKOLY"
    assert c1.getFront() == "This hungarian rebel."
    assert c1.getBack() == "Ferenc Rakoszi"
    
    assert d.find_main_card(c2) == c2
    assert d.find_main_card(c1) == c1
    assert d.find_main_card(c3) == c2
    
    d.setCurrentCard(c2)
    assert d.getCurrentCard() == c2
    assert d.nextCard() == True
    assert d.getCurrentCard() == c1
    
    d.setCurrentCard(c1)
    assert d.getCurrentCard() == c1
    assert d.lastCard() == True
    assert d.getCurrentCard() == c2
    
    # implemented circular linked list
    
    d.setCurrentCard(c2)
    assert d.lastCard() == True
    assert d.getCurrentCard() == c1
    assert d.lastCard() == True
    assert d.getCurrentCard() == c2
    
    d.setCurrentCard(c2)
    assert d.nextCard() == True
    assert d.getCurrentCard() == c1
    assert d.nextCard() == True
    assert d.getCurrentCard() == c2
    
    d.setCurrentCard(c2)
    assert d.forwardCard() == True
    assert d.getCurrentCard() == c3
    assert d.forwardCard() == False
    
    assert d.rearCard() == True
    assert d.getCurrentCard() == c2
    assert d.rearCard() == False
    
    d.removeCard(1) # remove c1
    assert d.numCards == 2
    assert d.nextCard() == True
    assert d.getCurrentCard() == c2
    assert d.lastCard() == True
    assert d.getCurrentCard() == c2
    
    
    print("Pass questions")

initializeCard()
initializeDeck
initializeQuestions()