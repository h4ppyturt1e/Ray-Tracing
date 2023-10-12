from Vector import vec3
from numpy import clip as clamp
from math import pow, sqrt


class Color:
    def __init__(self, r: float = 0, g: float = 0, b: float = 0):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return f'Color({self.r}, {self.g}, {self.b})'

    def __mul__(self, scalar):
        if isinstance(scalar, Color):
            return Color(self.r * scalar.r, self.g * scalar.g, self.b * scalar.b)
        return Color(self.r * scalar, self.g * scalar, self.b * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __add__(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b)

    def __truediv__(self, scalar):
        return Color(self.r / scalar, self.g / scalar, self.b / scalar)

    def to_255(self):
        return clamp((self.r * 255.0, self.g * 255.0, self.b * 255.0), 0, 255)


class Ray:
    def __init__(self, origin: vec3, direction: vec3):
        self.origin = origin
        self.direction = direction

    def __str__(self):
        return \
            f"Ray: \n\
        origin={self.origin}, \n\
        direction={self.direction}"

    def reflect(self, at: vec3, normal: vec3):
        return Ray(at, self.direction - 2 * self.direction.dot(normal) * normal)


class Setup:
    def __init__(self, n: float = None,
                 l: float = None,
                 r: float = None,
                 t: float = None,
                 b: float = None,
                 res: tuple = (0, 0),
                 background: Color = Color(0, 0, 0),
                 ambient: Color = Color(0, 0, 0),
                 output_fn: str = ""):
        self.n = n
        self.l = l
        self.r = r
        self.t = t
        self.b = b
        self.res = res
        self.background = background
        self.ambient = ambient
        self.output_fn = output_fn

    def __str__(self):
        return \
            f"Setup: \n\
        n={self.n}, \n\
        l={self.l}, \n\
        r={self.r}, \n\
        t={self.t}, \n\
        b={self.b}, \n\
        res={self.res}, \n\
        background={self.background}, \n\
        ambient={self.ambient}, \n\
        output_fn={self.output_fn}"


class Sphere:
    def __init__(self, name: str = "",
                 position: vec3 = vec3(0, 0, 0),
                 scale: vec3 = vec3(0, 0, 0),
                 color: Color = Color(0, 0, 0),
                 Ka: float = None,
                 Kd: float = None,
                 Ks: float = None,
                 Kr: float = None,
                 n: int = None):
        self.name = name
        self.position = position
        self.scale = scale
        self.color = color
        self.Ka = Ka
        self.Kd = Kd
        self.Ks = Ks
        self.Kr = Kr
        self.n = n

    def __str__(self):
        return \
            f"{self.name}: \n\
        position={self.position},\n\
        scale={self.scale}, \n\
        color={self.color}, \n\
        coefficients=({self.Ka}, {self.Kd}, {self.Ks}, {self.Kr}), \n\
        specular exponent={self.n}"

    def transform(self, vector: vec3):
        x = self.scale.x * vector.x
        y = self.scale.y * vector.y
        z = self.scale.z * vector.z
        return vec3(x, y, z)

    def inverse_transform(self, vector: vec3):
        x = vector.x / self.scale.x
        y = vector.y / self.scale.y
        z = vector.z / self.scale.z
        return vec3(x, y, z)

    def normal(self, point: vec3):
        # inverse transform points
        point = self.inverse_transform(point)
        position = self.inverse_transform(self.position)

        # compute normal
        normal = (point - position).normalize()

        return normal

    def intersections(self, ray: Ray):
        # inverse transform rays
        origin = self.inverse_transform(ray.origin)
        direction = self.inverse_transform(ray.direction)
        position = self.inverse_transform(self.position)

        # compute intersections
        a = direction.dot(direction)
        b = 2 * direction.dot(origin - position)
        c = (origin - position).dot(origin - position) - 1

        discriminant = b*b - 4*a*c

        if discriminant < 0:
            return None

        t1 = (-b + sqrt(discriminant)) / (2 * a)
        t2 = (-b - sqrt(discriminant)) / (2 * a)
        t = min(t1, t2)
        if t <= 0:
            return None

        return self.transform(origin + t * direction)


class Light:
    def __init__(self, name: str = "",
                 position: vec3 = vec3(0, 0, 0),
                 intensity: Color = Color(0, 0, 0)):
        self.name = name
        self.position = position
        self.intensity = intensity

    def __str__(self):
        return \
            f"{self.name}: \n\
        position={self.position}, \n\
        intensity={self.intensity}"

    def compute_intensity(self, intersection: vec3, sphere: Sphere):
        light_dir = self.position - intersection
        light_dist = light_dir.magnitude()

        # normalize
        light_dir = light_dir.normalize()

        # get normal vector between intersection and sphere
        normal = sphere.normal(intersection)

        # compute light intensity
        light_intensity = self.intensity / pow(light_dist, 2)
        light_intensity *= max(0, light_dir.dot(normal))
        return light_intensity

    def get_direction(self, point: vec3):
        return (self.position - point).normalize()
