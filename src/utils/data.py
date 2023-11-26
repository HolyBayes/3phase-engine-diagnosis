import numpy as np
import pandas as pd
import os, sys; sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from engine_config import config

def read(filename):
    df = pd.read_csv(filename, skiprows=17, sep=';', encoding='latin-1', header=None, names=['time', 'value'])
    return df

def time_to_freq_transform(df, config=config, db=True):
    """
    @param df: pd.DataFrame - spectrum data
    @param config: dict - engine config
    @param db: bool - convert to decibel scale if True
    @param reduce_noise: bool - reduce noise if True
    """
    f_sampling = config['f_sampling']
    y = df['value']
    n = len(y)
    yf = np.fft.rfft(y)
    fstep = f_sampling / n
    freqs = np.arange(len(yf)) * fstep
    if db:
        yf = 20*np.log10(np.abs(yf))
    return yf, freqs

def get_random_window(df, window_size_seconds=2., sampling_ratio_Hz=1e4):
    start_seconds = df[df.time < df.time.max()-window_size_seconds].time
    start_seconds = np.random.choice(start_seconds.values)
    window_size = int(window_size_seconds*sampling_ratio_Hz)
    window_df = df[start_seconds<=df.time].reset_index(drop=True)[:window_size].copy()
    window_df.time -= start_seconds
    return window_df