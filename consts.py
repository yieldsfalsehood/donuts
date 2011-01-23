#!/usr/bin/env python

THEMES_DIR = './themes'

common_style = r"""
\lstdefinestyle{common}{
  aboveskip={1.5\baselineskip},
  showtabs=false,
  showspaces=false,
  showstringspaces=false,
  prebreak = \raisebox{0ex}[0ex][0ex]{\ensuremath{\hookleftarrow}},
  columns=fixed,
  frame=single,
  framerule=0pt,
  upquote
}
""".lstrip()

listings_style = r"""
\lstdefinestyle{%(name)s}{
  backgroundcolor=%(backgroundcolor)s,
  style=common,
  basicstyle=%(basicstyle)s,
  identifierstyle=%(identifierstyle)s,
  commentstyle=%(commentstyle)s,
  stringstyle=%(stringstyle)s,
  keywordstyle=%(keywordstyle)s,
  procnamestyle=%(procnamestyle)s
}
""".lstrip()

preamble = r"""
\documentclass{article}

\usepackage[procnames]{listings}
\usepackage{color}
\usepackage{fullpage}
\usepackage{upquote}

\usepackage{highlights}

\begin{document}
"""

page = r"""
\lstinputlisting[language=python,title=%(name)s,procnamekeys={def},style=%(name)s]{sample.py}
"""

def theme_name(name):
    return 'highlight/' + name.replace('.theme', '').replace('_', '-')
