from ..DataType import DataType

class Vector3(DataType):
    def __init__(self, x:int | float = 0, y:int | float = 0, z:int | float = 0):
        super().__init__()
        self._x = 0
        self._y = 0
        self._z = 0
        if z == None:
            self.set_value(x,y)
        else: self.set_value(x,y,z)
        self.set_type("Vector3")

    def getX(self):
        """
        Getter for the X value. 
        \nReturns an Int/Float or 0 if it was never defined.
        """
        return self._x
    
    def getY(self):
        """
        Getter for the Y value. 
        \nReturns an Int/Float or 0 if it was never defined.
        """
        return self._y

    def getZ(self):
        """
        Getter for the Z value. 
        \nReturns an Int/Float or 0 if it was never defined.
        """
        return self._z

    def get_value(self):
        """
        Getter for the the vectors values. 
        \nReturns an tuple with Int/Floats in the form of (x,y,z)  and a value of 0 for any undefined axes.
        """
        return (self._x, self._y, self._z)
    
    def set_value(self, newX:int | float, newY:int| float, newZ:int| float):
        """
        Sets all values for X, Y and Z. 
        \nAccepts only ints or floats. 
        \nValues that are not ints or floats will be ignored.
        """
        self.setX(newX)
        self.setY(newY)
        self.setZ(newZ)

    def setX(self, newX:int | float):
        """
        Sets value for X axis. 
        \nAccepts only ints or floats. 
        \nValues that are not ints or floats will be ignored.
        """
        if not self.is_int_or_float(newX):
            return
        self._x = newX

    def setY(self, newY:int | float):
        """
        Sets value for Y axis. 
        \nAccepts only ints or floats. 
        \nValues that are not ints or floats will be ignored.
        """
        if not self.is_int_or_float(newY):
            return
        self._y = newY

    def setZ(self, newZ:int | float):
        """
        Sets value for Z axis. 
        \nAccepts only ints or floats. 
        \nValues that are not ints or floats will be ignored.
        """
        if not self.is_int_or_float(newZ):
            return
        self._z = newZ

    def add(self, vector):
        """
        Takes an input vector and adds the two.
        \nValid inputs: Vector3 or Vector2.
        \nIf invalid input: Returns self.
        \nReturns: Vector3.
        \nDoes not change the value for the vector calling the method.
        """
        if not isinstance(vector, Vector3):
            return self
        x = self.getX() + vector.getX()
        y = self.getY() + vector.getY()
        v_z = vector.getZ()
        self_z = self.getZ()
        if v_z and self_z:
            z = self.getZ() + vector.getZ()
        else:
            if v_z:
                z = v_z
            elif self_z:
                z = self_z
            else: z = 0
        return Vector3(x, y, z)

    def difference(self, vector):
        """
        Takes an input vector and finds the differnce subtracting the values of the input vector from the vector with the method called.
        \nValid inputs: Vector3 or Vector2.
        \nIf invalid input: Returns self.
        \nReturns: Vector3.
        \nDoes not change the value for the vector calling the method.
        """
        if not isinstance(vector, Vector3):
            return self
        x = self.getX() - vector.getX()
        y = self.getY() - vector.getY()
        v_z = vector.getZ()
        self_z = self.getZ()
        if v_z and self_z:
            z = self.getZ() - vector.getZ()
        else:
            if v_z:
                z = v_z
            elif self_z:
                z = self_z
            else: z = 0
        return Vector3(x, y, z)

    def scale(self, scaler:int,):
        """
        Multiplies all axis values by the input scaler.
        \nValid inputs: int or float.
        \nIf invalid input: Returns self.
        \nReturns: Vector3.
        \nDoes not change the value for the vector calling the method.
        """
        if not self.is_int_or_float(scaler):
            return self
        x = self.getX() * scaler
        y = self.getY() * scaler
        self_z = self.getZ()
        if self_z:
            z = self.getZ() * scaler
        else: z = 0

        return Vector3(x, y, z)

    def quick_magnitude(self):
        """
        Gives magnitude prior to sqrt.
        \nReturns an int or float value.
        \nPrimary use is for compairing two vectors to deterimine which is larger etc.
        """
        x = self.getX()
        y = self.getY()
        z = self.getZ()
        self_z = self.getZ()
        if self_z:
            z = self_z
        else: z = 0
        return (x*x) + (y*y) + (z*z)
    
    def print(self):
        """
        Prints: X: x_value, Y: y_value, Z: z_value
        """
        if self.getZ():
            print(f"X: {self._x}, Y: {self._y}, Z: {self._z}")
        else:
            print(f"X: {self._x}, Y: {self._y}")