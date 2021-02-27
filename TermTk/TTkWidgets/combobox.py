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

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.widget import *
from TermTk.TTkWidgets.button import *
from TermTk.TTkWidgets.table import *
from TermTk.TTkWidgets.resizableframe import *

class TTkComboBox(TTkWidget):
    __slots__ = ('_list', '_id', )
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkCheckbox' )
        # Define Signals
        # self.cehcked = pyTTkSignal()
        self._list = kwargs.get('list', [] )
        self._id = -1
        self.setMinimumSize(5, 1)
        self.setMaximumHeight(1)
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)

    def paintEvent(self):
        color       = TTkCfg.theme.comboboxContentColor
        borderColor = TTkCfg.theme.comboboxBorderColor
        if self._id == -1:
            text = "- select -"
        else:
            text = self._list[self._id]
        w = self.width()

        self._canvas.drawText(pos=(1,0), text=text, width=w-2, alignment=TTkK.CENTER_ALIGN, color=color)
        self._canvas.drawText(pos=(0,0), text="[",    color=borderColor)
        self._canvas.drawText(pos=(w-2,0), text="^]", color=borderColor)

    @pyTTkSlot(int)
    def _callback(self, val):
        self._id = val
        #TTkHelper.removeOverlay()
        self.setFocus()
        self.update()

    def mousePressEvent(self, evt):
        frameHeight = len(self._list) + 2
        frameWidth = self.width()
        if frameHeight > 30: frameHeight = 30
        if frameWidth  < 20: frameWidth = 20

        frame = TTkResizableFrame(layout=TTkGridLayout(), size=(frameWidth,frameHeight))
        table = TTkTable(parent=frame, showHeader=False)
        table.activated.connect(self._callback)
        TTkLog.debug(f"{self._list}")
        for item in self._list:
            table.appendItem([item])
        TTkHelper.overlay(self, frame, 0, 0)
        self.update()
        return True