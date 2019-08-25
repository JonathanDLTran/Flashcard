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
    
initializeCard()