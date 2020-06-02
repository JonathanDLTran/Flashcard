from RedBlackTree import *
from TextReader import *
from Parser import *
from Flashcard import *
from Constants import *
import pickle
import json


def run():
    processedText = textReaderDriver()
    d = Deck()
    d.text_to_cards(processedText)

    file_Name = "CurrentDeck.txt"
    fileObject = open(file_Name, 'wb')
    pickle.dump(d, fileObject)
    fileObject.close()

    parser_driver(d)


if __name__ == '__main__':
    processedText = textReaderDriver()
    d = Deck()
    d.text_to_cards(processedText)

    file_Name = "CurrentDeck.txt"
    fileObject = open(file_Name, 'wb')
    pickle.dump(d, fileObject)
    fileObject.close()

    parser_driver(d)

    # TODO: add parser for user experience
