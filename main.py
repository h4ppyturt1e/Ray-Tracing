"""
Written in Python 3.9.7 64-bit
By Ryan N. Permana (2022)
"""

import sys
import os
import numpy as np
from timeit import default_timer as timer

from Parser import parse
from Vector import vec3
from RayTracer import RayTracer
from Objects import Ray
from ppm import save_imageP3 as to_ppm

""" Global variables """

CAM_POS = vec3(0.0, 0.0, 0.0)


def main(input_file: str, is_test: bool = False):
    # parse input file
    setup, SPHERES, LIGHTS = parse(input_file, is_test)

    RT = RayTracer(setup, SPHERES, LIGHTS)
    WIDTH, HEIGHT = setup.res[0], setup.res[1]

    PIXELS = np.zeros((WIDTH, HEIGHT, 3))
    FOV = 126

    # compute aspect ratio
    ASPECT_RATIO = WIDTH / HEIGHT

    PLANE_HEIGHT = setup.t * np.tan(np.radians(FOV / 2))
    PLANE_WIDTH = PLANE_HEIGHT * ASPECT_RATIO

    # compute pixel size
    pixel_height = PLANE_HEIGHT / HEIGHT
    pixel_width = PLANE_WIDTH / WIDTH

    # compute half width and half height
    half_height = PLANE_HEIGHT / 2
    half_width = PLANE_WIDTH / 2

    for y in range(HEIGHT):
        for x in range(WIDTH):
            # compute pixel center coordinates
            x_coord = (x + 0.5) * pixel_width - half_width
            y_coord = (y + 0.5) * pixel_height - half_height

            # create ray origin and direction
            ray_origin = CAM_POS
            ray_direction = vec3(x_coord, y_coord, -1).normalize()

            # create ray
            ray = Ray(ray_origin, ray_direction)

            # trace ray
            color = RT.trace(ray, 0)

            # print(f"Pixel ({y}, {x})")
            PIXELS[-y, x] = color.to_255()

    to_ppm(setup.res[0], setup.res[1], setup.output_fn, PIXELS)

    print(f"The output file is \"{setup.output_fn}\".")


def tester():
    """ Test all files in the tests folder. """
    total_times = []
    lo_tests = [f for f in os.listdir("tests") if f.endswith(".txt")]

    for test in lo_tests:
        start = timer()
        main("tests/" + test, True)
        end = timer()
        runtime = end - start
        total_times.append((runtime, test))
        print(f"Runtime: {runtime:.5f} seconds.\n")

    avg_time = sum([t[0] for t in total_times]) / len(total_times)
    slowest = max(total_times, key=lambda x: x[0])
    fastest = min(total_times, key=lambda x: x[0])

    print(f"Average runtime: {avg_time:.2f} seconds.")
    print(f"Slowest runtime: {slowest[0]:.2f} seconds ({slowest[1]}).")
    print(f"Fastest runtime: {fastest[0]:.2f} seconds ({fastest[1]}).")
    print(f"Total runtime: {sum([t[0] for t in total_times]):.2f} seconds.")


if __name__ == '__main__':
    arg = str((sys.argv)[1])

    if arg == "TEST":
        tester()
    else:
        input_file = arg
        start = timer()
        main(input_file)
        end = timer()
        runtime = end - start
        print(f"Total runtime: {runtime:.2f} seconds.")
