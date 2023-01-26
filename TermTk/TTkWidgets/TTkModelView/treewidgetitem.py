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
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSlot
from TermTk.TTkWidgets import TTkWidget
from TermTk.TTkAbstract.abstractitemmodel import TTkAbstractItemModel


class TTkTreeWidgetItem(TTkAbstractItemModel):
    __slots__ = ('_parent', '_data', '_widgets', '_alignment', '_children', '_expanded', '_selected', '_hidden',
                 '_childIndicatorPolicy', '_icon', '_defaultIcon',
                 '_sortColumn', '_sortOrder', '_hasWidgets', '_parentWidget'
        # Signals
        # 'refreshData'
        )

    def __init__(self, *args, **kwargs):
        # Signals
        # self.refreshData = pyTTkSignal(TTkTreeWidgetItem)
        super().__init__(*args, **kwargs)
        self._hasWidgets = False
        self._children = []
        self._parentWidget = None
        data = args[0] if len(args)>0 and type(args[0])==list else [TTkString()]
        # self._data = [i if issubclass(type(i), TTkString) else TTkString(i) if isinstance(i,str) else TTkString() for i in data]
        self._data, self._widgets = self._processDataInput(data)
        self._alignment = [TTkK.LEFT_ALIGN]*len(self._data)
        self._parent = kwargs.get('parent', None)
        self._childIndicatorPolicy = kwargs.get('childIndicatorPolicy', TTkK.DontShowIndicatorWhenChildless)

        self._defaultIcon = True
        self._expanded = kwargs.get('expanded', False)
        self._selected = kwargs.get('selected', False)
        self._hidden = kwargs.get('hidden', False)
        self._parent = kwargs.get("parent", None)

        self._sortColumn = -1
        self._sortOrder = TTkK.AscendingOrder

        self._icon = ['']*len(self._data)
        self._setDefaultIcon()
        if 'icon' in kwargs:
            self._icon[0] = kwargs['icon']
            self._defaultIcon = False

    def _processDataInputWidget(self, widget, index):
        self._hasWidgets = True
        widget.hide()
        if self._parentWidget:
            widget.setParent(self._parentWidget)
        if hasattr(widget, 'text'):
            ret = widget.text()
            if hasattr(widget,'textChanged'):
                def _updateField(index):
                    def __updateFieldRet(text):
                        self._data[index] = text
                    return __updateFieldRet
                widget.textChanged.connect(_updateField(index))
        else:
            ret = TTkString()
        return ret

    def _processDataInput(self, dataInput):
        retData, retWidgets = [],[]
        for index, i in enumerate(dataInput):
            if issubclass(type(i), TTkString):
                retData.append(i)
                retWidgets.append(None)
            elif isinstance(i,str):
                retData.append(TTkString(i))
                retWidgets.append(None)
            elif issubclass(type(i), TTkWidget):
                retData.append(self._processDataInputWidget(i, index))
                retWidgets.append(i)
            else:
                retData.append(TTkString())
                retWidgets.append(None)
        return retData, retWidgets

    def _setDefaultIcon(self):
        if not self._defaultIcon: return
        self._icon[0] = TTkCfg.theme.tree[0]
        if self._childIndicatorPolicy == TTkK.DontShowIndicatorWhenChildless and self._children or \
           self._childIndicatorPolicy == TTkK.ShowIndicator:
            if self._expanded:
                self._icon[0] = TTkCfg.theme.tree[2]
            else:
                self._icon[0] = TTkCfg.theme.tree[1]

    def setParent(self, parent):
        self._parentWidget = parent
        if self._hasWidgets:
            for widget in [w for w in self._widgets if w]:
                parent.layout().addWidget(widget)
        for c in self._children:
            c.setParent(parent)

    def hasWidgets(self):
        return self._hasWidgets

    def isHidden(self):
        return self._hidden

    def setHidden(self, hide):
        if hide == self._hidden: return
        self._hidden = hide
        self.dataChanged.emit()

    def childIndicatorPolicy(self):
        return self._childIndicatorPolicy

    def setChildIndicatorPolicy(self, policy):
        self._childIndicatorPolicy = policy
        self._setDefaultIcon()

    def addChild(self, child):
        self._children.append(child)
        child._parent = self
        child._sortOrder = self._sortOrder
        child._sortColumn = self._sortColumn
        self._setDefaultIcon()
        self._sort(children=False)
        if self._parentWidget:
            child.setParent(self._parentWidget)
        child.dataChanged.connect(self.emitDataChanged)
        self.dataChanged.emit()

    def addChildren(self, children):
        for child in children:
            self.addChild(child)

    def child(self, index):
        if 0 <= index < len(self._children):
            return self._children[index]
        return None

    def children(self):
        return [x for x in self._children if not x.isHidden()]

    def icon(self, col):
        if col >= len(self._icon):
            return ''
        return self._icon[col]

    def setIcon(self, col, icon):
        if col==0:
            self._defaultIcon = False
        self._icon[col] = icon
        self.dataChanged.emit()

    def textAlignment(self, col):
        if col >= len(self._alignment):
            return TTkK.LEFT_ALIGN
        return self._alignment[col]

    def setTextAlignment(self, col, alignment):
        self._alignment[col] = alignment
        self.dataChanged.emit()

    def data(self, col, role=None):
        if col >= len(self._data):
            return ''
        return self._data[col]

    def widget(self, col, role=None):
        if col >= len(self._data):
            return None
        return self._widgets[col]

    def sortData(self, col):
        return self.data(col)

    def _sort(self, children):
        if self._sortColumn == -1: return
        self._children = sorted(
                self._children,
                key = lambda x : x.sortData(self._sortColumn),
                reverse = self._sortOrder == TTkK.DescendingOrder)
        # Broadcast the sorting to the children
        if children:
            for c in self._children:
                c.dataChanged.disconnect(self.emitDataChanged)
                c.sortChildren(self._sortColumn, self._sortOrder)
                c.dataChanged.connect(self.emitDataChanged)

    def sortChildren(self, col, order):
        self._sortColumn = col
        self._sortOrder = order
        if not self._children: return
        self._sort(children=True)
        self.dataChanged.emit()

    @pyTTkSlot()
    def emitDataChanged(self):
        self.dataChanged.emit()

    # def setDisabled(disabled):
    #    pass

    def setExpanded(self, expand):
        # hide all the widgets if this item is not expanded
        if not expand:
            def _recurseHide(item):
                for c in item._children:
                    if c._hasWidgets:
                        for widget in [w for w in c._widgets if w]:
                            widget.hide()
                    if c._expanded:
                        _recurseHide(c)
            _recurseHide(self)
        self._expanded = expand
        self._setDefaultIcon()
        self.emitDataChanged()

    def setSelected(self, select):
        self._selected = select

    # def isDisabled():
    #     pass

    def isExpanded(self):
        return self._expanded

    def isSelected(self):
        return self._selected

    def size(self):
        if self._expanded:
            return 1 + sum(c.size() for c in self.children())
        else:
            return 1