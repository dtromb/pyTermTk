# MIT License
#
# Copyright (c) 2023 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
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

# Yaml is not included by default
# import yaml
import json

from .superobj import SuperWidget

import TermTk as ttk


class WindowEditorView(ttk.TTkAbstractScrollView):
    def __init__(self, *args, **kwargs):
        self.weModified = ttk.pyTTkSignal()
        self.thingSelected = ttk.pyTTkSignal(ttk.TTkWidget, ttk.TTkWidget)
        super().__init__(*args, **kwargs)
        self.viewChanged.connect(self._viewChangedHandler)
        self._ttk = SuperWidget(wid=ttk.TTkWidget(name = 'TTk'), weModified=self.weModified, thingSelected=self.thingSelected, pos=(4,2), size=(self.width()-8,self.height()-4), superRootWidget=True)
        self.layout().addWidget(self._ttk)

    def getTTk(self):
        return self._ttk

    def getJson(self):
        return json.dumps(self._ttk.dumpDict(), indent=1)

    def resizeEvent(self, w, h):
        self._ttk.resize(w-8,h-4)
        return super().resizeEvent(w, h)

    @ttk.pyTTkSlot()
    def _viewChangedHandler(self):
        x,y = self.getViewOffsets()
        self.layout().setOffset(-x,-y)

    def viewFullAreaSize(self):
        _,_,w,h = self.layout().fullWidgetAreaGeometry()
        return w+1, h+1

    def viewDisplayedSize(self):
        return self.size()

    def paintEvent(self):
        w,h = self.size()
        self._canvas.fill(pos=(0,0),size=(w,h), char="╳", color=ttk.TTkColor.fg("#444400")+ttk.TTkColor.bg("#000044"))

class WindowEditor(ttk.TTkAbstractScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setViewport(wev := WindowEditorView())
        self.getTTk  = wev.getTTk
        self.getJson = wev.getJson