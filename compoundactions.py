"""This module contains more complex actions that are built of other primitive actions."""

from . import modes
from . import actions
from .actiontools import Compose
from .selectors import (Empty, EmptyBefore, PreviousFullLine,
                        SelectIndent, NextFullLine, NextChar, PreviousChar)
from .operators import Append, Insert, delete
from .insertoperations import ChangeAfter, ChangeInPlace
from .clipboard import copy, clear, paste_before
from logging import debug
from .repeat import repeatable

def escape(document):
    """Escape"""
    if document.mode != modes.SELECT:
        modes.select_mode(document)
    else:
        return Empty(document)
actions.escape = escape

OpenLineAfter = Compose(modes.select_mode, PreviousFullLine, SelectIndent, copy,
                        NextFullLine, Append('\n'), PreviousChar, EmptyBefore,
                        paste_before, clear, ChangeAfter, name='OpenLineAfter',
                        docs='Open a line after interval')
actions.OpenLineAfter = repeatable(OpenLineAfter)

OpenLineBefore = Compose(modes.select_mode, NextFullLine, SelectIndent, copy,
                         NextFullLine, Insert('\n'), NextChar, EmptyBefore,
                         paste_before, clear, ChangeAfter, name='OpenLineBefore',
                         docs='Open a line before interval')
actions.OpenLineBefore = repeatable(OpenLineBefore)

Cut = Compose(copy, delete, name='Cut', docs='Copy and delete selected text.')
actions.Cut = Cut

CutChange = Compose(Cut, ChangeInPlace,
                    name='CutChange', docs='Copy and change selected text.')
actions.CutChange = repeatable(CutChange)

