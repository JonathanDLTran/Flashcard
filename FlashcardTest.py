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
    assert d.cardList == []
    print("Pass deck")

initializeCard()
initializeDeck()