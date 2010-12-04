#!/usr/bin/python

import sys
import css2tree


preamble = r"""
\documentclass{article}

\usepackage[procnames]{listings}
\usepackage{color}
\usepackage{fullpage}
\usepackage{upquote}

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
"""

# I put the procnamekeys style  here, rather than above, to keep style
# separate from language.
page = r"""
\lstinputlisting[language=python,title=%(style)s,procnamekeys={def},style=%(style)s]{sample.py}
"""


# stackoverflow.com/questions/214359/converting-hex-to-rgb-and-vice-versa
#
# added  three-digit   check  to   correctly  handle  the   w3c  spec,
# c.f. http://www.w3.org/TR/2001/WD-css3-color-20010305#colorunits
def hex2rgb(value):
    """
    Convert a hex string to an rgb tuple.
    """
    value = value.lstrip('#')
    lv = len(value)
    if lv == 3:
        return hex2rgb(''.join([2 * value[i] for i in (0, 1, 2)]))
    return tuple(int(value[i:i + lv/3], 16) for i in range(0, lv, lv/3))


# The  following  functions,  plus  the dictionary  mapping  to  them,
# convert attribute definitions to latex styles. Currently I only have
# those  attributes mapped  that  are actually  used. Attributes  (and
# values) that are used but  not defined here will be silently ignored
# - future expansion should watch for that.
def fontStyle(value):
    if value == 'italic': return r'\itshape'
    return ''

def fontWeight(value):
    if value == 'bold': return r'\bfseries'
    return ''

def color(value):
    return r'\color[RGB]{%d,%d,%d}' % hex2rgb(value)

styleFuncs = {
    'color': color,
    'font-weight': fontWeight,
    'font-style': fontStyle,
    'background-color': color,
    }


def texify(attribs):
    """
    Map the appropriate style function across each attribute in
    `attribs', accumulating the results in a string.
    """
    s = ''.join([ styleFuncs[name](value) if name in styleFuncs else ''
                   for name, value in attribs.items()])
    return s


def extractStyle(tree, which):
    """
    Return the style attributes for selector `which' in the `tree'.
    """
    if which in tree:
        if '|style' in tree[which]:
            return tree[which]['|style']
    return {}

def tree2tex(name, tree):
    """
    Given a style `name' and css `tree' (created through the css2tree
    module), generate a listings-specific style definition.
    """

    # pick out the relevant parts of the tree
    t = tree['pre.sh_sourceCode']

    # pull out the  '|style' member for each style  type.
    basicStyle    = extractStyle(tree, 'pre.sh_sourceCode')
    nameStyle     = extractStyle(t, '.sh_name')
    commentStyle  = extractStyle(t, '.sh_comment')
    stringStyle   = extractStyle(t, '.sh_string')
    keywordStyle  = extractStyle(t, '.sh_keyword')
    functionStyle = extractStyle(t, '.sh_function')

    # begin a style definition
    print '\lstdefinestyle{%s}{' % name

    # it  turns   out  that  all   of  the  included  styles   have  a
    # background-color  defined,  and   that's  only  defined  in  the
    # pre.sh_sourceCode selector.
    if 'background-color' in basicStyle:
        print '  backgroundcolor=%s,' % texify({'background-color':
                                                basicStyle['background-color']})
        del basicStyle['background-color']

    # each style here will derive from the common style
    print '  style=common,'

    print '  basicstyle=%s,' % texify(basicStyle)
    print '  identifierstyle=%s,' % texify(nameStyle)
    print '  commentstyle=%s,' % texify(commentStyle)
    print '  stringstyle=%s,' % texify(stringStyle)
    print '  keywordstyle=%s,' % texify(keywordStyle)
    print '  procnamestyle=%s' % texify(functionStyle)

    print '}'


def main(argc, argv):
    """
    Generate a demo tex file for the given style file(s). The name of
    each style is taken to be the /name/ of each file, and that name
    is included directly in the output tex without any scrubbing.

    Usage: css2tex.py style-file ...
    """
    names = argv[1:]

    # set up the tex file's preamble
    print preamble

    # fill the preamble with style definitions
    for name in names:
        tree = css2tree.css2tree(name)
        tree2tex(name, tree)

    # begin the document...
    print r'\begin{document}'

    # generate a "page"  for each style - I  originally had each style
    # demo'd one per page, so this is now a bad naming choice
    l = [page % {'style': name} for name in names]

    # put three style  demos per page, with a  horizontal rule between
    # each. the  embedded newlines are only to  make that intermediate
    # tex file  easier to read. I'm  not thrilled about  how messy the
    # joins and ranges are done  here, but I figured I'd replicate the
    # code in hex2rgb  above (rather than clean that  up - ha!). also,
    # you  should  be  calling  this  with at  least  three  styles  -
    # otherwise things fall apart.
    ll = len(l)
    print '\n\\newpage\n'.join(['\n\\hrulefill\n'.join(l[i:i + ll/3])
                                for i in range(0, ll, ll/3)])

    # ...end the document
    print r'\end{document}'

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
