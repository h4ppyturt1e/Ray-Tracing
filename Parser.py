from re import sub
from Vector import vec3
from Objects import Setup, Light, Sphere, Color


def parse(fn: str, is_test):
    """
    Parse input file into Setup, Sphere, and Light objects:

    Setup object contains:
    ====================================
    float n - NEAR
    floar l - LEFT
    float r - RIGHT
    float t - TOP
    float b - BOTTOM
    tuple(int, int) res - RESOLUTION
    vec3 background - BACKGROUND COLOR
    vec3 ambient - AMBIENT LIGHT INTENSITY
    str output_fn - OUTPUT FILENAME

    Sphere object contains:
    ====================================
    str name - NAME
    float x, y, z - POSITION
    float sclX, sclY, sclZ - SCALE
    float r, g, b - COLOR
    float Ka, Kd, Ks, Kr - COEFFICIENTS
    int n - SPECULAR EXPONENT

    Light object contains:
    ====================================
    str name - NAME
    float x, y, z - POSITION
    float lr, lg, lb - INTENSITY

    Returns:
    ====================================
    Setup setup - SETUP OBJECT
    lo_spheres - LIST OF SPHERE OBJECTS
    lo_lights - LIST OF LIGHT OBJECTS
    """
    setup = Setup()
    lo_spheres = []
    lo_lights = []

    with open(fn, 'r') as f:
        # gets raw line data, removes \t and \n, and splits
        # by first space into [[tag, data],[tag, data],..[tag, data]]
        raws = f.readlines()
        subbed_raws = [sub(r'\t', ' ', raw) for raw in raws]
        cleaned_raws = [line.strip().split(" ", 1) for line in subbed_raws]

        # for each line, check tag and assign data to appropriate dict
    for line in cleaned_raws:
        cur_tag = line[0]
        if len(line) > 1:
            cur_data = line[1]

        if cur_tag == "NEAR":
            setup.n = float(cur_data)

        elif cur_tag == "LEFT":
            setup.l = float(cur_data)

        elif cur_tag == "RIGHT":
            setup.r = float(cur_data)

        elif cur_tag == "TOP":
            setup.t = float(cur_data)

        elif cur_tag == "BOTTOM":
            setup.b = float(cur_data)

        elif cur_tag == "RES":
            setup.res = tuple([int(x) for x in cur_data.split()])

        elif cur_tag == "SPHERE":
            cur_sphere = {}
            split_data = cur_data.split()
            name = split_data[0]
            position = [float(x) for x in split_data[1:4]]
            position = vec3(position[0], position[1], position[2])
            scale = [float(x) for x in split_data[4:7]]
            scale = vec3(scale[0], scale[1], scale[2])
            color = [float(x) for x in split_data[7:10]]
            color = Color(color[0], color[1], color[2])
            Ka, Kd, Ks, Kr = [float(x) for x in split_data[10:14]]
            n = int(split_data[14])

            cur_sphere = Sphere(name, position, scale,
                                color, Ka, Kd, Ks, Kr, n)
            lo_spheres.append(cur_sphere)

        elif cur_tag == "LIGHT":
            cur_light = {}
            split_data = cur_data.split()
            name = split_data[0]
            position = [float(x) for x in split_data[1:4]]
            position = vec3(position[0], position[1], position[2])
            intensity = [float(x) for x in split_data[4:7]]
            intensity = Color(intensity[0], intensity[1], intensity[2])

            cur_light = Light(name, position, intensity)
            lo_lights.append(cur_light)

        elif cur_tag == "BACK":
            bg = [float(x) for x in cur_data.split()]
            bg = Color(bg[0], bg[1], bg[2])
            setup.background = bg

        elif cur_tag == "AMBIENT":
            amb = [float(x) for x in cur_data.split()]
            amb = Color(amb[0], amb[1], amb[2])
            setup.ambient = amb

        elif cur_tag == "OUTPUT":
            setup.output_fn = cur_data

    # for testing
    if not is_test:
        print_dicts(setup, lo_spheres, lo_lights)

    return setup, lo_spheres, lo_lights


def print_dicts(setup, lo_spheres, lo_lights):
    """ Print Setup, Sphere, and Light objects for testing """
    print(f"{setup}\n")
    for sphere in lo_spheres:
        print(f"{sphere}\n")
    for light in lo_lights:
        print(f"{light}\n")
