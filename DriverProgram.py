from RedBlackTree import *
from TextReader import *
from Parser import *
from Flashcard import *
from Constants import *
import pickle

def parser_driver(deck):
    while(True):
        command = input("Please enter your command: \n")
        if command == "next":
            deck.nextCard()
        elif command == "last":
            deck.lastCard()
        elif command == "forward":
            deck.forwardCard()
        elif command == "rear":
            deck.rear()
        elif command == "front":
            deck.frontCard()
        elif command == "back":
            deck.backCard()
        elif command == "quit":
            return
        
    

if __name__ == '__main__':
    processedText = textReaderDriver()
    d = Deck()
    d.text_to_cards(processedText)
    
    
    file_Name = "CurrentDeck.txt"
    fileObject = open(file_Name,'wb') 
    pickle.dump(d, fileObject)
    fileObject.close()
    
    parser_driver(d)
    
    # TODO: add parser for user experience
    