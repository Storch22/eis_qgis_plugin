import numpy as np
from OpenGL.GL import *  # noqa

from ... import QtGui
from ... import functions as fn
from ..GLGraphicsItem import GLGraphicsItem

__all__ = ["GLLinePlotItem"]


class GLLinePlotItem(GLGraphicsItem):
    """Draws line plots in 3D."""

    def __init__(self, parentItem=None, **kwds):
        """All keyword arguments are passed to setData()"""
        super().__init__(parentItem=parentItem)
        glopts = kwds.pop("glOptions", "additive")
        self.setGLOptions(glopts)
        self.pos = None
        self.mode = "line_strip"
        self.width = 1.0
        self.color = (1.0, 1.0, 1.0, 1.0)
        self.setData(**kwds)

    def setData(self, **kwds):
        """
        Update the data displayed by this item. All arguments are optional;
        for example it is allowed to update vertex positions while leaving
        colors unchanged, etc.

        ====================  ==================================================
        **Arguments:**
        ------------------------------------------------------------------------
        pos                   (N,3) array of floats specifying point locations.
        color                 (N,4) array of floats (0.0-1.0) or
                              tuple of floats specifying
                              a single color for the entire item.
        width                 float specifying line width
        antialias             enables smooth line drawing
        mode                  'lines': Each pair of vertexes draws a single line
                                       segment.
                              'line_strip': All vertexes are drawn as a
                                            continuous set of line segments.
        ====================  ==================================================
        """
        args = ["pos", "color", "width", "mode", "antialias"]
        for k in kwds.keys():
            if k not in args:
                raise Exception(
                    "Invalid keyword argument: %s (allowed arguments are %s)"
                    % (k, str(args))
                )
        self.antialias = False
        if "pos" in kwds:
            pos = kwds.pop("pos")
            self.pos = np.ascontiguousarray(pos, dtype=np.float32)
        if "color" in kwds:
            color = kwds.pop("color")
            if isinstance(color, np.ndarray):
                color = np.ascontiguousarray(color, dtype=np.float32)
            self.color = color
        for k, v in kwds.items():
            setattr(self, k, v)
        self.update()

    def paint(self):
        if self.pos is None:
            return
        self.setupGLState()

        glEnableClientState(GL_VERTEX_ARRAY)

        try:
            glVertexPointerf(self.pos)

            if isinstance(self.color, np.ndarray):
                glEnableClientState(GL_COLOR_ARRAY)
                glColorPointerf(self.color)
            else:
                color = self.color
                if isinstance(color, str):
                    color = fn.mkColor(color)
                if isinstance(color, QtGui.QColor):
                    color = color.getRgbF()
                glColor4f(*color)
            glLineWidth(self.width)

            if self.antialias:
                glEnable(GL_LINE_SMOOTH)
                glEnable(GL_BLEND)
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

            if self.mode == "line_strip":
                glDrawArrays(GL_LINE_STRIP, 0, self.pos.shape[0])
            elif self.mode == "lines":
                glDrawArrays(GL_LINES, 0, self.pos.shape[0])
            else:
                raise Exception(
                    "Unknown line mode '%s'. (must be 'lines' or 'line_strip')"
                    % self.mode
                )

        finally:
            glDisableClientState(GL_COLOR_ARRAY)
            glDisableClientState(GL_VERTEX_ARRAY)
