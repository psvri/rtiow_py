from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from ast import Tuple
from config import Vector, Point
from ray import Ray

if TYPE_CHECKING:
    from material import Material


class HitRecord:
    p: Point
    normal: Vector
    t: float
    front_face: bool
    mat: Material

    def set_face_normal(self, r: Ray, outward_normal: Vector):
        self.front_face = Vector.dot(r.direction(), outward_normal) < 0
        if self.front_face:
            self.normal = outward_normal
        else:
            self.normal = -outward_normal

    def from_hit_record(self, rec: 'HitRecord'):
        self.p = rec.p
        self.normal = rec.normal
        self.t = rec.t
        self.front_face = rec.front_face
        self.mat = rec.mat


class Hittable(ABC):

    @abstractmethod
    def hit(self, r: Ray, t_min: float, t_max: float) -> Tuple[bool, HitRecord]:
        pass
