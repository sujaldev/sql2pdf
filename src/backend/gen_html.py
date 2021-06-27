from lib.html_generator.highlight import *
from src.backend.run_sql import *


base_code = """<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
:root {
    /* WINDOW THEME */
    --window-color: rgb(40, 44, 52);
    --window-default-text-color: white;
    --window-border-radius: 10px;
    --window-min-width: 400px;
    --window-min-height: 100px;
    --title-bar-height: 50px;
    --title-bar-color: rgb(30, 34, 42);
    --btn-size: 15px;
    --btn-default-color: white;
    --btn-spacing: 10px;
    --btn-min-color: #27C93F;
    --btn-max-color: #FFBD2E;
    --btn-close-color: #FF5F56;
    --keyword-color: %keyword-color%;
    --identifier-color: %identifier-color%;
    --symbol-color: %symbol-color%;
    --numeric-literal-color: %numeric-literal-color%;
    --string-literal-color: %string-literal-color%;

    /* SYNTAX THEME */
}

.keyword{
    color: var(--keyword-color)
}

.identifier{
    color: var(--identifier-color)
}

.symbol{
    color: var(--symbol-color)
}

.numeric-literal{
    color: var(--numeric-literal-color)
}

.string-literal{
    color: var(--string-literal-color)
}

/* * {
    padding: 0;
    margin: 0;
} */

.text{
    font-family: Consolas, Menlo, Monaco, Lucida Console, Liberation Mono, DejaVu Sans Mono, Bitstream Vera Sans Mono, Courier New, monospace, serif;
}

.regular{
    font-weight: 500;
}

.bold{
    font-weight: 900;
}

.code-window{
    display: inline-block;
    position: relative;
    left: 50%;
    transform: translateX(-50%);
    min-width: var(--window-min-width);
    min-height: var(--window-min-height);
    background: var(--window-color);
    color: var(--window-default-text-color);
    border-radius: var(--window-border-radius);
}

.header {
    display: flex;
    align-items: center;
    width: 100%;
    height: var(--title-bar-height);
    background: var(--title-bar-color);
    border-radius: var(--window-border-radius) var(--window-border-radius) 0 0;
}

.btn {
    width: var(--btn-size);
    height: var(--btn-size);
    background: var(--btn-default-color);
    border-radius: 50%;
    margin-right: var(--btn-spacing);
}

.btn:nth-child(1){
    margin-left: 20px;
    background: var(--btn-min-color);
}

.btn:nth-child(2){
    background: var(--btn-max-color);
}

.btn:nth-child(3){
    background: var(--btn-close-color);
    margin-right: 40px;
}

.code{
    padding: 30px;
}

.sub-heading {
    text-align: center;
    text-transform: uppercase;
    font-size: 24px;
}

.section-division-line {
    position: relative;
    left: 50%;
    transform: translateX(-50%);
    margin: 30px;
    width: 80%;
    height: 2px;
    background: rgba(0,0,0,0.1);
}
    </style>
    <title>SQL TO PDF</title>
</head>
<body>
    %code%
</body>
</html>
"""

query_window = """
    <div class="code-window">
        <div class="header">
            <div class="btn"></div>
            <div class="btn"></div>
            <div class="btn"></div>
            <div class="text regular">%window_title%</div>
        </div>
        <div class="code text bold">%code%</div>
    </div><br>
"""

query_output = """
    <br>
    <div class="code-window">
        <div class="header">
            <div class="btn"></div>
            <div class="btn"></div>
            <div class="btn"></div>
            <div class="text regular">%window_title%</div>
        </div>
        <div class="code text bold"><p class="output-text">%output%</p></div>
    </div>
"""

sub_headings = """
    <h1 class="sub-heading">%heading%</h1>
"""


# def gen_html(query, window_title="MySQL Code", template=base_code, color=default_colors):
#     template = apply_colors(template, color)
#     template = template.replace("%code%", highlight(query)).replace("%window_title%", window_title)
#     return template


def gen_query_window(query, window_title="MySQL Code", template=query_window):
    template = template.replace("%window_title%", window_title)
    template = template.replace("%code%", highlight(query))
    return template


def gen_query_output(output, template=query_output):
    output = output.replace("\n", "<br>")
    output = output.replace(" ", "&nbsp;")
    template = template.replace("%window_title%", "OUTPUT WINDOW")
    template = template.replace("%output%", output)
    return template


def gen_sub_heading(comment, template=sub_headings):
    comment = comment.replace("--", "")
    comment = comment.replace(" ", "&nbsp;")
    template = template.replace("%heading%", comment)
    return template


def gen_html(query, template=base_code, user="root", password="admin"):
    output_map = group_sql_output(query, user, password)
    html = ""
    for entry in output_map:
        q, o = entry[0], entry[1]
        if "--" in q:
            # print(q)
            cursor = q.find("--")
            query_part, sub_heading = q[:cursor], q[cursor:]
            html += "<div class='section-division-line'></div>"
            html += gen_sub_heading(sub_heading.split("\n")[0])
            html += gen_query_window(q)
            html += gen_query_output(o)
        else:
            html += "<div class='section-division-line'></div>"
            html += gen_query_window(q)
            html += gen_query_output(o)
            html += "<br><br>"
    return apply_colors(template.replace("%code%", html))
