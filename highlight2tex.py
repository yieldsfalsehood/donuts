#!/usr/bin/env python

import consts
import lua
import os

lua.execute("LUA_PATH = '%s/?'" % consts.THEMES_DIR)

def hex2rgb(value):
    """
    Convert a hex string to an rgb tuple.
    """
    value = value.lstrip('#')
    lv = len(value)
    if lv == 3:
        return hex2rgb(''.join([2 * value[i] for i in (0, 1, 2)]))
    return tuple(int(value[i:i + lv/3], 16) for i in range(0, lv, lv/3))

def color(value):

    # at least  one theme  (dante) uses a  keyword color name,  in which
    # case I just default to black, until I find a better solution
    if value.startswith('#'):
        return r'\color[RGB]{%d,%d,%d}' % hex2rgb(value)

    return r'\color[RGB]{0,0,0}'

def style(rule):
    colour = lua.eval('%s.Colour' % rule)
    boldQ = lua.eval('%s.Bold' % rule)
    bold = r'\bfseries' if boldQ else ''

    return color(colour) + bold

if __name__ == '__main__':

    print consts.common_style

    for theme in os.listdir(consts.THEMES_DIR):

        lua.require(theme)

        name = consts.theme_name(theme)
        styles = {
            'name':            name,
            'backgroundcolor': style('Canvas'),
            'basicstyle':      style('Default'),
            'identifierstyle': style('Keywords[2]'),
            'commentstyle':    style('BlockComment'),
            'stringstyle':     style('String'),
            'keywordstyle':    style('Keywords[1]'),
            'procnamestyle':   style('Keywords[4]'),
            }

        print consts.listings_style % styles
