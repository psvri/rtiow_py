from math import inf, sqrt
import multiprocessing as mp
from random import random, uniform
import sys
from material import Lambertian, Dielectric, Material, Metal
from config import Point, Color, Vector
from ray import Ray
from sphere import Sphere
from hittable_list import HittableList
from camera import Camera
from color import write_color


# Image
ASPECT_RATION = 16.0 / 9.0
IMAGE_WIDTH = 428
IMAGE_HEIGHT = int(IMAGE_WIDTH / ASPECT_RATION)
SAMPLES_PER_PIXEL = 100
MAX_DEPTH = 50


class Scene:

    @staticmethod
    def generate_image():

        world_init: HittableList = Scene.random_scene()

        # Camera
        lookfrom = Vector(13, 2, 3)
        lookat = Vector(0, 0, 0)
        vup = Vector(0, 1, 0)
        dist_to_focus = 10.0
        aperture = 0.1

        cam_init = Camera(lookfrom, lookat, vup, 20,
                          ASPECT_RATION, aperture, dist_to_focus)

        print("P3\n" + str(IMAGE_WIDTH) + ' ' + str(IMAGE_HEIGHT) + "\n255")

        count = 0
        for j in range(IMAGE_HEIGHT-1, -1, -1):
            for i in range(0, IMAGE_WIDTH):
                pixel_color = Color()
                for _ in range(0, SAMPLES_PER_PIXEL):
                    u = (i + random()) / (IMAGE_WIDTH-1)
                    v = (j + random()) / (IMAGE_HEIGHT-1)
                    r = cam_init.get_ray(u, v)
                    pixel_color += Scene.ray_color(r, world_init, MAX_DEPTH)

                write_color(pixel_color, SAMPLES_PER_PIXEL)
                count += 1
                print(f"""completed {count}/{IMAGE_WIDTH * IMAGE_HEIGHT}""",
                      file=sys.stderr, end='\r')

    @staticmethod
    def generate_image_mp():

        world_init: HittableList = Scene.random_scene()

        # Camera
        lookfrom = Vector(13, 2, 3)
        lookat = Vector(0, 0, 0)
        vup = Vector(0, 1, 0)
        dist_to_focus = 10.0
        aperture = 0.1

        cam_init = Camera(lookfrom, lookat, vup, 20,
                          ASPECT_RATION, aperture, dist_to_focus)

        items = []
        for j in range(IMAGE_HEIGHT-1, -1, -1):
            for i in range(0, IMAGE_WIDTH):
                items.append((i, j))

        pool = mp.Pool(mp.cpu_count(), initializer=Scene.init_pool,
                       initargs=(world_init, cam_init))
        result = pool.starmap(Scene.compute_color, items)
        pool.close()
        pool.join()

        for color in result:
            write_color(color, SAMPLES_PER_PIXEL)

    @staticmethod
    def ray_color(r: Ray, world: HittableList, depth: int) -> Color:
        if depth <= 0:
            return Color()

        is_hit, rec = world.hit(r, 0.001, inf)
        if is_hit:
            is_scattered, attenuation, scattered = rec.mat.scatter(
                r, rec)

            if is_scattered:
                return attenuation * Scene.ray_color(scattered, world, depth-1)
            return Color(0, 0, 0)

        unit_direction = Vector.unit_vector(r.direction())
        t = 0.5*(unit_direction.y() + 1.0)
        return (1.0-t)*Color(1.0, 1.0, 1.0) + t*Color(0.5, 0.7, 1.0)

    @staticmethod
    def hit_sphere(center: Point, radius: float, r: Ray) -> float:
        oc = r.origin() - center
        a = r.direction().length_squared()
        half_b = Vector.dot(oc, r.direction())
        c = oc.length_squared() - radius*radius
        discriminant = half_b*half_b - a*c
        if discriminant < 0:
            return -1.0
        else:
            return (-half_b - sqrt(discriminant)) / a

    @staticmethod
    def random_scene() -> HittableList:
        world: HittableList = HittableList()

        ground_material = Lambertian(Color(0.5, 0.5, 0.5))
        world.add(Sphere(ground_material, Point(0, -1000, 0), 1000))

        for a in range(-11, 11, 1):
            for b in range(-11, 11, 1):
                choose_mat = random()
                center = Point(a + 0.9*random(), 0.2, b + 0.9*random())

                if (center - Point(4, 0.2, 0)).length() > 0.9:
                    sphere_material: Material

                    if choose_mat < 0.8:
                        # diffuse
                        albedo = Color.random_vec() * Color.random_vec()
                        sphere_material = Lambertian(albedo)
                        world.add(Sphere(sphere_material, center, 0.2))
                    elif choose_mat < 0.95:
                        # metal
                        albedo = Color.random_vec_bn(0.5, 1)
                        fuzz = uniform(0, 0.5)
                        sphere_material = Metal(albedo, fuzz)
                        world.add(Sphere(sphere_material, center, 0.2))
                    else:
                        # glass
                        sphere_material = Dielectric(1.5)
                        world.add(Sphere(sphere_material, center, 0.2))

        material1 = Dielectric(1.5)
        world.add(Sphere(material1, Point(0, 1, 0), 1.0))

        material2 = Lambertian(Color(0.4, 0.2, 0.1))
        world.add(Sphere(material2, Point(-4, 1, 0), 1.0))

        material3 = Metal(Color(0.7, 0.6, 0.5), 0.0)
        world.add(Sphere(material3, Point(4, 1, 0), 1.0))

        return world

    @staticmethod
    def compute_color(i: int, j: int) -> Color:
        global SAMPLES_PER_PIXEL, IMAGE_HEIGHT, IMAGE_WIDTH, world, cam
        pixel_color = Color()
        for _ in range(0, SAMPLES_PER_PIXEL):
            u = (i + random()) / (IMAGE_WIDTH-1)
            v = (j + random()) / (IMAGE_HEIGHT-1)
            r = cam.get_ray(u, v)
            pixel_color += Scene.ray_color(r, world, MAX_DEPTH)

        return pixel_color

    @staticmethod
    def init_pool(world_init, cam_init):
        global world, cam
        world = world_init
        cam = cam_init
