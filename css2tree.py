#!/usr/bin/python

import pprint
import re
import sys


cssStyle_re   = re.compile(r'(?P<selectors>.+?)\{(?P<attribs>.+?)\}')
cssAttrib_re  = re.compile(r'\s*(?P<name>.+?):\s*(?P<value>.+?)\s*(?:;|$)')


def parseStyle(style, tree = {}):
    """
    Generates and returns a tree represented by a dictionary such that
    each  node   is  represented  by   the  textual  name   of  nested
    classes. The special  node name '|style' gives the  style for that
    node's parent selector.

    Note:  selectors may possibly  overlap, in  which case  styles are
    /updated/ - repeat attributes  are overwritten, new attributes are
    augmented.

    `style': a re match object representing a style block
    `tree': the tree to build on (default: empty tree)
    """

    # selectors  may  be  nested,  but  there is  no  support  for
    # siblings or grouped selectors
    selectors = style.group('selectors').split()

    # iteratively build a selector tree
    t = tree
    for s in selectors:
        if s not in t:
            t[s] = {}
        t = t[s]

    # extract the attributes that make up this style
    attribs = re.finditer(cssAttrib_re, style.group('attribs'))
    style = dict([a.groups() for a in attribs])

    # update the lowest selector's style
    if '|style' in t:
        t['|style'].update(style)
    else:
        t['|style'] = style

def css2tree(fname, tree = {}):
    """
    Process the css file `fname' in to a tree. See parseStyle() for a
    description of the typical element.
    """

    # rather  than stream parse,  the entire  file is  read in  as one
    # blob, with lines  joined by a whitespace. this  isn't great, but
    # it  simplified a  few kinks  and runs  reasonably fast  even for
    # large input.
    with open(fname, 'r') as f:
        text = ' '.join([l.strip() for l in f])

        # process each style definition
        styles = re.finditer(cssStyle_re, text)
        if styles:
            for style in styles:
                parseStyle(style, tree)

    return tree

def main(argc, argv):
    """
    Generate a tree for the given style file and pretty print the
    top-level keys.

    Usage: css2tree.py style-file
    """
    fname = argv[1]

    tree = css2tree(fname)
    pprint.pprint(tree.keys())

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)

