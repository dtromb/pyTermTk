#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import TermTk.libbpytop as lbt
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import *

class TTkHelper:
    # TODO: Add Setter/Getter
    _rootCanvas = None
    _updateWidget = []
    _paintBuffer  = []

    @staticmethod
    def addUpdateWidget(widget):
        if widget not in TTkHelper._updateWidget:
            TTkHelper._updateWidget.append(widget)

    @staticmethod
    def addPaintBuffer(canvas):
        if canvas is not TTkHelper._rootCanvas:
            if canvas not in TTkHelper._paintBuffer:
                TTkHelper._paintBuffer.append(canvas)

    @staticmethod
    def registerRootCanvas(canvas):
        TTkHelper._rootCanvas = canvas
        TTkHelper._paintBuffer = []
        TTkHelper._updateWidget = []

    @staticmethod
    def paintAll():
        if TTkHelper._rootCanvas is None:
            return
        processed = []
        for widget in TTkHelper._updateWidget:
            processed.append(widget)
            widget.paintEvent()
            widget.paintChildCanvas()
            p = widget.parentWidget()
            #if p in TTkHelper._updateWidget and p not in processed:
            widget.paintNotifyParent()
        TTkHelper._updateWidget = []
        TTkHelper._rootCanvas.pushToTerminal(0, 0, TTkGlbl.term_w, TTkGlbl.term_h)

    @staticmethod
    def absPos(widget) -> (int,int):
        ppos = TTkHelper.absParentPos(widget)
        wpos = widget.pos()
        return (wpos[0]+ppos[0], wpos[1]+ppos[1])

    @staticmethod
    def absParentPos(widget) -> (int,int):
        if widget is None or widget.parentWidget() is None:
            return (0, 0)
        return TTkHelper.absPos(widget.parentWidget())

    class Color(lbt.Color): pass
    class Mv(lbt.Mv): pass
