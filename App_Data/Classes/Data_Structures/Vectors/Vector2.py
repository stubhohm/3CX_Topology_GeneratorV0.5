from .Vector3 import Vector3

class Vector2(Vector3):
    def __init__(self, x:int = 0, y:int = 0):
        super().__init__(x, y, None)
        self.set_type("Vector2")

    def getZ(self):
        """
        Returns None for the Vector2 Class.
        \nInhereted from Vector3 Parent Class.
        """
        return None
    
    def setZ(self, newZ:int):
        """
        Bypassed for the Vector 2 Class.
        \nInhereted from Vector3 Parent Class.
        """
        pass

    def set_value(self, newX, newY):
        return super().set_value(newX, newY, None)
    
    def get_value(self) -> tuple[int, int]:
        """
        Getter for the the vectors values. 
        \nReturns an tuple with Int/Floats in the form of (x,y)  and a value of 0 for any undefined axes.
        """
        x = self.getX()
        y = self.getY()
        return (x, y)

    def add(self, vector):
        """
        Takes an input vector and adds the two.
        \nValid inputs: Vector3 or Vector2.
        \nIf invalid input: Returns self.
        \nReturns: Vector2.
        \nDoes not change the value for the vector calling the method.
        """
        x, y, z = super().add(vector).get_value()
        return Vector2(x, y)

    def difference(self, vector):
        """
        Takes an input vector and finds the differnce subtracting the values of the input vector from the vector with the method called.
        \nValid inputs: Vector3 or Vector2.
        \nIf invalid input: Returns self.
        \nReturns: Vector2.
        \nDoes not change the value for the vector calling the method.
        """
        x, y, z = super().difference(vector).get_value()
        return Vector2(x, y)

    def scale(self, scaler:int):
        x, y, z = super().scale(scaler).get_value()
        return Vector2(x, y)

    def print(self):
        super().print()