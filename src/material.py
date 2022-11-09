from math import sqrt
from random import random
from abc import ABC, abstractmethod
from typing import ClassVar, Tuple
from ray import Ray
from hittable import HitRecord
from config import Color, Vector


class Material(ABC):

    @abstractmethod
    def scatter(self, r_in: Ray, rec: HitRecord) -> Tuple[bool, Color, Ray]:
        pass


class Lambertian(Material):
    albedo: ClassVar[Color]

    def __init__(self, a: Color) -> None:
        self.albedo = a

    def scatter(self, r_in: Ray, rec: HitRecord) -> Tuple[bool, Color, Ray]:
        scatter_direction = rec.normal + Vector.random_unit_vector()
        if scatter_direction.near_zero():
            scatter_direction = rec.normal
        return (True, self.albedo, Ray(rec.p, scatter_direction))


class Metal(Material):
    albedo: ClassVar[Color]
    fuzz: ClassVar[float]

    def __init__(self, a: Color, fuzz: float) -> None:
        self.albedo = a
        self.fuzz = fuzz

    def scatter(self, r_in: Ray, rec: HitRecord) -> Tuple[bool, Color, Ray]:
        reflected = Vector.reflect(
            Vector.unit_vector(r_in.direction()), rec.normal)
        scattered = Ray(rec.p, reflected + self.fuzz *
                        Vector.random_in_unit_sphere())
        return (Vector.dot(reflected, rec.normal) > 0, self.albedo, scattered)


class Dielectric(Material):
    ir: ClassVar[float]

    def __init__(self, ir: float) -> None:
        self.ir = ir

    def scatter(self, r_in: Ray, rec: HitRecord) -> Tuple[bool, Color, Ray]:
        attenuation = Color(1.0, 1.0, 1.0)
        if rec.front_face:
            refraction_ratio = 1.0/self.ir
        else:
            refraction_ratio = self.ir

        unit_direction = Vector.unit_vector(r_in.direction())
        cos_theta = min(Vector.dot(-unit_direction, rec.normal), 1.0)
        sin_theta = sqrt(1.0 - cos_theta*cos_theta)

        cannot_refract = refraction_ratio * sin_theta > 1.0
        direction: Vector

        if cannot_refract or self._reflectance(cos_theta, refraction_ratio) > random():
            direction = Vector.reflect(unit_direction, rec.normal)
        else:
            direction = Vector.refract(
                unit_direction, rec.normal, refraction_ratio)

        scattered = Ray(rec.p, direction)
        return (True, attenuation, scattered)

    @staticmethod
    def _reflectance(cosine: float, ref_idx: float):
        # Use Schlick's approximation for reflectance.
        r0 = (1-ref_idx) / (1+ref_idx)
        r0 = r0*r0
        return r0 + (1-r0)*pow((1 - cosine), 5)
