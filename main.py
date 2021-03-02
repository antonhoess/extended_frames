#!/usr/bin/python

import tkinter as tk
import argparse

from nested_frame import NestedFrame, ParentsLevelManager
from scroll_frame import ScrollFrame
from aspect_ratio_frame import AspectRatioFrame

"""This module performs example tests on the various classes derived from tkinter.Frame."""

__author__ = "Anton Höß"
__copyright__ = "Copyright 2021"
__credits__ = list()
__license__ = "BSD"
__version__ = "0.1"
__maintainer__ = "Anton Höß"
__email__ = "anton.hoess42@gmail.com"
__status__ = "Development"


class TestGui:
    def test_gui_nested_frame(self):
        self._root = tk.Tk()
        self._root.title("NestedFrame-Test")

        # Nested frame test
        ###################
        frm = self._root
        parents = ParentsLevelManager()

        # Nested Frame can be used like normal Frames but also with their speciality
        # to make the code appear nested the way as the frames do
        with NestedFrame(frm, parents=parents, bg="blue") as frm:
            frm.pack(fill=tk.X, side=tk.LEFT, padx=5)

            # Just a normal nested frame, but using a ParentLevelManager
            # -> No more need for "frm = frm.parent" at the end of each block
            with NestedFrame(frm, parents=parents) as frm:
                frm.pack(side=tk.TOP, padx=5)
                tk.Label(frm, text="x", width=9, bg="yellow", anchor=tk.W).pack(side=tk.LEFT)

                # Go deeper one more step to show that jumping back two levels works
                with NestedFrame(frm, parents=parents) as frm:
                    frm.pack(side=tk.TOP, padx=5)
                    tk.Label(frm, text="x1", width=9, bg="yellow", anchor=tk.W).pack(side=tk.LEFT)

            # Jump back two levels
            with NestedFrame(frm, parents=parents) as frm:
                frm.pack(side=tk.TOP, padx=5)
                tk.Label(frm, text="x2", width=9, bg="yellow", anchor=tk.W).pack(side=tk.LEFT)
                frm = frm.parent

            # This frame hosts a grid
            with NestedFrame(frm, bg="red") as frm:
                frm.pack(side=tk.TOP, padx=5)
                frm.columnconfigure((0, 1, 2), weight=1)
                frm.rowconfigure((0, 1, 2), weight=1)
                tk.Label(frm, text="y", width=9, bg="yellow", anchor=tk.W).grid(row=0, column=0)

                # This frame is one of the grid elements and can get places using grid() as with normal Frames
                with NestedFrame(frm) as frm:
                    frm.grid(row=2, column=2)
                    tk.Label(frm, text="y1", width=9, bg="yellow", anchor=tk.W).pack(side=tk.LEFT)
                    tk.Label(frm, text="y2", width=10, bg="yellow", anchor=tk.E).pack(side=tk.LEFT)
                    frm = frm.parent
                frm = frm.parent

            # NestedFrame can also be used like a normal Frame (without with) and placed somewhere inside the structure
            parent = frm  # If nesting frames like in this block, one needs to hold a list of parent frames
            frm = NestedFrame(frm)
            frm.pack(side=tk.TOP, padx=5)
            tk.Label(frm, text="a", width=9, bg="yellow", anchor=tk.W).pack(side=tk.LEFT)
            frm = parent

            # Continue with a nested frame to show that one can mix nested and normal frames
            with NestedFrame(frm) as frm:
                frm.pack(side=tk.TOP, padx=5)
                tk.Label(frm, text="z", width=9, bg="yellow", anchor=tk.W).pack(side=tk.LEFT)
                frm = frm.parent

            # At the end not needed anymore but it's a good idea to write it
            # in case more elements get added later on
            frm = frm.parent
        # end with
    # end def

    def test_gui_scroll_frame(self):
        # Enable / disable the scrolling functionality
        scroll = True

        self._root = tk.Tk()
        self._root.title("ScrollFrame-Test")

        frm = self._root
        parents = ParentsLevelManager()

        # The following lines just produce a more complex nesting situation to see if it works.
        # For details see comments in test_gui_nested_frame().
        with NestedFrame(frm, parents=parents) as frm:
            frm.pack(expand=True, fill=tk.BOTH)

            expand = False
            fill = tk.BOTH
            with NestedFrame(frm, parents=parents) as frm:
                frm.pack(expand=expand, fill=fill)

                with NestedFrame(frm, parents=parents) as frm:
                    frm.pack(expand=expand, fill=fill)

            with NestedFrame(frm, parents=parents) as frm:
                frm.pack(expand=expand, fill=fill)

            with ScrollFrame(frm, parents=parents, max_width=500, max_height=150, scroll=scroll) as self._scf:
                self._scf.pack(expand=True, fill=tk.BOTH)

                # Add some widgets to occupy some space
                for i in range(20):
                    x = tk.Checkbutton(self._scf, text="*" * 50 + f"{i}")
                    x.pack(anchor=tk.W, side=tk.TOP)
                    x.configure(bg="light blue")
                # end for
            # end with
        # end with

        # Just a label
        x = tk.Label(self._root, text="x", width=9, bg="yellow", anchor=tk.W)
        x.pack(side=tk.TOP, expand=False, fill=tk.Y)

        # Button to add new list elements
        btn = tk.Button(self._root, text="Add list entry")
        btn.pack(side=tk.TOP, expand=False, fill=tk.Y)

        def add_entry(_event):
            tk.Checkbutton(self._scf, text="*" * 50 + f"{self._i}").pack(anchor=tk.W, side=tk.TOP)
            self._i += 1
        # end def

        self._i = 100
        btn.bind("<Button-1>", add_entry)

        # Set come background colors to distinguish the different window areas
        self._root.configure(bg="pink")
        if scroll:
            self._scf.frm_base.configure(bg="green")
            self._scf.configure(bg="red")
            self._scf.canvas.configure(bg="gray")
        # end if
    # end def

    def test_gui_aspect_ratio_frame(self):
        aspect_ratio = 2.0 / 1.0  # None

        self._root = tk.Tk()
        self._root.title("AspectRatioFrame-Test")
        self._root.geometry(f"{600}x{400}")

        frm = self._root
        parents = ParentsLevelManager()

        # The following lines just produce a more complex nesting situation to see if it works.
        # For details see comments in test_gui_nested_frame().
        with NestedFrame(frm, parents=parents) as frm:
            frm.pack(expand=True, fill=tk.BOTH)

            expand = False
            fill = tk.BOTH
            with NestedFrame(frm, parents=parents) as frm:
                frm.pack(expand=expand, fill=fill)

                with NestedFrame(frm, parents=parents) as frm:
                    frm.pack(expand=expand, fill=fill)

            with NestedFrame(frm, parents=parents) as frm:
                frm.pack(expand=expand, fill=fill)

            with AspectRatioFrame(frm, parents=parents, aspect_ratio=aspect_ratio, anchor=tk.SE, bg="blue") as frm:
                frm.pack(expand=True, fill=tk.BOTH)
                # frm.aspect_ratio = 3  # None
                frm.anchor = tk.CENTER

                tk.Label(frm, text="inner content", bg="bisque").pack(side=tk.TOP)
            # end with

        tk.Label(self._root, text="outer content", bg="red").pack(side=tk.TOP)
    # end def

    def run(self):
        self._root.mainloop()
    # end def
# end class


def main():
    nested_frame = "NestedFrame"
    scroll_frame = "ScrollFrame"
    aspect_ratio_frame = "AspectRatioFrame"

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", action="append", required=True,
                        choices=[nested_frame, scroll_frame, aspect_ratio_frame],
                        help="Defines the test to perform. Multiple tests can be started at one.")
    args = parser.parse_args()

    # Run the tests
    gui = TestGui()

    if nested_frame in args.test:
        gui.test_gui_nested_frame()
    # end if

    if scroll_frame in args.test:
        gui.test_gui_scroll_frame()
    # end if

    if aspect_ratio_frame in args.test:
        gui.test_gui_aspect_ratio_frame()
    # end if

    gui.run()
# end def


if __name__ == "__main__":
    main()
# end if
