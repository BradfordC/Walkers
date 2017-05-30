"""Modules for creating a widget-based user interface. See the examples folder 
for sample scripts that use this module."""

import pygame

# The basestring class was removed in Python 3, but we want to keep it to maintain 
# compatibility with previous versions of python.
try:
    __builtins__["basestring"]
except KeyError:
    __builtins__["basestring"] = str

from pgu.gui.theme import Theme
from pgu.gui.style import Style
from pgu.gui.widget import Widget
from pgu.gui.surface import subsurface, ProxySurface
from pgu.gui.const import *

from pgu.gui.container import Container
from pgu.gui.app import App, Desktop
from pgu.gui.table import Table
from pgu.gui.document import Document
#html
from pgu.gui.area import SlideBox, ScrollArea, List

from pgu.gui.form import Form
from pgu.gui.group import Group

from pgu.gui.basic import Spacer, Color, Label, Image, parse_color
from pgu.gui.button import Icon, Button, Switch, Checkbox, Radio, Tool, Link
from pgu.gui.input import Input, Password
from pgu.gui.keysym import Keysym
from pgu.gui.slider import VSlider, HSlider, VScrollBar, HScrollBar
from pgu.gui.select import Select
from pgu.gui.misc import ProgressBar

from pgu.gui.menus import Menus
from pgu.gui.dialog import Dialog, FileDialog
from pgu.gui.textarea import TextArea

from pgu.gui.deprecated import Toolbox, action_open, action_setvalue, action_quit, action_exec
