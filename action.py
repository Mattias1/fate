"""This module exposes the basic action machinery."""

class Action:
    """Base class for actions."""

    def __init__(self, session, *args):
        """Every object in args must have an undo and a do function."""
        self.session = session

    def _do(self):
        """Do implemented by subclass."""
        pass

    def _undo(self):
        """Undo implemented by subclass."""
        pass

    def undo(self):
        """Undo action."""
        self._undo()

    def do(self, redo=False):
        """Do action."""
        self._do()

        if not redo:
            self.session.actiontree.add(self)
        self.session.OnApplyActor.fire(self)

    def redo(self):
        """Redo action."""
        self.do(redo=True)

def actor(function):
    """Base function for actors."""
    def wrapper(session, preview=False):
        action = function(session)
        if action and not preview:
            action.do()
        else:
            return action

    return wrapper


class CompoundAction(Action):
    """
    This class can be used to compose multiple actions into a single
    action.
    """
    def __init__(self, session, *args):
        """Every object in args must be an Action."""
        Action.__init__(self, session)
        self.sub_actions = tuple(a for a in args if a)

    def __str__(self):
        result = []
        for sub_action in self:
            result.append(str(sub_action))
        return '(' + ', '.join(result) + ')'

    def _undo(self):
        """Undo action."""
        for sub_action in self:
            sub_action._undo()

    def _do(self):
        """Do action."""
        for sub_action in self.sub_actions:
            sub_action._do()

    def __iter__(self):
        """Iterate linearly through all atomic subactions."""
        for sub_action in self.sub_actions:
            if sub_action.__class__ == CompoundAction:
                for sub_sub_action in sub_action:
                    if sub_sub_action != None:
                        yield sub_sub_action
            else:
                if sub_action != None:
                    yield sub_action

    def contains_class(self, _class):
        """
        Check if an atomic subaction of class _class is contained
        in self.
        """
        for sub_action in self:
            if sub_action.__class__ == _class:
                return True
        return False


def compose(*args):
    """
    This function returns the compositional actor from the
    argument actors, and does the resulting actions upon execution.
    """
    def wrapper(session, toplevel=True):
        actionlist = [f(session, toplevel=False)
                      if hasattr(f, 'is_actor') else f(session) for f in args]
        actionlist = [x for x in actionlist if x]
        if not actionlist:
            return
        action = CompoundAction(session, *actionlist)

        if toplevel:
            action.do()
        else:
            return action

    wrapper.is_actor = True
    return wrapper
