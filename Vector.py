from math import sqrt


class vec3:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z
        
    def __str__(self):
        return f'Vec3({self.x}, {self.y}, {self.z})'

    def __add__(self, other):
        return vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float):
            return vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: float):
        return self.__mul__(scalar)

    def __truediv__(self, other):
        return vec3(self.x / other, self.y / other, self.z / other)

    def __neg__(self):
        return vec3(-self.x, -self.y, -self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y or self.z != other.z

    def __getitem__(self, index):
        return [self.x, self.y, self.z][index]

    def __setitem__(self, index, value):
        [self.x, self.y, self.z][index] = value

    def magnitude(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        return vec3(self.y * other.z - self.z * other.y,
                    self.z * other.x - self.x * other.z,
                    self.x * other.y - self.y * other.x)
        
    def normalize(self):
        return self / self.magnitude()
    
    def translate(self, translation):
        return self + translation
    
    def scale(self, scale: float):
        return self * scale