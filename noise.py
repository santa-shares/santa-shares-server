# Borrowed from pip/p5 as can't pip install wsgl library where deployed.
import math, random
from math import ceil, floor, exp, log, sqrt
from math import degrees, radians
from math import sin, cos, tan
from math import asin, acos, atan, atan2

SINCOS_PRECISION = 0.5
SINCOS_LENGTH = int(360 / SINCOS_PRECISION)
PRE_COS = [ cos(radians(d) * SINCOS_PRECISION) for d in range(SINCOS_LENGTH) ]

PERLIN_OCTAVES = 4
PERLIN_FALLOFF = 0.5
PERLIN_YWRAPB = 4
PERLIN_YWRAP = 1 << PERLIN_YWRAPB
PERLIN_ZWRAPB = 8
PERLIN_ZWRAP = 1 << PERLIN_ZWRAPB
PERLIN_SIZE = 4095
PERLIN_COS_TABLE = PRE_COS
PERLIN_TWO_PI = SINCOS_LENGTH
PERLIN_PI = PERLIN_TWO_PI
PERLIN_PI >>= 1
PERLIN = None

def noise(x, y=0, z=0):

    global PERLIN

    def noise_fsc(i):
        return 0.5 * (1 - PERLIN_COS_TABLE[int(i * PERLIN_PI) % PERLIN_TWO_PI])

    if PERLIN is None:
        PERLIN = [random.random() for _ in range(PERLIN_SIZE + 1)]

    x = (-1 * x) if x < 0 else x
    xi = int(x)
    xf = x - xi

    y = (-1 * y) if y < 0 else y
    yi = int(y)
    yf = y - yi

    z = (-1 * z) if z < 0 else z
    zi = int(z)
    zf = z - zi

    r = 0
    ampl = 0.5

    for i in range(PERLIN_OCTAVES):
        rxf = noise_fsc(xf)
        ryf = noise_fsc(yf)

        of = int(xi + (yi << PERLIN_YWRAPB) + (zi << PERLIN_ZWRAPB))
        n1 = PERLIN[of % PERLIN_SIZE]
        n1 += rxf * (PERLIN[(of + 1) % PERLIN_SIZE] - n1)
        n2 = PERLIN[(of + PERLIN_YWRAP) % PERLIN_SIZE]
        n2 += rxf * (PERLIN[(of + PERLIN_YWRAP + 1) & PERLIN_SIZE] - n2)
        n1 += ryf * (n2 - n1)

        of += PERLIN_ZWRAP
        n2 = PERLIN[of & PERLIN_SIZE]
        n2 += rxf * (PERLIN[(of + 1) % PERLIN_SIZE] - n2)
        n3 = PERLIN[(of + PERLIN_YWRAP) % PERLIN_SIZE]
        n3 += rxf * (PERLIN[(of + PERLIN_YWRAP + 1) % PERLIN_SIZE] - n3)

        n2 += ryf * (n3 - n2)
        n1 += noise_fsc(zf) * (n2 - n1)

        r += n1 * ampl
        ampl *= PERLIN_FALLOFF

        xi *= 2
        xf *= 2

        yi *= 2
        yf *= 2

        zi *= 2
        zf *= 2

        if xf >= 1:
            xi = xi + 1
            xf = xf - 1

        if yf >= 1:
            yi = yi + 1
            yf = yf - 1

        if zf >= 1:
            zi = zi + 1
            zf = zf - 1

    return r

def noise_seed(seed):
    global PERLIN
    random_seed(seed)
    PERLIN = None

def random_uniform(high=1, low=0):
    return random.uniform(low, high)

def random_gaussian(mean=0, std_dev=1):
    return random.gauss(mean, std_dev)

def random_seed(seed):
    random.seed(seed)