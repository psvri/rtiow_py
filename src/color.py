from math import sqrt
from config import Color
from utils import clamp


def write_color(pixel_color: Color, samples_per_pixel: int):
    r = pixel_color.x()
    g = pixel_color.y()
    b = pixel_color.z()

    scale = 1.0 / samples_per_pixel
    r = sqrt(scale * r)
    g = sqrt(scale * g)
    b = sqrt(scale * b)

    ir = int(256 * clamp(r, 0, 0.999))
    ig = int(256 * clamp(g, 0, 0.999))
    ib = int(256 * clamp(b, 0, 0.999))

    print(str(ir) + ' ' + str(ig) + ' ' + str(ib))
