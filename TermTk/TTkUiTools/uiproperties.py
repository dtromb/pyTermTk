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

from TermTk.TTkLayouts import TTkLayout, TTkGridLayout, TTkVBoxLayout, TTkHBoxLayout
from TermTk.TTkWidgets import *
from .properties import *

TTkUiProperties = {
    # Widgets
        TTkButton.__name__:         TTkButtonProperties,
        TTkCheckbox.__name__:       TTkCheckboxProperties,
        TTkComboBox.__name__:       TTkComboBoxProperties,
        TTkFrame.__name__:          TTkFrameProperties,
        TTkLabel.__name__:          TTkLabelProperties,
        TTkLineEdit.__name__:       TTkLineEditProperties,
        TTkList.__name__:           TTkListProperties,
        TTkRadioButton.__name__:    TTkRadioButtonProperties,
        TTkResizableFrame.__name__: TTkResizableFrameProperties,
        TTkScrollBar.__name__:      TTkScrollBarProperties,
        TTkSplitter.__name__:       TTkSplitterProperties,
        TTkTextEdit.__name__:       TTkTextEditProperties,
        TTkWidget.__name__:         TTkWidgetProperties,
        TTkWindow.__name__:         TTkWindowProperties,
    # Layouts
        TTkLayout.__name__:         TTkLayoutProperties,
}