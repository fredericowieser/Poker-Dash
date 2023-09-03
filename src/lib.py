import numpy as np

def color_red_green_nums(val):
    if type(val) in (str, float):
        color = ''
        try:
            val = float(val)
            if val < 0: color = 'red'
            elif val > 0: color = 'green'
            return 'background-color: %s' % color
        except:
            return 'background-color: %s' % color

def avg_gbp_in_per_cap(data : np.ndarray) -> float:
    pass

def avg_net_n_buyins(data : np.ndarray) -> float:
    pass

def avg_net(data : np.ndarray) -> float:
    pass

