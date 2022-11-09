from typing import List, Tuple
from hittable import HitRecord, Hittable
from ray import Ray


class HittableList(Hittable):
    objects: List[Hittable]

    def __init__(self) -> None:
        self.objects = []

    def clear(self):
        self.objects.clear()

    def add(self, new_object: Hittable):
        self.objects.append(new_object)

    def hit(self, r: Ray, t_min: float, t_max: float) -> Tuple[bool, HitRecord]:
        out_rec = HitRecord()
        hit_anything = False
        closest_so_far = t_max

        for scene_object in self.objects:
            did_hit, temp_rec = scene_object.hit(r, t_min, closest_so_far)
            if did_hit:
                hit_anything = True
                closest_so_far = temp_rec.t
                out_rec = temp_rec

        return (hit_anything, out_rec)
