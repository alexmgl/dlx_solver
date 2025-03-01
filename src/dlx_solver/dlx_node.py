class Node:
    def __init__(self, c=None, s=None, llink=None, rlink=None, ulink=None, dlink=None):
        self.is_header = False
        self.name = None
        self.c = c            # reference to the column header
        self.s = s            # used for storing the row index (for option rows) or count (in column headers)
        # Initialize circular pointers if not provided.
        self.llink = llink if llink is not None else self
        self.rlink = rlink if rlink is not None else self
        self.ulink = ulink if ulink is not None else self
        self.dlink = dlink if dlink is not None else self

    # Remove self from horizontal list.
    def cover_h(self):
        self.rlink.llink = self.llink
        self.llink.rlink = self.rlink

    # Restore self in horizontal list.
    def uncover_h(self):
        self.rlink.llink = self
        self.llink.rlink = self

    # Remove self from vertical list.
    def cover_v(self):
        self.ulink.dlink = self.dlink
        self.dlink.ulink = self.ulink

    # Restore self in vertical list.
    def uncover_v(self):
        self.dlink.ulink = self
        self.ulink.dlink = self
