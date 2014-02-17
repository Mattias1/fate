"""Actors are functions that act on a session.
Sequences of actors are again an actor via the actor decorator."""
from .selectors import (next_full_line, previous_full_line,
                        previous_char, next_char, next_white_space,
                        previous_white_space, empty_after,
                        empty_before, local_pattern_selector, empty)
from .operators import change_after, change_before, delete
from .clipboard import copy, paste_after, paste_before, clear
from .action import compose
from . import modes


def escape(session):
    """Escape"""
    if session.selection_mode != modes.SELECT_MODE:
        modes.select_mode(session)
    else:
        empty(session)


def undo(session):
    """Undo"""
    session.actiontree.undo()


def redo(session):
    """Redo"""
    session.actiontree.redo()

select_indent = local_pattern_selector(r'(?m)^([ \t]*)[^ \t]', group=1)

open_line_after = compose(modes.select_mode, empty_after,
                        next_full_line,
                        select_indent, copy,
                        next_full_line, change_after('\n', 0),
                        previous_char, empty_before, paste_before,
                        clear)

open_line_before = compose(modes.select_mode, empty_before,
                         next_full_line,
                         select_indent, copy,
                         next_full_line, change_before('\n', 0),
                         next_char, empty_before, paste_before,
                         clear)

cut = compose(copy, delete)