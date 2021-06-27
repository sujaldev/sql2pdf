from lib.sql_lexer.tokens import *
from lib.sql_lexer.helper_funcs import *


def parse(query):
    """
    TAKE A SQL QUERY (WITHOUT COMMENTS) AND GENERATE LIST OF LEXEMES AND IT'S TYPE
    :param query:
    :return:
    """
    i = 0  # INDEX WHILE TRAVERSING QUERY
    buffer = ""  # STORES CHARS IN ORDER UNTIL A LEXEME IS IDENTIFIED
    parsed_list = []  # PARSED OUTPUT IS STORED HERE IN FORM OF [(LEXEME, TOKEN-TYPE)]
    expected_end = False

    # TRAVERSE THROUGH QUERY CHARACTER BY CHARACTER
    while i < len(query):
        char = query[i]  # CURRENT CHAR
        # GET NEXT CHAR AND SET NONE IF AT END OF QUERY
        try:
            next_char = query[i + 1]
        except IndexError:
            next_char = None
        # ADD CHAR TO BUFFER
        buffer += char

        # TRY TO DETECT LEXEME
        # IGNORED CHARACTERS
        if buffer in ignored_chars:
            parsed_list.append((buffer, ignored_chars[buffer]))
            buffer = ""
        # COMMENTS
        elif "-" in buffer and next_char == "-":
            i = i + query[i:].find("\n")
            buffer = ""
            continue
        # LITERALS
        # STRING
        elif buffer in ("'", '"'):
            expected_end = True
        elif (buffer[-1] in ("'", '"')) and (buffer[0] == buffer[-1]) and expected_end:
            parsed_list.append((buffer, "string-literal"))
            expected_end = False
            buffer = ""
        # NUMBERS
        elif is_int_or_float(buffer) and next_char in tuple_remove(symbols, "."):
            parsed_list.append((buffer, "numeric-literal"))
            buffer = ""
        elif is_int_or_float(buffer) and next_char == ".":
            pass
        elif is_int_or_float(buffer) and next_char == " ":
            parsed_list.append((buffer, "numeric-literal"))
            parsed_list.append((" ", "whitespace"))
            i += 1
            buffer = ""
        # KEYWORD
        elif (buffer.upper() in keywords) and not expected_end:
            # IF NEXT CHAR IS A SYMBOL APPEND BUFFER TO PARSED LIST AND CLEAR BUFFER
            if next_char in symbols:
                parsed_list.append((buffer.upper(), "keyword"))
                buffer = ""
            # IF NEXT CHAR IS WHITESPACE ADD BUFFER TO PARSED LIST, EMPTY BUFFER AND SKIP NEXT CHARACTER
            elif next_char in ignored_chars:
                parsed_list.append((buffer.upper(), "keyword"))
                parsed_list.append((next_char, ignored_chars[next_char]))
                buffer = ""
                i += 1
        # SYMBOLS
        elif (buffer in symbols) and not expected_end:
            # APPEND SYMBOL TO PARSED LIST AND EMPTY BUFFER
            parsed_list.append((buffer, "symbol"))
            buffer = ""
            # SKIP NEXT CHAR IF NEXT CHAR IS WHITESPACE
            if next_char == " ":
                parsed_list.append((" ", "whitespace"))
                i += 1
        # IDENTIFIERS
        elif (next_char in symbols) and not expected_end:
            # IF NEXT CHAR IS SYMBOL APPEND THEN CLEAN BUFFER
            parsed_list.append((buffer.lower(), "identifier"))
            buffer = ""
        elif (next_char == " ") and not expected_end:
            # IF NEXT CHAR IS WHITESPACE APPEND THEN CLEAN BUFFER AND SKIP NEXT CHAR
            parsed_list.append((buffer.lower(), "identifier"))
            parsed_list.append((" ", "whitespace"))
            buffer = ""
            i += 1
        # UPDATE INDEX
        i += 1

    # RETURN PARSED OUTPUT
    return parsed_list
