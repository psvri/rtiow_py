from typing import Tuple
from math import sqrt
from hittable import HitRecord, Hittable
from config import Vector, Point
from ray import Ray
from material import Material


class Sphere(Hittable):
    center: Point
    radius: float
    mat: Material

    def __init__(self, mat: Material, cen: Point = None, r: float = 0) -> None:
        if cen is not None:
            self.center = cen
        self.radius = r
        self.mat = mat

    def hit(self, r: Ray, t_min: float, t_max: float) -> Tuple[bool, HitRecord]:
        rec = HitRecord()
        oc = r.origin() - self.center
        a = r.direction().length_squared()
        half_b = Vector.dot(oc, r.direction())
        c = oc.length_squared() - self.radius*self.radius

        discriminant = half_b*half_b - a*c
        if discriminant < 0:
            return (False, rec)
        sqrtd = sqrt(discriminant)

        # Find the nearest root that lies in the acceptable range.
        root = (-half_b - sqrtd) / a
        if root < t_min or t_max < root:
            root = (-half_b + sqrtd) / a
            if root < t_min or t_max < root:
                return (False, rec)

        rec.t = root
        rec.p = r.at(rec.t)
        rec.normal = (rec.p - self.center) / self.radius
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        rec.mat = self.mat

        return (True, rec)
