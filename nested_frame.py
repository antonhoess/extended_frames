from __future__ import annotations
from typing import Optional
import collections
import tkinter as tk

"""This tkinter.Frame derived class allows to define multiple frames in a visually nested manner
in the code using th "with" statement."""

__author__ = "Anton Höß"
__copyright__ = "Copyright 2021"
__credits__ = list()
__license__ = "BSD"
__version__ = "0.1"
__maintainer__ = "Anton Höß"
__email__ = "anton.hoess42@gmail.com"
__status__ = "Development"


class ParentsLevelManager(collections.OrderedDict):
    """A manager that holds and handles the stack of parent widgets/frames. Useful to use a NestedFrame without
    the need to care about the level of nested frames, especially when leaving the scopes using "with".
    """

    def is_level_up(self) -> bool:
        """Indicates if the level of nested "with" block has decreased at least by one,
        i.e. at least one "with" block ended.

        Returns
        -------
        level_up : bool
            Indicates if level up has happened.
        """

        level_up = len(self) > 0 and list(self.values())[-1] is False

        return level_up
    # end def

    def remove_old_levels(self) -> tk.Frame:
        """Checks, if there are old levels, i.e. one or more exited "with" blocks. If so, the levels not valid anymore
        get deleted from the list and the currently valid parent widget/frame gets returned.

        Returns
        -------
        cur_parent : tk.Frame
            eturns the last (correct) parent.
        """

        # Count the number of invalid parents
        cnt = 0
        for frame, valid in reversed(self.items()):
            if not valid:
                cnt += 1
            else:
                break
            # end if
        # end for

        # Set the newest frame (of the remaining valid ones) as the current one
        # (instead of the one given as parameter)
        parent = list(self.keys())[-(cnt + 1)]

        # Remove all frames from old levels no longer used
        parents = list(self.keys())
        for i in range(1, cnt + 1):
            del self[parents[-i]]
        # end for

        # Return current parent
        return parent
# end class


class NestedFrame(tk.Frame):
    """A frame that can be nested using the "with" statement for easily creating a frame hierarchy and
    a visual overview over the hierarchy (by means of python indentation using "with" blocks).

    Parameters
    ----------
    master : tk.Misc
        The parent frame.
    parents: ParentsLevelManager, optional
        The ParentsLevelManager which automatically handles the level ups of using this frame by "with".
    **kwargs
        Keyword arguments passed to tkinter.Frame.
    """

    tag_name = "nested_frame"

    def __new__(cls, master: tk.Misc, parents: Optional[ParentsLevelManager] = None, **kwargs) -> NestedFrame:
        if parents is not None:
            if parents.is_level_up():
                # This is an old frame, i.e. there has been at least one (or more) level ups.
                master = parents.remove_old_levels()
            # end if
        # end if

        frame = super().__new__(cls)
        frame.master = master

        return frame
    # end if

    def __init__(self, master: tk.Misc, parents: Optional[ParentsLevelManager] = None, **kwargs) -> None:
        # Suppress warning of unused variable
        _master = master

        # Use self.master (which was set in __new__) as master,
        # since in __new__ the current valid parent frame got determined
        master = self.master

        if parents is not None:
            # At first add the root frame, if not yet done
            if len(parents) == 0:
                parents[master] = True
            # end if

            # A new (nested) frame - add it to the list
            parents[self] = True
        # end if

        super().__init__(master, **kwargs)
        self._parents = parents
    # end def

    def __repr__(self) -> str:
        return repr(super())
    # end def

    def __enter__(self) -> NestedFrame:
        """Enters the "with" block and returns the object itself (with ... as ...)."""

        return self
    # end def

    def __exit__(self, exception_type: any, exception_value: any, exception_traceback: any) -> bool:
        """Leaves the "with" block and invalidates its parent frame. Doesn't handle exceptions, but propagates them.

        Parameters
        ----------
        exception_type : any
            The exception type.
        exception_value : any
            The exception value.
        exception_traceback: any
            The exception traceback.

        Returns
        -------
        prop_ex: bool
            Indicates if exceptions shall be propagated.
        """

        # Invalidate the parent frame of this frame (self)
        if self._parents is not None:
            self._parents[self] = False
        # end if

        # Propagate exception
        return False
    # end def

    @property
    def parent(self):
        """Returns the parent frame."""

        return self.master
    # end def
# end class
