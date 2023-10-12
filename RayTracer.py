from typing import List
from Vector import vec3
from Objects import Setup, Ray, Sphere, Light, Color


class RayTracer:
    def __init__(self, setup: Setup, lo_spheres: List[Sphere], lo_lights: List[Light]):
        self.setup = setup
        self.lo_spheres = lo_spheres
        self.lo_lights = lo_lights

    def closest_intersections(self, ray: Ray, lo_spheres: List[Sphere]):
        """ Returns the closest intersection point and the sphere it belongs to """
        closest_sphere = None
        closest_intersection = None
        min_distance = float("inf")

        for sphere in lo_spheres:
            # get the list of intersection points
            intersection = sphere.intersections(ray)

            if intersection is not None:
                distance = (intersection - ray.origin).magnitude()

                if distance + 0.0001 < min_distance:
                    min_distance = distance
                    closest_sphere = sphere
                    closest_intersection = intersection

        return closest_sphere, closest_intersection

    def compute_ambient(self, sphere: Sphere):
        # Ka * Ia * Oc
        ambient = sphere.Ka * self.setup.ambient * sphere.color
        return ambient

    def compute_diffuse(self, sphere: Sphere, light: Light, L: vec3, N: vec3):
        # Kd * I * max(N.L, 0) * Oc
        diffuse = sphere.Kd * light.intensity * max(N.dot(L), 0) * sphere.color
        return diffuse

    def compute_specular(self, ray: Ray, sphere: Sphere, light: Light, L: vec3, N: vec3):
        # R = 2(N.L)N - L
        R = 2 * (N.dot(L) * N) - L
        V = -ray.direction

        # Ks * I * max(R.V, 0)^n
        specular = sphere.Ks * light.intensity * \
            pow(max(R.dot(V), 0), sphere.n)
        return specular

    def trace(self, ray: Ray, depth: int = 0):
        """ Traces a ray and returns the color up to 3 bounces """
        if depth > 3:
            return self.setup.background

        # find closest intersection
        closest_sphere, closest_intersection = self.closest_intersections(
            ray, self.lo_spheres)
        if closest_sphere is None:
            return self.setup.background
        normal = closest_sphere.normal(closest_intersection)

        # compute ambient color
        ambient_color = self.compute_ambient(closest_sphere)

        # compute diffuse and specular colors
        diffuse_color = Color(0, 0, 0)
        specular_color = Color(0, 0, 0)
        for light in self.lo_lights:
            # compute light direction and distance
            light_direction = (
                light.position - closest_intersection).normalize()
            light_distance = (
                light.position - closest_intersection).magnitude()

            # check if light is blocked by another sphere
            shadow_ray = Ray(closest_intersection, light_direction)
            _, shadow_intersection = self.closest_intersections(
                shadow_ray, self.lo_spheres)
            if shadow_intersection and (shadow_intersection - closest_intersection).magnitude() < light_distance:
                continue

            # add diffuse and specular contributions
            diffuse_color += self.compute_diffuse(
                closest_sphere, light, light_direction, normal)
            specular_color += self.compute_specular(
                ray, closest_sphere, light, light_direction, normal)

        # compute reflect color
        reflect_color = self.setup.background
        if closest_sphere.Kr > 0:
            reflect_ray = ray.reflect(closest_intersection, normal)
            reflect_color = self.trace(reflect_ray, depth + 1)

        # combine colors
        color = ambient_color + diffuse_color + \
            specular_color + closest_sphere.Kr * reflect_color

        return color
