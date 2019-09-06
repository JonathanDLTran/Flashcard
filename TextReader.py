#A CS 3110 Note to self
#WHY DO I PROGRAM? - I LOVE BUILDING PROJECTS, OBJECTS, THINGS I LOVE TO SEE WORK
#PROPERLY. I WANT TO CREATE THINGS THAT ARE COOL FOR MYSELF WHILE CHALLENGING MYSELF

from Constants import *

def textReaderDriver():
    try:
        filename = enterFileName()
        return textReaderController(filename, True)
    except IOError as e:
        print("IO ERROR - no such txt file in your current directory - quitting program")
        
    

def textReaderController(filename, convertToSentences ):
    """
    Header function, to be used with other modules
    """
    fileString = readDocument(filename)
    return format_text(fileString, convertToSentences)

def enterFileName(): # NOT TESTED YET
    print("Please navigate to the correct directory where you want to run this program. ")
    result = input("Please enter your file name with '.txt' at the end: ")
    if '.txt' not in result:
        print("No txt extension on file name. ")
    return result

def readDocument(filename):
    """
    Preconditions: the file must be a standard .txt file
        File must be in the following format: question \n ANSWER: answer \n \n next Question Answer cycle, etc END
    Reads the file, searching for "ANSWER"
    """
    f = open(filename, 'r')
    fileString = f.read()
    return fileString


def format_text(string_text, convert_to_sentences):
    """
    Formats text properly into dictionary
    Precondition:
    convert_to_sentences [bool] true if convert to sentences else don't
    string_text is a non_empty [str] such that
    it consists of blocks of questions with the block
    QUESTION: asas ANSWER: asda END || followed by possibly another question
    It must end in '||'
    Returns: list of tuples where the first element in the tuple are the list of
        question clues and the second is a string and is the answerline
    """
    listOfQuestionBlocks = convert_text_to_block(string_text)
    questionAnswerTuples = []
    for question in listOfQuestionBlocks:
        if not convert_to_sentences:
            pair = question_answer(question)
            questionAnswerTuples.append(([pair[0]], pair[1]))
        else:
            questionAnswerTuples.append(question_answer(question))
    if not convert_to_sentences:
        return questionAnswerTuples
    finalQuestionAnswerList = []
    for qaTuple in questionAnswerTuples:
        questionBlock = qaTuple[0]
        questionAnswer = qaTuple[1]
        questionList = convert_block_to_list(questionBlock)
        newTuple = (questionList, questionAnswer)
        finalQuestionAnswerList.append(newTuple)
    return finalQuestionAnswerList

        

def convert_text_to_block(string_text, list_of_blocks = []):
    """
    tail recursive
    every block of string must be ended by '||', and moreover, the string_text must end in '||' as well.
    """
    if string_text == '':
        return list_of_blocks
    newLinePos = string_text.index('||')
    beforeNewLines = string_text[:newLinePos]
    afterNewLines = string_text[newLinePos + 2:] # plus one plus two more for both new lines
    newListOfBlocks = list_of_blocks + [beforeNewLines]
    return convert_text_to_block(afterNewLines, newListOfBlocks)
    
    
def question_answer(single_block):
    """
    tail recursive
    single Block must have QUESTION, ANSWER, and END in it
    """
    single_block = single_block.strip()
    q = single_block.index(QUESTION) 
    a = single_block.index(ANSWER) 
    e = single_block.index(END)
    return (single_block[q + len(QUESTION): a].strip(), single_block[a + len(ANSWER): e].strip())

def convert_block_to_list(string_block):
    """
    Wrapper Function
    PostCondition: Returns a block of string into a list of strings
    PreCondition: The block of strings has at least one period, with a period ending the string block.
                String_block is not an empty string and is [str]
    """
    stringLen = len(string_block)
    if string_block[stringLen - 1] != '.':
        string_block = string_block + '.'
    newList = [element.strip() for element in block_to_sentence(string_block)]
    return [element for element in newList if element != '.']

def block_to_sentence(string_block, sentence_list = []):
    """
    Tail Recursive
    PostCondition: Converts a block of string into a list of strings, separated by the periods
    PreCondition: The block of strings has at least one period, with a period ending the string block.
                String_block is not an empty string and is [str]
    """
    if string_block == "": 
        return sentence_list
    p = string_block.index(".")
    beforePeriod = string_block[:p + 1]
    afterPeriod = string_block[p + 1:]
    newSentenceList = sentence_list + [beforePeriod]
    return block_to_sentence(afterPeriod, newSentenceList)
    


##########DEAD OR DEPRECATED CODE. ONLY FIND PERIODS WAS TESTED#########

def find_periods(string_block, period_list = []):
    """
    Tail Recursive
    PostCondition: Returns a list of positions where periods are located in string_block
    PreCondition: String_block is a [str] not empty, with at least one period, ending in a period
    """
    if (string_block == "") or ('.' not in string_block):
        return period_list
    periodPos = string_block.rindex(".")
    newPeriodList = [periodPos] + period_list 
    after_period_string = string_block[:periodPos]
    return find_periods(after_period_string, newPeriodList)
    
def searchForAnswer(fileString):
    """
    Recursively searches fileString for ANSWER, and will return a list of positions where ANSWER will be 
    """
    if fileString == []:
        return []
    answerList = []
    answerPos = fileString.index(ANSWER)
    answerList.append(answerPos)
    return answerPos + searchForAnswer(fileString[answerPos + 1: ])

def searchForEnd(fileString):
    return fileString.index(END)