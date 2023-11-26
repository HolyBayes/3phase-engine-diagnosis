# This Python file uses the following encoding: latin-1
from .freqs import *
import numpy as np
import scipy as sp
from ..utils import data
from collections import defaultdict
import noisereduce as nr

#ANOMALIES_FREQS = {'дефект клетки ротора': get_type1_freqs, 'эксцентриситет воздушного зазора': get_type2_freqs, 
#            'межвитковые замыкания': get_type3_freqs, 'дефект подшипника (тело качения)': get_type4_1_freqs,
#             'дефект подшипника (внешняя дорожка)': get_type4_2_freqs, 'дефект подшипника (внутренняя дорожка)': get_type4_3_freqs,
#            'другие механические дефекты': get_type5_freqs}


ANOMALIES_FREQS = {'rotor cell defect': get_type1_freqs, 'air gap eccentricity': get_type2_freqs, 
            'inter-cell shortages': get_type3_freqs, 'bearing defect (rotation body)': get_type4_1_freqs,
             'bearing defect (outer track)': get_type4_2_freqs, 'bearing defect (inner track)': get_type4_3_freqs,
            'unknown mechanical defect': get_type5_freqs}



def get_anomaly_score(freqs, signal, anomaly_fn, max_peak_distance_Hz=0.5, thresh=0.0):
    freqs = np.array(freqs)
    anomaly_freqs = anomaly_fn()
    peaks, _ = sp.signal.find_peaks(signal, distance=5, prominence=10)
    prominences = sp.signal.peak_prominences(signal, peaks)[0]
    median_prominence = np.median(prominences)
    locations = []
    scores = []
    anomaly_freqs_ = []
    for f in anomaly_freqs:
        neighbours_indices = [i for i in np.arange(freqs.shape[0]) if abs(freqs[i]-f)<max_peak_distance_Hz]
        neighbouring_peaks = [i for i, p in enumerate(peaks) if p in neighbours_indices]
        if not neighbouring_peaks: continue
        peak = max(neighbouring_peaks, key=lambda x: -prominences[x])
        prominence = prominences[peak]
        locations.append(freqs[peaks[peak]])
        score = -1+2./(1+np.exp(-prominence/median_prominence))
        scores.append(score)
        anomaly_freqs_.append(f)
    scores = np.array(scores)
#     locations = np.array(locations)
    locations = np.array(anomaly_freqs_)
    mask = scores > thresh
    if sum(mask) > 0:
        return locations, np.array(scores)
    return None, None


SINGLE_DETECTION_THRESHOLDS = {
    'inter-cell shortages': 0.07,
    'rotor cell defect': 0.13,
    'unknown mechanical defect': 0.00,
    'bearing defect (rotation body)': 0.0,
    'bearing defect (outer track)': 0.0,
    'bearing defect (inner track)': 0.0,
    'air gap eccentricity': 0.0
}


BOOTSTRAP_THRESHOLDS = {
    'inter-cell shortages': 0.05,
    'rotor cell defect': 0.30,
    'unknown mechanical defect': 0.06,
    'bearing defect (rotation body)': 0.0,
    'bearing defect (outer track)': 0.0,
    'bearing defect (inner track)': 0.0,
    'air gap eccentricity': 0.0
}

def detect(freqs, yf, max_peak_distance_Hz=0.5, thresh_dict=SINGLE_DETECTION_THRESHOLDS):
    res = {anomaly_type: get_anomaly_score(freqs, yf, anomaly_freqs_fn, max_peak_distance_Hz, thresh_dict[anomaly_type]) for anomaly_type, anomaly_freqs_fn in ANOMALIES_FREQS.items()}
    return {k:{'scores': v[1].tolist(), 'locations': v[0].tolist()} for k,v in res.items() if v[0] is not None}

def detect_bootstrap(df, bootstrap_cnt=100, window_size_seconds=2.,
                     max_peak_distance_Hz=0.5,
                     sampling_ratio_Hz=1e4, reduce_noise=False, cut_freq_Hz=200,
                     detection_threshold=SINGLE_DETECTION_THRESHOLDS,
                     bootstrap_thresh=BOOTSTRAP_THRESHOLDS):
    preds = defaultdict(lambda: defaultdict(list))
    for _ in range(bootstrap_cnt):
        df_window = data.get_random_window(df)
        if reduce_noise:
            df_window.value = nr.reduce_noise(df_window.value, int(sampling_ratio_Hz), freq_mask_smooth_hz=cut_freq_Hz)
        yf, freqs = data.time_to_freq_transform(df_window)
        mask = freqs < cut_freq_Hz
        freqs, yf = [x[mask] for x in [freqs, yf]]
        p = detect(freqs, yf, max_peak_distance_Hz=max_peak_distance_Hz, thresh_dict=detection_threshold)
        for anomaly_type in p:
            for loc, score in zip(p[anomaly_type]['locations'], p[anomaly_type]['scores']):
                preds[anomaly_type][loc].append(score)
    res = {}
    for k,v in preds.items():
        scores = []
        locations = []
        uncertainties = []
        for loc, loc_scores in v.items():
            bootstrap_score = sum(loc_scores)/bootstrap_cnt
            if bootstrap_score <= bootstrap_thresh[k]: continue
            locations.append(loc)
            scores.append(bootstrap_score)
            if len(loc_scores) == 1:
                uncertainties.append(0.)
            else:
                uncertainties.append(np.std(loc_scores + [0.]*(bootstrap_cnt-len(loc_scores))))
        if len(scores) == 0: continue
        res[k] = {'scores': scores, 'locations': locations, 'uncertainties': uncertainties}
    return res