from math import tan, radians
from config import Point, Vector
from ray import Ray


class Camera:
    _origin: Point
    _lower_left_corner: Point
    _horizontal: Vector
    _vertical: Vector
    _u: Vector
    _v: Vector
    _w: Vector
    _lens_radius: Vector

    def __init__(self, lookfrom: Point, lookat: Point, vup: Vector, vfov: float,
                 aspect_ratio: float, aperture: float, focus_dist: float) -> None:
        theta = radians(vfov)
        h = tan(theta/2)
        viewport_height = 2.0 * h
        viewport_width = aspect_ratio * viewport_height

        self._w = Vector.unit_vector(lookfrom - lookat)
        self._u = Vector.unit_vector(Vector.cross(vup, self._w))
        self._v = Vector.cross(self._w, self._u)

        self._origin = lookfrom
        self._horizontal = focus_dist * viewport_width * self._u
        self._vertical = focus_dist * viewport_height * self._v
        self._lower_left_corner = self._origin - \
            self._horizontal/2 - self._vertical/2 - focus_dist * self._w

        self._lens_radius = aperture / 2

    def get_ray(self, s: float, t: float) -> Ray:
        rd = self._lens_radius * Vector.random_in_unit_disk()
        offset = self._u * rd.x() + self._v * rd.y()

        return Ray(
            self._origin + offset,
            self._lower_left_corner + s*self._horizontal +
            t*self._vertical - self._origin - offset
        )
