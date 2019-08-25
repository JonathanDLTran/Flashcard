
FRONT = 0
BACK = 1
FORWARD = 2
REAR = 3
FOLLOWING = 4
LAST = 5
SKIP = 'skip'

def readDocument():
        pass



class Pile:
    pass
    

class Card:
    
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
    def __init__(self, front = None, back = None, forward = None, rear = None, following = None, last = None):
        """
        Instantiates a new card with no connections
        """
        assert (front == None or type(front) == str)
        assert (back == None or type(back) == str)
        assert (forward == None or type(forward) == Card)
        assert (rear == None or type(rear) == Card)
        assert (following == None or type(following) == Card)
        assert (last == None or type(last) == Card)
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
        DESTRUCTIVE
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
        
                
    
    
class RedBlackTree:
    pass