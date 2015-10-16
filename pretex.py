#!/usr/bin/env python

import sys

keywords = ['theme', 'title', 'author', 'date', 'sec', 'subsec', 'slide', 'txt', 'box', 'img']

def clean_input(expr):
    newexpr = []
    for elm in expr:
        newexpr = newexpr + elm.split();
    return newexpr

def parse(src):
    expr = []
    while src:
        elm = src.pop(0)
        if elm[-2:] == "::" and elm[:-2] in keywords:
            expr.append([elm[:-2]]);
        else:
            expr[-1].append(elm);
    return expr

def pretex(expr):
    theme = 'default'; title = ''; author = ''; date = '';
    for val in expr:
        if val[0] == 'theme':
            theme = val[1]          
        elif val[0] == 'title':
            title = '\\title{{{}}}\n'.format(' '.join(val[1:]))
        elif val[0] == 'author':
            author = '\\author{{{}}}\n'.format(' '.join(val[1:]))
        elif val[0] == 'date':
            date = '\\date{{{}}}\n'.format(' '.join(val[1:]))

    code = "\\documentclass{{beamer}}\n\usetheme{{{}}}\n".format(theme) + title + author + date
    code = code + "\\usepackage{graphicx}\\begin{document}\n\\maketitle\n"

    slide_begin = False; item_begin = False; 

    for val in expr:

        elm = val.pop(0);

        if elm == 'sec':
            if item_begin:
                code = code + '\\end{itemize}\n'
            if slide_begin:
                code = code + '\\end{frame}\n'
            slide_begin = False;
            item_begin = False;
            code = code + '\\section{{{}}}\n'.format(' '.join(val))

        elif elm == 'subsec':
            if item_begin:
                code = code + '\\end{itemize}\n'
            if slide_begin:
                code = code + '\\end{frame}\n'
            slide_begin = False;
            item_begin = False;
            code = code + '\\subsection{{{}}}\n'.format(' '.join(val))

        elif elm == 'slide':
            if item_begin:
                code = code + '\\end{itemize}\n'
            if slide_begin:
                code = code + '\\end{frame}\n'
            slide_begin = True;
            item_begin = False;
            code = code + '\\begin{{frame}}{{{}}}\n'.format(' '.join(val))

        elif elm == 'txt':
            if not item_begin:
                code = code + '\\begin{itemize}\n'
            item_begin = True; 
            code = code + '\\item {}\n'.format(' '.join(val))

        elif elm == 'box':
            if item_begin:
                code = code + '\\end{itemize}\n'
            item_begin = False;
            box_title = val.pop(0);
            code = code + '\\begin{{block}}{{{}}}\n {}\n\\end{{block}}\n'.format(box_title, ' '.join(val))

        elif elm == 'img':
            if item_begin:
                code = code + '\\end{itemize}\n'
            item_begin = False;
            code = code + '\\begin{{center}}\\includegraphics{{{}}}\\end{{center}}\n'.format(' '.join(val))

    if item_begin:
        code = code + '\\end{itemize}\n'

    if slide_begin:
        code = code + '\\end{frame}\n'

    code = code + '\\end{document}'

    return code

if __name__ == '__main__':
    src = clean_input(sys.stdin.readlines())
    print pretex(parse(src))
