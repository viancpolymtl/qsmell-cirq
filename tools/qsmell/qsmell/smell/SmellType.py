""" Smell interface. """

from enum import Enum
from .CG import *
from .ROC import *
from .NC import *
from .LC import *
from .IM import *
from .IdQ import *
from .IQ import *
from .AQ import *
from .LPQ import *

class SmellType(Enum):
    CG  = CG()
    ROC = ROC()
    NC  = NC()
    LC  = LC()
    IM  = IM()
    IdQ = IdQ()
    IQ  = IQ()
    AQ  = AQ()
    LPQ = LPQ()

    def __str__(self):
        return self.value.name

    def __repr__(self):
        return str(self)

    @staticmethod
    def argparse(s):
        try:
            return SmellType[s]
        except KeyError:
            return s
