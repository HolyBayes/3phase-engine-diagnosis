# This Python file uses the following encoding: latin-1
import os, sys; sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from engine_config import config
import math

def get_type1_freqs(config=config, n_range=range(1,4)):
    #  частоты для дефекта клетки ротора. n_range - диапазон гармоник
    s = config['s']
    f1 = config['f1']
    freqs = []
    for n in n_range:
        assert n > 0
        assert isinstance(n, int)
        freqs.append((1+2*n*s)*f1)
        freqs.append((1-2*n*s)*f1)
    return freqs
        

def get_type2_freqs(config=config, n_range=range(1,4)):
    #  частоты для эксцентриситета воздушного зазора. n_range - диапазон гармоник
    R_s = config['R_s']
    p = config['p']
    s = config['s']
    f1 = config['f1']
    freqs = []
    for n in n_range:
        assert n > 0
        assert isinstance(n, int)
        freqs.append(f1*((R_s*(1-s)/p)+n+((1-s)/p)))
        freqs.append(f1*((R_s*(1-s)/p)+n-((1-s)/p)))
        freqs.append(f1*((R_s*(1-s)/p)-n+((1-s)/p)))
        freqs.append(f1*((R_s*(1-s)/p)-n-((1-s)/p)))
    return freqs
    
def get_type3_freqs(config=config, n_range=range(1,4), k_range=range(1,4)):
    # функция расчёта гармоник для межвитковых замыканий. n_range и k_range - диапазон для гармоник 
    f1 = config['f1']
    p = config['p']
    s = config['s']
    freqs = []
    for n in n_range:
        assert n > 0
        assert isinstance(n, int)
        for k in k_range:
            assert k > 0
            assert isinstance(k, int)
            freqs.append(f1*((n*(1-s)/p)+k))
            freqs.append(f1*((n*(1-s)/p)-k))
    return freqs

def get_type4_1_freqs(config=config):
    # функция расчёта гармоник для дефектов подшипника (тело качения)
    D_pit = config['D_pit']
    D_ball = config['D_ball']
    f_r = config['beta']
    beta = config['beta']
    return [(D_pit/D_ball)*f_r*(1-(D_ball/(D_pit*math.cos(beta)))**2)]
    
def get_type4_2_freqs(config=config):
    # функция расчёта гармоник для дефектов подшипника (внешняя дорожка)
    n = config['n']
    D_pit = config['D_pit']
    D_ball = config['D_ball']
    f_r = config['beta']
    beta = config['beta']
    return [(n/2)*f_r*(1-(D_ball/(D_pit*math.cos(beta))))]

def get_type4_3_freqs(config=config):
    # функция расчёта гармоник для дефектов подшипника (внутренняя дорожка)
    n = config['n']
    D_pit = config['D_pit']
    D_ball = config['D_ball']
    f_r = config['beta']
    beta = config['beta']
    return [(n/2)*f_r*(1+(D_ball/(D_pit*math.cos(beta))))]


def get_type5_freqs(config=config, n_range=range(1,4)):
    # функция расчёта гармоник для других механических поломок. n_range - диапазон для гармоник 
    f_r = config['f_r']
    f1 = config['f1']
    freqs = []
    for n in n_range:
        assert n > 0
        assert isinstance(n, int)
        freqs.append(f1 + n*f_r)
    return freqs
