from lib.sql_lexer.lexer import parse
from lib.html_generator.color_schemes import *


def highlight(query):
    html = ""
    parsed = parse(query)
    for lexeme in parsed:
        lex = lexeme[0]
        token_type = lexeme[1]
        if token_type == "newline":
            html += "<br>"
        elif token_type == "whitespace":
            html += " "
        else:
            html += f"<span class='{token_type}'>{lex}</span>"
    return html


def apply_colors(template, theme=default_colors):
    for color_name, color in theme.items():
        template = template.replace(f"%{color_name}%", color)
    return template
