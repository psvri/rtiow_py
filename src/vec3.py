from typing import List, Union
from math import sqrt
from random import random, uniform


class Vec3:
    e: List[float]

    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        self.e = [x, y, z]

    def x(self) -> float:
        return self.e[0]

    def y(self) -> float:
        return self.e[1]

    def z(self) -> float:
        return self.e[2]

    def __neg__(self) -> 'Vec3':
        return Vec3(-self.e[0], -self.e[1], -self.e[2])

    def __str__(self) -> str:
        return str(self.e)

    def __getitem__(self, key) -> float:
        return self.e[key]

    def __iadd__(self, other: 'Vec3') -> 'Vec3':
        self.e[0] += other.e[0]
        self.e[1] += other.e[1]
        self.e[2] += other.e[2]
        return self

    def __itruediv__(self, other: float) -> 'Vec3':
        return self.__imul__(1/other)

    def __imul__(self, other: float) -> 'Vec3':
        self.e[0] *= other
        self.e[1] *= other
        self.e[2] *= other
        return self

    def length(self) -> float:
        return sqrt(self.length_squared())

    def length_squared(self) -> float:
        return self.e[0] * self.e[0] + self.e[1] * self.e[1] + self.e[2] * self.e[2]

    def __add__(self, other: 'Vec3') -> 'Vec3':
        return Vec3(self.e[0] + other.e[0], self.e[1] + other.e[1], self.e[2] + other.e[2])

    def __sub__(self, other: 'Vec3') -> 'Vec3':
        return Vec3(self.e[0] - other.e[0], self.e[1] - other.e[1], self.e[2] - other.e[2])

    def __mul__(self, other: Union['Vec3', float]) -> 'Vec3':
        if isinstance(other, float):
            return Vec3(self.e[0] * other, self.e[1] * other, self.e[2] * other)
        return Vec3(self.e[0] * other.e[0], self.e[1] * other.e[1], self.e[2] * other.e[2])

    def __rmul__(self, other) -> 'Vec3':
        return self.__mul__(other)

    def __truediv__(self, other: float) -> 'Vec3':
        return self.__mul__(1 / other)

    def near_zero(self) -> bool:
        s = 1e-8
        return (abs(self.e[0]) < s) and (abs(self.e[1]) < s) and (abs(self.e[2]) < s)

    @staticmethod
    def dot(u: 'Vec3', v: 'Vec3') -> float:
        return u.e[0] * v.e[0] + u.e[1] * v.e[1] + u.e[2] * v.e[2]

    @staticmethod
    def cross(u: 'Vec3', v: 'Vec3') -> 'Vec3':
        return Vec3(u.e[1] * v.e[2] - u.e[2] * v.e[1],
                    u.e[2] * v.e[0] - u.e[0] * v.e[2],
                    u.e[0] * v.e[1] - u.e[1] * v.e[0])

    @staticmethod
    def unit_vector(v: 'Vec3') -> 'Vec3':
        return v / v.length()

    @staticmethod
    def random_vec() -> 'Vec3':
        return Vec3(random(), random(), random())

    @staticmethod
    def random_vec_bn(min_val: float, max_val: float) -> 'Vec3':
        return Vec3(uniform(min_val, max_val), uniform(min_val, max_val), uniform(min_val, max_val))

    @staticmethod
    def random_in_unit_sphere() -> 'Vec3':
        while True:
            p = Vec3.random_vec_bn(-1.0, 1.0)
            if p.length_squared() >= 1:
                continue
            return p

    @staticmethod
    def random_unit_vector() -> 'Vec3':
        return Vec3.unit_vector(Vec3.random_in_unit_sphere())

    @staticmethod
    def reflect(v: 'Vec3', n: 'Vec3') -> 'Vec3':
        return v - 2*Vec3.dot(v, n)*n

    @staticmethod
    def refract(uv: 'Vec3', n: 'Vec3', etai_over_etat: float) -> 'Vec3':
        cos_theta = min(Vec3.dot(-uv, n), 1.0)
        r_out_perp = etai_over_etat * (uv + cos_theta*n)
        r_out_parallel = -sqrt(abs(1.0 - r_out_perp.length_squared())) * n
        return r_out_perp + r_out_parallel

    @staticmethod
    def random_in_unit_disk() -> 'Vec3':
        while True:
            p = Vec3(uniform(-1, 1), uniform(-1, 1), 0)
            if p.length_squared() >= 1:
                continue
            return p


if __name__ == '__main__':
    vec = Vec3(1, 2, 3)
    print(-vec)
    print(vec * vec)
    print(vec + vec)
    print(vec * 3.0)
    print(vec/2)

    vec += vec
    print(vec)
    print()

    for i in range(10):
        print(Vec3.random_in_unit_sphere())
