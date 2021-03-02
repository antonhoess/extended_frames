from __future__ import annotations
from typing import Optional
import tkinter as tk

from nested_frame import NestedFrame, ParentsLevelManager

"""This tkinter.Frame derived class creates a frame that allows to define a maximum width and height
and allows to scroll its content."""

__author__ = "Anton Höß"
__copyright__ = "Copyright 2021"
__credits__ = list()
__license__ = "BSD"
__version__ = "0.1"
__maintainer__ = "Anton Höß"
__email__ = "anton.hoess42@gmail.com"
__status__ = "Development"


class AutoScrollbar(tk.Scrollbar):
    """A scrollbar that hides itself if it's not needed. Only works if you use the grid geometry manager!

    Parameters
    ----------
    master : tk.Misc
        The master widget to place this scrollbar in.
    **kwargs
        Keyword arguments passed to tkinter.Scrollbar
    """

    def __init__(self, master: tk.Misc, **kwargs):
        super().__init__(master, **kwargs)

        self._active = False
    # end def

    def set(self, lo, hi):
        """Set the fractional values of the slider position (upper and lower ends as value between 0 and 1).

        Parameters
        ----------
        lo : float
            Lower end with a value between 0 and 1.
        hi : float
            Upper end with a value between 0 and 1.
        """
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
            self._active = False
        else:
            self.grid()
            self._active = True

        super().set(lo, hi)
    # end def

    def pack(self, **kwargs):
        raise tk.TclError("Cannot use pack with this widget!")
    # end def

    def place(self, **kwargs):
        raise tk.TclError("Cannot use place with this widget!")
    # end def

    @property
    def active(self):
        return self._active
    # end def
# end class


class ScrollFrame(NestedFrame):
    """A scrollable frame with scrollbars that hide itself if they're not needed and with mouse scroll support.

    Parameters
    ----------
    master: tk.Misc
        The master widget to place this scrollbar in.
    parents: ParentsLevelManager, optional
        The ParentsLevelManager which automatically handles the level ups of using this frame by "with".
    max_width : int, optional
        The max. width of the scrollable frame.
    max_height : int, optional
        The max. height of the scrollable frame.
    max_height : int, optional
        The max. height of the scrollable frame.
    scroll : bool, default True
        Indicates is the frame shall be scrollable. If not, its internal complexity gets reduced.
    **kwargs
        Keyword arguments passed to tkinter.Canvas.
    """

    tag_name = "scroll_frame"

    def __new__(cls, master: tk.Misc, parents: Optional[ParentsLevelManager] = None, max_width: Optional[int] = None,
                max_height: Optional[int] = None, scroll: bool = True, **kwargs) -> ScrollFrame:
        # Create the scroll frame itself
        frame = super().__new__(cls, master, parents, **kwargs)

        if scroll:
            # Base frame which holds the two scrollbars and the canvas. This is necessary to allow the user to use this
            # ScrollFrame in any way he wants (pack, grid, place)
            frame._frm_base = tk.Frame(frame.master)
            # This frame doesn't get pack()ed or grid()ed or place()ed here,
            # since the program using ScrollFrame needs full control over it

            # The vertical scrollbar
            frame._scr_ver = AutoScrollbar(frame._frm_base)
            frame._scr_ver.grid(row=0, column=1, sticky=tk.N + tk.S)

            # The horizontal scrollbar
            frame._scr_hor = AutoScrollbar(frame._frm_base, orient=tk.HORIZONTAL)
            frame._scr_hor.grid(row=1, column=0, sticky=tk.E + tk.W)

            # The canvas - server as a container packing items into it
            frame._canvas = tk.Canvas(frame._frm_base,
                                      yscrollcommand=frame._scr_ver.set,
                                      xscrollcommand=frame._scr_hor.set,
                                      bd=0, highlightthickness=0, relief=tk.RIDGE)
            frame._canvas.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

            # Assign the scrollbars to the canvas view
            frame._scr_ver.config(command=frame._canvas.yview)
            frame._scr_hor.config(command=frame._canvas.xview)

            # Make the canvas expandable
            frame._frm_base.rowconfigure(0, weight=1)
            frame._frm_base.columnconfigure(0, weight=1)

        else:
            # Set the helper widgets to None for the properties
            frame._frm_base = None
            frame._scr_hor = None
            frame._scr_ver = None
            frame._canvas = None
        # end if

        return frame  # noqa
    # end def

    def __init__(self, master: tk.Misc, parents: Optional[ParentsLevelManager] = None, max_width: Optional[int] = None,
                 max_height: Optional[int] = None, scroll: bool = True, **kwargs) -> None:
        # Suppress warning of unused variable
        _master = master

        self._max_width = max_width
        self._max_height = max_height
        self._scroll = scroll

        if self._scroll:
            # Place container frame inside canvas
            self.master = self._canvas  # Necessary to make NestedFrame work properly
            super().__init__(self._canvas, parents=parents, **kwargs)

            # Event bindings
            self.bind("<Configure>", self._reset_scroll_region)
            self._bind_mouse_wheel_event(self._canvas)

            self._update()

        else:
            super().__init__(self.master, parents=parents, **kwargs)
        # end if
    # end def

    def __repr__(self) -> str:
        return repr(super())
    # end def

    @property
    def frm_base(self) -> tk.Frame:
        """Returns the base frame helper widget.
        The main widget (frame) is self and therefore doesn't need a property.
        """

        return self._frm_base
    # end def

    @property
    def scr_hor(self) -> tk.Scrollbar:
        """Returns the horizontal scrollbar helper widget."""

        return self._scr_hor
    # end def

    @property
    def scr_ver(self) -> tk.Scrollbar:
        """Returns the vertical scrollbar helper widget."""

        return self._scr_ver
    # end def

    @property
    def canvas(self) -> tk.Canvas:
        """Returns the canvas helper widget."""

        return self._canvas
    # end def

    def place(self, *args, **kwargs) -> None:
        """Places the ScrollFrame in its parent widget."""

        if self._scroll:
            self._frm_base.place(*args, **kwargs)
        else:
            super().place(*args, **kwargs)
        # end if
    # end def

    def pack(self, *args, **kwargs) -> None:
        """Packs the ScrollFrame in its parent widget."""

        if self._scroll:
            self._frm_base.pack(*args, **kwargs)
        else:
            super().pack(*args, **kwargs)
        # end if
    # end def

    def grid(self, *args, **kwargs) -> None:
        """Grids the ScrollFrame in its parent widget."""

        if self._scroll:
            self._frm_base.grid(*args, **kwargs)
        else:
            super().grid(*args, **kwargs)
        # end if
    # end def

    def _bind_mouse_wheel_event(self, master: tk.Misc) -> None:
        """Binds mouse scroll events (for different OSs) to the master widget.

        Parameters
        ----------
        master : tk.Misc
            The master widget to place this scrollbar in.
        """

        self._bind_tree(master, "<MouseWheel>", self._cb_mouse_wheel_vertical)  # With Windows OS
        self._bind_tree(master, "<Button-4>", self._cb_mouse_wheel_vertical)  # With Linux OS
        self._bind_tree(master, "<Button-5>", self._cb_mouse_wheel_vertical)  # "

        self._bind_tree(master, "<Shift-MouseWheel>", self._cb_mouse_wheel_horizontal)  # With Windows OS
        self._bind_tree(master, "<Shift-Button-4>", self._cb_mouse_wheel_horizontal)  # With Linux OS
        self._bind_tree(master, "<Shift-Button-5>", self._cb_mouse_wheel_horizontal)  # "
    # end def

    def _bind_tree(self, widget: tk.Misc, event: str, callback: callable, add: str = "") -> None:
        """Binds an event to a widget and all its descendants recursively.

        Parameters
        ----------
        widget : tk.Misc
            The widget to bind the callback to.
        event : str
            The event to bind to the widget.
        callback : callable
            The callback to call on event.
        add : str, default ""
            Specifies whether callback will be called additionally ("+") to the other bound function
            or whether it will replace the previous function ("").
        """

        widget.bind(event, callback, add)

        for child in widget.winfo_children():
            self._bind_tree(child, event, callback, add)
        # end for
    # end def

    def _update(self) -> None:
        """Updates the widgets width and height (when its parent's size changes)."""

        self._canvas.create_window(0, 0, anchor=tk.NW, window=self)
        self.update_idletasks()
        self._canvas.config(scrollregion=self._canvas.bbox(tk.ALL))

        if self.winfo_reqwidth() != self._canvas.winfo_width():
            # Update the canvas's width to fit the inner frame
            if self._max_width is not None:
                self._canvas.config(width=min(self._max_width, self.winfo_reqwidth()))
            else:
                self._canvas.config(width=self.winfo_reqwidth())
            # end if
        # end if

        if self.winfo_reqheight() != self._canvas.winfo_height():
            # Update the canvas's height to fit the inner frame
            if self._max_height is not None:
                self._canvas.config(height=min(self._max_height, self.winfo_reqheight()))
            else:
                self._canvas.config(height=self.winfo_reqheight())
            # end if
        # end if
    # end def

    def _reset_scroll_region(self, _event) -> None:
        """Resets the size of the scroll-region to the size of the bounding box around all elements
        when the size of the widget has changed.
        Also binds the mouse scroll events to the probably newly added widgets.

        Parameters
        ----------
        _event
            The event information. Not used.
        """

        # resize scroll region
        self._canvas.configure(scrollregion=self._canvas.bbox(tk.ALL))

        # Bind the mouse scroll events to the probably newly added child widgets
        self._bind_mouse_wheel_event(self._canvas)
    # end def

    def _cb_mouse_wheel(self, event: tk.Event, ver: bool) -> None:
        """The mouse scroll callback that scrolls the window.

        Parameters
        ----------
        event : tk.Event
            The event information.
        ver : bool
            If True, scroll in vertical direction, else scroll in horizontal direction.
        """

        # Respond to Linux or Windows wheel event
        if getattr(event, "num") == 4:
            event.delta = 120

        elif getattr(event, "num") == 5:
            event.delta = -120

        if ver:
            self._canvas.yview_scroll(int(-1 * (event.delta / 120)), tk.UNITS)
        else:
            self._canvas.xview_scroll(int(-1 * (event.delta / 120)), tk.UNITS)
        # end if
    # end def

    def _cb_mouse_wheel_horizontal(self, event: tk.Event) -> None:
        """The horizontal mouse scroll callback.

        Parameters
        ----------
        event : tk.Event
            The event information.
        """

        if self._scr_hor.active:
            self._cb_mouse_wheel(event, ver=False)
    # end def

    def _cb_mouse_wheel_vertical(self, event: tk.Event) -> None:
        """The vertical mouse scroll callback.

        Parameters
        ----------
        event : tk.Event
            The event information.
        """

        if self._scr_ver.active:
            self._cb_mouse_wheel(event, ver=True)
    # end def
# end class
