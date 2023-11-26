import argparse
from src.utils import data
from src import detection
import noisereduce as nr
from engine_config import config
import json
import warnings; warnings.filterwarnings('ignore')


parser = argparse.ArgumentParser(description='anomalies detector')
parser.add_argument('filename', type=str)
# parser.add_argument('--threshold', type=float, default=0.4, help='Signal detection threshold')
parser.add_argument('--max_peak_distance_Hz', type=float, default=0.5)
parser.add_argument('--cut_freq_Hz', type=float, default=200, help='Cut all frequencies above the value')
parser.add_argument('--no_noise_reduction', default=False, action='store_true', help='Disable noise reduction from the original signal')
parser.add_argument('--bootstrap_cnt', default=100, type=int, help='Bootstrap windows count')
parser.add_argument('--bootstrap_window_size_seconds', default=2, help='Size of bootstrap windows (in seconds)')
# parser.add_argument('--bootstrap_thresh', default=0.02, help='Threshold for the averaged bootstrap scores')

args = parser.parse_args()

if __name__ == '__main__':
    df = data.read(args.filename)
    
    if args.bootstrap_cnt == 1:
        if not args.no_noise_reduction:
            df.value = nr.reduce_noise(df.value, int(config['f_sampling']))
        yf, freqs = data.time_to_freq_transform(df)

        mask = freqs < args.cut_freq_Hz
        freqs, yf = [x[mask] for x in [freqs, yf]]
        preds = detection.detect(freqs, yf, max_peak_distance_Hz=args.max_peak_distance_Hz)
    else:
        preds = detection.detect_bootstrap(df, bootstrap_cnt=args.bootstrap_cnt,
                                           window_size_seconds=args.bootstrap_window_size_seconds,
                                           max_peak_distance_Hz=args.max_peak_distance_Hz,
                                           sampling_ratio_Hz=config['f_sampling'], reduce_noise=not args.no_noise_reduction,
                                           cut_freq_Hz=args.cut_freq_Hz)
    print(json.dumps(preds))
