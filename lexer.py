# We use Jay Conrod's IMP language

SPACE = " "

ASSIGN = ":="
EQ = "="
LT = "<"
GT = ">"
LTE = "<="
GTE = ">="
IF = "if"
ELSE = "else"
WHILE = "while"

keywords = [
    ASSIGN,
    EQ,
    LT,
    GT,
    LTE,
    GTE,
    IF,
    ELSE,
    WHILE,
]

add_space_in_parse = [
    IF,
    ELSE,
    WHILE,
]


def match_keywords(program_str, idx, keyword, add_space):
    if add_space:
        keyword += SPACE
    if len(keyword) > len(program_str[idx:]):
        return False
    for i in range(len(keyword)):
        actual_i = i + idx
        if program_str[actual_i] != keyword[i]:
            return False
    return True


def match_first_keyword(program_str, idx, keyword_list, add_space):
    for kw in keyword_list:
        if match_keywords(program_str, idx, kw, add_space):
            return kw
    return None


def match_char(char, keywords_list):
    kws = []
    for kw in keywords_list:
        if kw[0] == char:
            kws.append(kw)
    return kws


def lex(program_str):
    tokens = []
    is_var = False
    var_name = ""
    l = len(program_str)
    i = 0
    while (i != l):
        char = program_str[i]
        if not is_var:
            match_keywords_list = match_char(char, keywords)
            kw = match_first_keyword(
                program_str, i, match_keywords_list, False)
            # need to change true condition
            if kw != None:
                tokens.append(kw)
                l = len(kw)
                i += l

            else:
                is_var = True
                var_name += char
                i += 1
        else:
            if char == SPACE:
                is_var = False
                tokens.append(var_name)
                var_name = ""
                i += 1
            else:
                var_name += char
                i += 1
    return tokens


if __name__ == "__main__":
    program = "if else"
    print(lex(program))
