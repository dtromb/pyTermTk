


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

from TermTk.TTkCore.constant import TTkConstant, TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.cfg import *
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.spacer import TTkSpacer
from TermTk.TTkWidgets.frame import TTkFrame
from TermTk.TTkWidgets.button import TTkButton
from TermTk.TTkWidgets.menubar import TTkMenuButton
from TermTk.TTkLayouts.boxlayout import TTkHBoxLayout
from TermTk.TTkLayouts.gridlayout import TTkGridLayout


class TTkTabButton(TTkButton):
    __slots__ = ('_sideEnd', '_tabStatus')
    def __init__(self, *args, **kwargs):
        self._sideEnd = TTkK.NONE
        self._tabStatus = TTkK.Unchecked
        TTkButton.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTabButton' )
        if self._border:
            self.resize(len(self._text)+2, 3)
            self.setMinimumSize(2+len(self._text), 3)
            self.setMaximumSize(2+len(self._text), 3)
        else:
            self.resize(len(self._text)+2, 2)
            self.setMinimumSize(len(self._text)+2, 2)
            self.setMaximumSize(len(self._text)+2, 2)
        self.setFocusPolicy(TTkK.ParentFocus)

    def sideEnd(self):
        return self._sideEnd

    def setSideEnd(self, sideEnd):
        self._sideEnd = sideEnd
        self.update()

    def tabStatus(self):
        return self._tabStatus

    def setTabStatus(self, status):
        self._tabStatus = status
        self.update()

    def paintEvent(self):
        self._canvas.drawTabButton(
            pos=(0,0), size=self.size(),
            small=(not self._border),
            sideEnd=self._sideEnd, status=self._tabStatus,
            label=self.text )


'''
_curentIndex =              2
_labelPos =      [0],[1],  [2],   [3],   [4],
                ╭─┌──┌──────╔══════╗──────┬──────┐─╮
_labels=        │◀│La│Label1║Label2║Label3│Label4│▶│
                ╞═══════════╩══════╩═══════════════╡
                 leftscroller                     rightScroller
'''

class TTkTabBar(TTkWidget):
    __slots__ = (
        '_tabButtons', '_small',
        '_highlighted', '_currentIndex','_lastIndex',
        '_leftScroller', '_rightScroller',
        #Signals
        'currentChanged', 'tabBarClicked')

    def __init__(self, *args, **kwargs):
        self._tabButtons = []
        self._currentIndex = -1
        self._lastIndex = -1
        self._highlighted = -1
        self._tabMovable = False
        self._tabClosable = False
        self._leftScroller = False
        self._rightScroller = False
        self._small = kwargs.get('small',True)
        self._sideBorder = TTkK.LEFT | TTkK.RIGHT

        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkTabs')
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)

        # Signals
        self.currentChanged = pyTTkSignal(int)
        self.tabBarClicked  = pyTTkSignal(int)
        TTkWidget.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_TTkTabs')
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)

    def addTab(self, label):
        self.insertTab(len(self._tabButtons), label)

    def insertTab(self, index, label):
        button = TTkTabButton(parent=self, text=label, border=not self._small)
        self._tabButtons.insert(index,button)
        button.clicked.connect(lambda :self.setCurrentIndex(self._tabButtons.index(button)))
        self._updateTabs()

    def setSideBorder(self, border):
        self._sideBorder |= border

    def unsetSideBorder(self, border):
        self._sideBorder &= ~border

    def currentIndex(self):
        return self._currentIndex

    @pyTTkSlot(int)
    def setCurrentIndex(self, index):
        TTkLog.debug(index)
        if 0 <= index < len(self._tabButtons):
            self._currentIndex = index
            self._offset = index
            self._updateTabs()

    def resizeEvent(self, w, h):
        self._updateTabs()

    def _updateTabs(self):
        w = self.width()
        # Find the tabs used size max size
        maxLen = 0
        sizes = [t.width()-1 for t in self._tabButtons]
        for s in sizes: maxLen += s
        if maxLen <= w:
            self._leftScroller = False
            self._rightScroller = False
            shrink = 1
            offx = 0
        else:
            self._leftScroller = True
            self._rightScroller = True
            w-=4
            shrink = w/maxLen
            offx = 2

        posx=0
        for t in self._tabButtons:
            tmpx = offx+min(int(posx*shrink),w-t.width())
            sideEnd = TTkK.NONE
            if tmpx==0:
                sideEnd |= TTkK.LEFT
            if tmpx+t.width()==self.width():
                sideEnd |= TTkK.RIGHT
            t.move(tmpx,0)
            t.setSideEnd(sideEnd)
            t.setTabStatus(TTkK.Unchecked)
            posx += t.width()-1

        # ZReorder the widgets:
        for i in range(0,max(0,self._currentIndex)):
            self._tabButtons[i].raiseWidget()
        for i in reversed(range(max(0,self._currentIndex),len(self._tabButtons))):
            self._tabButtons[i].raiseWidget()
        if 0 <= self._highlighted < len(self._tabButtons):
            self._tabButtons[self._highlighted].raiseWidget()

        if self._currentIndex == -1:
            self._currentIndex = len(self._tabButtons)-1

        if self._tabButtons:
            self._tabButtons[self._currentIndex].setTabStatus(TTkK.Checked)

        if self._lastIndex != self._currentIndex:
            self._lastIndex = self._currentIndex
            self.currentChanged.emit(self._currentIndex)

        self.update()

    def paintEvent(self):
        if self._small: return
        self._canvas.drawTabWidgetBottomLine(pos=(0,2), size=self.size())

'''
           ┌────────────────────────────┐
           │ Root Layout                │
           │┌────────┬────────┬────────┐│
           ││ Left M │ TABS   │ RightM ││
           │└────────┴────────┴────────┘│
           │┌──────────────────────────┐│
           ││ Layout                   ││
           ││                          ││
           │└──────────────────────────┘│
           └────────────────────────────┘
'''

class TTkTabWidget(TTkFrame):
    __slots__ = (
        '_tabBarTopLayout', '_tabBar', '_topLeftLayout', '_topRightLayout',
        '_tabWidgets',
        # Forward Signals
        'currentChanged', 'tabBarClicked',
        # forward methods
        'currentIndex', 'setCurrentIndex')

    def __init__(self, *args, **kwargs):
        self._tabWidgets = []
        self._tabBarTopLayout = TTkGridLayout()

        TTkFrame.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTabWidget')

        self._tabBar = TTkTabBar(small = not self.border())
        self._topLeftLayout   = None
        self._topRightLayout  = None
        self._tabBarTopLayout.addWidget(self._tabBar,0,1)

        self._tabBar.currentChanged.connect(self._tabChanged)
        self._tabBar.focusChanged.connect(self._focusChanged)


        self.setLayout(TTkGridLayout())
        if self.border():
            self.setPadding(3,1,1,1)
        else:
            self.setPadding(2,0,0,0)

        self.rootLayout().addItem(self._tabBarTopLayout)
        self._tabBarTopLayout.setGeometry(0,0,self._width,self._padt)
        # forwarded methods
        self.currentIndex    = self._tabBar.currentIndex
        self.setCurrentIndex = self._tabBar.setCurrentIndex
        # forwarded Signals
        self.currentChanged = self._tabBar.currentChanged
        self.tabBarClicked  = self._tabBar.tabBarClicked

    @pyTTkSlot(TTkWidget)
    def setCurrentWidget(self, widget):
        for i, w in enumerate(self._tabWidgets):
            if widget == w:
                self.setCurrentIndex(i)
                break

    @pyTTkSlot(int)
    def _tabChanged(self, index):
        for i, widget in enumerate(self._tabWidgets):
            if index == i:
                widget.show()
            else:
                widget.hide()

    @pyTTkSlot(bool)
    def _focusChanged(self, focus):
        return
        if focus:
            tabBorderColor = self._tabBorderColorFocus
        else:
            tabBorderColor = self._tabBorderColor

        for widget in self._tabBarTopLayout.iterWidgets():
            widget.setBorderColor(tabBorderColor)
            widget.update()

    def addMenu(self, text, position=TTkK.LEFT):
        return TTkMenuButton()

    def addTab(self, widget, label):
        widget.hide()
        self._tabWidgets.append(widget)
        self.layout().addWidget(widget)
        self._tabBar.addTab(label)

    def insertTab(self, index, widget, label):
        widget.hide()
        self._tabWidgets.insert(index, widget)
        self.layout().addWidget(widget)
        self._tabBar.insertTab(index, label)

    def resizeEvent(self, w, h):
        self._tabBarTopLayout.setGeometry(0,0,w,self._padt)

    #def paintEvent(self): pass
