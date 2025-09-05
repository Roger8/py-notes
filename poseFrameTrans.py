import numpy as np

class CPose:
    def __init__(self,x,y,z,A,B,C):
        self.x = x
        self.y = y
        self.z = z
        self.a = A
        self.b = B
        self.c = C # R 

    def current2parent(self,refFrame,currentpose): 
        pass

