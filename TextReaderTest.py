from TextReader import *

def test_find_period():
    print("test period")
    string1 = "hi. My name is Jonathan. Lol."
    assert find_periods(string1) == [2, 23, 28]

    string2 = "."
    assert find_periods(string2) == [0]
    print("Pass period")
    
def test_block_sentence():
    print("Test block")
    string1 = "hi. My name is Jonathan. Lol."
    assert convert_block_to_list(string1) == ['hi.', 'My name is Jonathan.', 'Lol.']
    
    string2 = "."
    assert convert_block_to_list(string2) == []
    
    string3 = "llama ate cake. haha. "
    assert convert_block_to_list(string3) == ["llama ate cake.", 'haha.']
    print("Pass block")
    
def test_blocks():
    print("Testing many blocks")
    string = ("Hi my name is Jonathan.How are you. || Are you happy.||")
    assert convert_text_to_block(string) == ["Hi my name is Jonathan.How are you. ", " Are you happy." ]
    
    string = ("Hi my name is Jonathan.How are you. || Are you happy.|| Lolz this is a question hahahha. ||")
    assert convert_text_to_block(string) == ["Hi my name is Jonathan.How are you. ", " Are you happy.", " Lolz this is a question hahahha. " ]
    print("passing many blocks")
    
def test_q_a():
    print("Test question answer")
    qa = "QUESTION: This man was the liberator of Venezuela. ANSWER: Bolivar END"
    assert question_answer(qa) == ("This man was the liberator of Venezuela.", "Bolivar")
    
    qa2 = "QUESTION: This man was the liberator of Venezuela. He was led the Admirable Campaign. He lost to Jose Boves. ANSWER: Bolivar END"
    assert question_answer(qa2) == ("This man was the liberator of Venezuela. He was led the Admirable Campaign. He lost to Jose Boves.", "Bolivar")
    print("Pass question answer")
    
def test_format():
    print("Test format")
    text = "QUESTION: this man was imre thokoly. ANSWER: IMRE THOKOLY END || QUESTION: This hungarian rebel. ANSWER: Ferenc Rakoszi END ||"
    sentences = True
    assert format_text(text, sentences) == [(["this man was imre thokoly."], "IMRE THOKOLY"), (["This hungarian rebel."], "Ferenc Rakoszi")]
    text2 = "QUESTION: this man was imre thokoly. this man was imre thokoly. ANSWER: IMRE THOKOLY END || QUESTION: This hungarian rebel. ANSWER: Ferenc Rakoszi END ||"
    assert format_text(text2, sentences) == [(["this man was imre thokoly.", "this man was imre thokoly."], "IMRE THOKOLY"), (["This hungarian rebel."], "Ferenc Rakoszi")]
    sentences = False
    assert format_text(text2, sentences) == [(["this man was imre thokoly. this man was imre thokoly."], "IMRE THOKOLY"), (["This hungarian rebel."], "Ferenc Rakoszi")]
    print("Pass format")
def test_controller():
    print("Test controller")
    filename = "Test.txt"
    assert textReaderController(filename, True) == [(["this man was imre thokoly.", "this man was imre thokoly."], "IMRE THOKOLY"), (["This hungarian rebel."], "Ferenc Rakoszi")]
    assert textReaderController(filename, False) == [(["this man was imre thokoly. this man was imre thokoly."], "IMRE THOKOLY"), (["This hungarian rebel."], "Ferenc Rakoszi")]
    print("Pass controller")

test_find_period()
test_block_sentence()
test_blocks()
test_q_a()
test_format()
test_controller()