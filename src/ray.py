from config import Point, Vector


class Ray:
    orig: Point
    dir: Vector

    def __init__(self, origin: Point = None, direction: Vector = None) -> None:
        if origin is not None:
            self.orig = origin
        else:
            self.orig = Point()
        if direction is not None:
            self.dir = direction
        else:
            self.dir = Vector()

    def at(self, t: float) -> Vector:
        return self.orig + self.dir * t

    def origin(self) -> Point:
        return self.orig

    def direction(self) -> Vector:
        return self.dir
