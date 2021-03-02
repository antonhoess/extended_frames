from __future__ import annotations
from typing import Optional, Tuple
import tkinter as tk

from nested_frame import NestedFrame, ParentsLevelManager

"""This tkinter.Frame derived class creates a frame that always keeps a given aspect ratio."""

__author__ = "Anton Höß"
__copyright__ = "Copyright 2021"
__credits__ = list()
__license__ = "BSD"
__version__ = "0.1"
__maintainer__ = "Anton Höß"
__email__ = "anton.hoess42@gmail.com"
__status__ = "Development"


class AspectRatioFrame(NestedFrame):
    """An aspect-ratio keeping frame.

    Parameters
    ----------
    master: tk.Misc
        The master widget to place this scrollbar in.
    parents: ParentsLevelManager, optional
        The ParentsLevelManager which automatically handles the level ups of using this frame by "with".
    aspect_ratio : float, optional
        The aspect ratio (= width / height) to keep.
        If not set, no aspect ratio gets enforced and it will behave normally.
    anchor : str, default tk.CENTER
        Defines where to anchor the (in one dimension shrank) inner frame.
        Valid values are: tk.N, tk.NE, tk.E, tk.SE, tk.S, tk.SW, tk.W, tk.NW and tk.CENTER.
    max_height : int, optional
        The max. height of the scrollable frame.
    scroll : bool, default True
        Indicates is the frame shall be scrollable. If not, its internal complexity gets reduced.
    **kwargs
        Keyword arguments passed to tkinter.Frame.
    """

    tag_name = "aspect_ratio_frame"

    def __new__(cls, master: tk.Misc, parents: Optional[ParentsLevelManager] = None,
                aspect_ratio: Optional[float] = None, anchor: Optional[str] = tk.CENTER, **kwargs) -> AspectRatioFrame:
        # Create the aspect ratio frame itself
        frame = super().__new__(cls, master, parents, **kwargs)

        # Create the base frame
        frame._frm_base = tk.Frame(frame.master)

        return frame  # noqa
    # end def

    def __init__(self, master: tk.Misc, parents: Optional[ParentsLevelManager] = None,
                 aspect_ratio: Optional[float] = None, anchor: Optional[str] = tk.CENTER, **kwargs) -> None:
        # Suppress warning of unused variable
        _master = master

        self._aspect_ratio = aspect_ratio
        self._anchor = anchor
        self._configure_funcid = None

        # We need this helper variable to see if there's a change in the values
        # for handling the event binding later on correctly
        self._aspect_ratio = None

        super().__init__(self._frm_base, parents=parents, **kwargs)

        self._set_aspect_ratio(aspect_ratio)
    # end def

    def __repr__(self) -> str:
        return repr(super())
    # end def

    @property
    def frm_base(self) -> tk.frame:
        """Returns the base frame helper widget.
        The main widget (frame) is self and therefore doesn't need a property.
        """

        return self._frm_base
    # end def

    def place(self, *args, **kwargs) -> None:
        """Places the AspectRatioFrame in its parent widget."""

        self._frm_base.place(*args, **kwargs)
    # end def

    def pack(self, *args, **kwargs) -> None:
        """Packs the AspectRatioFrame in its parent widget."""

        self._frm_base.pack(*args, **kwargs)
    # end def

    def grid(self, *args, **kwargs) -> None:
        """Grids the AspectRatioFrame in its parent widget."""

        self._frm_base.grid(*args, **kwargs)
    # end def

    @property
    def aspect_ratio(self) -> Optional[float]:
        """Returns the aspect ratio value.

        Returns
        -------
        aspect_ratio : float, optional
            Aspect ratio.
        """

        return self._aspect_ratio
    # end def

    @aspect_ratio.setter
    def aspect_ratio(self, value: Optional[float]) -> None:
        """Sets the aspect value. See aspect_ratio parameter description in __init__.

        Parameters
        ----------
        value : float
            Aspect ratio.
        """

        self._set_aspect_ratio(value)
    # end def

    @property
    def anchor(self) -> str:
        """Returns the anchor value.

        Returns
        -------
        anchor : float, optional
            Anchor.
        """

        return self._anchor
    # end def

    @anchor.setter
    def anchor(self, value: str) -> None:
        """Sets the anchor. See anchor parameter description in __init__.

        Parameters
        ----------
        value : float
            Anchor.
        """

        self._anchor = value
        self._set_aspect_ratio(self._aspect_ratio)
    # end def

    def _set_aspect_ratio(self, aspect_ratio: Optional[float] = None) -> None:
        """Sets the aspect ratio and handles the necessary binding and unbinding of configure-events.

        Parameters
        ----------
        aspect_ratio : float, optional
            Aspect ratio.
        """

        # If currently bound, unbind before binding again to prevent multiple event bindings
        if self._aspect_ratio:
            self._frm_base.unbind("<Configure>", self._configure_funcid)
        # end if

        self._aspect_ratio = aspect_ratio

        # If a new aspect ratio is given to set, add a new binding
        if self._aspect_ratio:
            self._configure_funcid = self._frm_base.bind("<Configure>", self._on_configure, add="+")
        else:
            super().pack(expand=True, fill=tk.BOTH)
        # end if
    # end def

    @staticmethod
    def _get_anchor_values(anchor: str, parent_width: int, parent_height: int) -> Tuple[int, int]:
        """Returns the corresponding x- and y- offsets for a given anchor. For use in tkinter.Widget.place().
        Surprisingly, depending on the anchor, the anchor on the child widget varies.

        Parameters
        ----------
        anchor : str
            Anchor for the child widget within this parent widget (self).
        parent_width : int
            Width of the parent widget (self) in pixels.
        parent_width : int
            Height of the parent widget (self) in pixels.

        Returns
        -------
        x_offset : int
            X-offset for anchoring the child widget.
        y_offset : int
            Y-offset for anchoring the child widget.
        """
        
        valid_anchors = (tk.N, tk.NE, tk.E, tk.SE, tk.S, tk.SW, tk.W, tk.NW, tk.CENTER)
        if anchor not in valid_anchors:
            raise ValueError(f"Parameter anchor ({anchor}) not in {valid_anchors}")
        # end if

        if anchor == tk.N:
            return int(parent_width / 2), 0

        elif anchor == tk.NE:
            return parent_width, 0

        elif anchor == tk.E:
            return parent_width, int(parent_height / 2)

        elif anchor == tk.SE:
            return parent_width, parent_height

        elif anchor == tk.S:
            return int(parent_width / 2), parent_height

        elif anchor == tk.SW:
            return 0, parent_height

        elif anchor == tk.W:
            return 0, int(parent_height / 2)

        elif anchor == tk.NW:
            return 0, 0

        elif anchor == tk.CENTER:
            return int(parent_width / 2), int(parent_height / 2)
    # end def

    def _on_configure(self, event: tk.Event) -> None:
        """Handles the configure-event and enforces the aspect ratio.
        When this frame (= parent frame) resizes, fit the content into it, either by fixing the width or the height
        and then adjusting the height or width based on the aspect ratio.

        Parameters
        ----------
        event : tk.Event
            Configure-event-object.
        """

        width = getattr(event, "width")
        height = getattr(event, "height")

        ratio = width / height

        if self._aspect_ratio:
            if ratio > self._aspect_ratio:
                desired_height = height
                desired_width = int(height * self._aspect_ratio)
            else:
                desired_width = width
                desired_height = int(width / self._aspect_ratio)
            # end if

        else:
            desired_width = width
            desired_height = height
        # end if

        # Place the window, give it an explicit size and set the offset for making it centered
        anchor = self._anchor
        x, y = self._get_anchor_values(anchor, width, height)
        super().place(x=x, y=y, anchor=anchor, width=desired_width, height=desired_height)
    # end def
# end class
