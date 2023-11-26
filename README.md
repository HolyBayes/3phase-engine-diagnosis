# 3phase engines break detection

Repository for engine defects detection.

## Requirements

Python >= 3.9

## Setup

```
poetry install
```

To pull all the repository datasets, use the following command:

```
git lfs fetch --all
```

## Usage

```
poetry run python detect.py <signal filename>
```

You can also save the output in json file via the following command
```
poetry run python detect.py <signal filename> > result.json
```


For more info, run
```
poetry run python detect.py --help
```

## Example

The command
```
poetry run python detect.py data/нагрузка\ 100%\ 11\ 01.txt
```

produces an output in json-format
```
{"rotor cell defect": {"scores": [0.35177167740754056, 0.33521470300756806, 0.464201297403968, 0.33230831612342415, 0.3264957937907862, 0.31774803194720835], "locations": [52.55, 47.13333333333333, 55.78333333333333, 44.516666666666666, 57.916666666666664, 41.53333333333333]}, "inter-cell shortages": {"scores": [0.30344309046487417, 0.4467664540094092, 0.33964129710472224, 0.3580142145413754, 0.33894041987943724, 0.3398648253315826, 0.3062831037892264, 0.3453817916716988, 0.377776663645762], "locations": [73.91666666666667, 123.86666666666666, 174.18333333333334, 98.21666666666667, 148.86666666666667, 199.06666666666666, 123.05, 22.983333333333334, 173.31666666666666]}}

```

