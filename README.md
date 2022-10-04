# random-utilities

This repo contains some random utilities than uses built in python3.x packages only - no external libraries are needed.

## Listing Environments Containing Set of Packages: 

[conda_env_packages_search.py](https://github.com/mohamadmansourX/random-utilities/blob/main/conda_env_packages_search.py)

```
usage: conda_env_packages_search.py [-h] [--packages PACKAGES [PACKAGES ...]] [--multiprocess] [--cores CORES] [--progress]

Check what conda environment/s having the combination of the passed packages

optional arguments:
  -h, --help            show this help message and exit
  --packages PACKAGES [PACKAGES ...]
                        Package names to check
  --multiprocess        Whether to multiprocess
  --cores CORES         Number of cores to use
  --progress            Whether to show progress bar, Turned off by default
```

### E.g. Usage:

```
$ python conda_env_packages_search.py --packages cv2 onnxruntime --multiprocess --cores 4
```

Output:
```
Checking the following packages: ['cv2', 'onnxruntime']
Found the following conda environments: ['env1', 'env2', 'env3', 'en4', 'env6']

Found the following conda environments containing all packages:
        ['env1', 'env4']
Time taken: 14.339622 sec
```
