#!/usr/bin/env python

import consts
import os

if __name__ == '__main__':

    names = [consts.theme_name(theme)
             for theme in os.listdir(consts.THEMES_DIR)]

    print consts.preamble

    # generate a "page"  for each style - I  originally had each style
    # demo'd one per page, so this is now a bad naming choice
    l = [consts.page % {'name': name} for name in names]

    # put three style  demos per page, with a  horizontal rule between
    # each. the  embedded newlines are only to  make that intermediate
    # tex file  easier to read. I'm  not thrilled about  how messy the
    # joins and ranges are done  here, but I figured I'd replicate the
    # code in hex2rgb  above (rather than clean that  up - ha!). also,
    # you  should  be  calling  this  with at  least  three  styles  -
    # otherwise things fall apart.
    ll = len(l)
    print '\n\\newpage\n'.join(['\n\\hrulefill\n'.join(l[i:i + 3])
                                for i in range(0, ll, 3)])

    # ...end the document
    print r'\end{document}'
