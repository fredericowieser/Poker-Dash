import numpy as np


def color_red_green_nums(val):
    if type(val) in (str, float):
        color = ""
        try:
            val = float(val)
            if val < 0:
                color = "red"
            elif val > 0:
                color = "green"
            return "background-color: %s" % color
        except:
            return "background-color: %s" % color


def avg_gbp_in_per_cap(data: np.ndarray) -> float:
    pass


def avg_net_n_buyins(data: np.ndarray) -> float:
    pass


def avg_net(data: np.ndarray) -> float:
    pass


def encode_str_2_rgb(s):
    """Encodes any string to an RGB value where the elements of the
    RGB set are floats from 0 to 1."""
    s_as_bytes = str.encode(str(s))

    s_float = hash(s_as_bytes) % 100 / 100

    if s_float < (1 / 3):
        r = (hash(29 * s_as_bytes) % 256) / (256 * 2) + 0.1
        g = (hash(23 * s_as_bytes) % 256) / (256 * 5) + 0.65
        b = (hash(5 * s_as_bytes) % 256) / (256 * 2) + 0.3
        return (r, g, b)
    if s_float < (2 / 3):
        r = (hash(2 * s_as_bytes) % 256) / (256 * 2) + 0.3
        g = (hash(17 * s_as_bytes) % 256) / (256 * 2) + 0.1
        b = (hash(7 * s_as_bytes) % 256) / (256 * 5) + 0.65
        return (r, g, b)
    if s_float < 1:
        r = (hash(5 * s_as_bytes) % 256) / (256 * 5) + 0.65
        g = (hash(11 * s_as_bytes) % 256) / (256 * 2) + 0.3
        b = (hash(13 * s_as_bytes) % 256) / (256 * 2) + 0.1
        return (r, g, b)
