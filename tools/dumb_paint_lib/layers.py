# MIT License
#
# Copyright (c) 2024 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

__all__ = ['Layers','LayerData']

import sys, os

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

class LayerData():
    __slots__ = ('_name','_data')
    def __init__(self,name:ttk.TTkString=ttk.TTkString('New'),data=None) -> None:
        self._name:ttk.TTkString = ttk.TTkString(name) if type(name)==str else name
        self._data = data
    def name(self):
        return self._name
    def setName(self,name):
        self._name = name
    def data(self):
        return self._data
    def setData(self,data):
        self._data = data

class _layerButton(ttk.TTkWidget):
    classStyle = {
                'default':     {'color': ttk.TTkColor.fg("#dddd88")+ttk.TTkColor.bg("#000044"),
                                'borderColor': ttk.TTkColor.fg('#CCDDDD'),
                                'grid':1},
                'disabled':    {'color': ttk.TTkColor.fg('#888888'),
                                'borderColor':ttk.TTkColor.fg('#888888'),
                                'grid':0},
                'hover':       {'color': ttk.TTkColor.fg("#dddd88")+ttk.TTkColor.bg("#000050")+ttk.TTkColor.BOLD,
                                'borderColor': ttk.TTkColor.fg("#FFFFCC")+ttk.TTkColor.BOLD,
                                'grid':1},
                'selected':     {'color': ttk.TTkColor.fg("#dddd88")+ttk.TTkColor.bg("#004488"),
                                'borderColor': ttk.TTkColor.fg("#FFFF00"),
                                'grid':0},
                'unchecked':   {'color': ttk.TTkColor.fg("#dddd88")+ttk.TTkColor.bg("#000044"),
                                'borderColor': ttk.TTkColor.RST,
                                'grid':3},
                'clicked':     {'color': ttk.TTkColor.fg("#FFFFDD")+ttk.TTkColor.BOLD,
                                'borderColor': ttk.TTkColor.fg("#DDDDDD")+ttk.TTkColor.BOLD,
                                'grid':0},
                'focus':       {'color': ttk.TTkColor.fg("#dddd88")+ttk.TTkColor.bg("#000044")+ttk.TTkColor.BOLD,
                                'borderColor': ttk.TTkColor.fg("#ffff00") + ttk.TTkColor.BOLD,
                                'grid':1},
            }

    __slots__ = ('_layer','_first', '_isSelected',
               # signals
               'clicked'
               )
    def __init__(self, layer:LayerData, **kwargs):
        self.clicked = ttk.pyTTkSignal(_layerButton)
        self._layer:LayerData = layer
        self._isSelected = False
        self._first = True
        super().__init__(**kwargs)

    def mouseReleaseEvent(self, evt) -> bool:
        self.clicked.emit(self)
        return True

    def paintEvent(self, canvas: ttk.TTkCanvas):
        # if self.isEnabled() and self._checkable:
        #     if self._checked:
        #         style = self.style()['checked']
        #     else:
        #         style = self.style()['unchecked']
        #     if self.hasFocus():
        #         borderColor = self.style()['focus']['borderColor']
        #     else:
        #         borderColor = style['borderColor']
        # else:
        #    style = self.currentStyle()
        #    borderColor = style['borderColor']
        if self._isSelected:
            style = self.style()['selected']
        else:
            style = self.currentStyle()
        borderColor = style['borderColor']
        textColor   = style['color']
        w,h = self.size()
        canvas.drawText(    pos=(0,0),text=f"     ┏{'━'*(w-7)}┓",color=borderColor)
        canvas.drawText(    pos=(0,2),text=f"     ┗{'━'*(w-7)}┛",color=borderColor)
        if self._first:
            canvas.drawText(pos=(0,1),text=f" □ ▣ ┃{' '*(w-7)}┃",color=borderColor)
        else:
            canvas.drawText(pos=(0,1),text=f" □ ▣ ╽{' '*(w-7)}╽",color=borderColor)
        canvas.drawTTkString(pos=(7,1),text=self._layer.name(), color=textColor)

class LayerScrollWidget(ttk.TTkAbstractScrollView):
    __slots__ = ('_layers','_selected',
                 # Signals
                 'layerSelected','layerAdded','layerDeleted')
    def __init__(self, **kwargs):
        self.layerSelected = ttk.pyTTkSignal(LayerData)
        self.layerAdded = ttk.pyTTkSignal(LayerData)
        self.layerDeleted = ttk.pyTTkSignal(LayerData)
        self._selected = None
        self._layers:list[_layerButton] = []
        super().__init__(**kwargs)
        self.viewChanged.connect(self._placeTheButtons)

    def viewFullAreaSize(self) -> tuple:
        _,_,w,h = self.layout().fullWidgetAreaGeometry()
        return w,h

    def viewDisplayedSize(self) -> tuple:
        return self.size()

    def maximumWidth(self):   return 0x10000
    def maximumHeight(self):  return 0x10000
    def minimumWidth(self):   return 0
    def minimumHeight(self):  return 0

    @ttk.pyTTkSlot(_layerButton)
    def _clickedLayer(self, layerButton:_layerButton):
        if sel:=self._selected:
            sel._isSelected = False
            sel.update()
        self._selected = layerButton
        layerButton._isSelected = True
        self.layerSelected.emit(layerButton._layer)
        self.update()

    @ttk.pyTTkSlot()
    def addLayer(self,name=None):
        name = name if name else f"Layer #{len(self._layers)}"
        _l=LayerData(name=name)
        newLayerBtn:_layerButton  = _layerButton(parent=self,layer=_l)
        self._layers.insert(0,newLayerBtn)
        if sel:=self._selected: sel._isSelected = False
        self._selected = newLayerBtn
        newLayerBtn._isSelected = True
        newLayerBtn.clicked.connect(self._clickedLayer)
        self.viewChanged.emit()
        self._placeTheButtons()
        self.layerAdded.emit(newLayerBtn._layer)
        return _l

    def _placeTheButtons(self):
        w,h = self.size()
        for i,l in enumerate(self._layers):
            l._first = i==0
            l.setGeometry(0,i*2,w,3)
            l.lowerWidget()
        self.update()

    @ttk.pyTTkSlot()
    def delLayer(self):
        self._layers.remove()

class Layers(ttk.TTkGridLayout):
    __slots__ = ('_scrollWidget',
                 # Forward Methods
                 'addLayer',
                 # Forward Signals
                 'layerSelected','layerAdded','layerDeleted','layerOrderChanged')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._scrollWidget = _lsw = LayerScrollWidget()
        _sa = ttk.TTkAbstractScrollArea(scrollWidget=self._scrollWidget,minWidth=16)
        _sa.setViewport(_lsw)
        self.addWidget(_sa,0,0,1,5)
        self.addWidget(btnAdd :=ttk.TTkButton(text='add')           ,1,0)
        self.addWidget(btnUp  :=ttk.TTkButton(text='▲',maxWidth=3)  ,1,1)
        self.addWidget(btnDown:=ttk.TTkButton(text='▼',maxWidth=3)  ,1,2)
        # self.addItem(ttk.TTkLayout(),1,3)
        self.addWidget(btnDel :=ttk.TTkButton(text=ttk.TTkString('del',ttk.TTkColor.RED),maxWidth=5),1,4)

        btnAdd.setToolTip( "Create a new Layer\nand add it to the image")
        btnDel.setToolTip( "Delete the selected Layer")
        btnUp.setToolTip(  "Raise the selected Layer one step")
        btnDown.setToolTip("Lower the selected Layer one step")

        btnAdd.clicked.connect(_lsw.addLayer)
        btnDel.clicked.connect(_lsw.delLayer)

        # forward signals
        self.layerSelected = _lsw.layerSelected
        self.layerSelected = _lsw.layerSelected
        self.layerAdded    = _lsw.layerAdded
        self.layerDeleted  = _lsw.layerDeleted

        # forward methods
        self.addLayer = _lsw.addLayer
