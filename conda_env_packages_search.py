import subprocess
import argparse
from multiprocessing import Pool
from itertools import repeat
import time
import tqdm as tqd
from tqdm import tqdm
import platform


def get_conda_envs():
    cmd = 'conda env list'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = p.stdout.readlines()
    envs = []
    for line in lines:
        line = line.decode('utf-8')
        if line.startswith('#'):
            continue
        line = line.strip()
        if line == '':
            continue
        envs.append(line.split()[0])
    return envs
#
def check_env_pckg(env, package):
    cmd = 'conda list -n {} | {} {}'.format(env, 'findstr' if platform.system() == 'Windows' else 'grep' ,package)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = p.stdout.readlines()
    if len(lines) > 0:
        return env
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.description = 'Check what conda environment/s having the combination of the passed packages'
    parser.add_argument('--packages', nargs='+', help='Package names to check')
    parser.add_argument('--multiprocess', action='store_true', help='Whether to multiprocess')
    parser.add_argument('--cores', type=int, default=4, help='Number of cores to use')
    parser.add_argument('--progress', action='store_false', help='Whether to show progress bar, Turned off by default')
    args = parser.parse_args()
    packages = args.packages
    time1 = time.time()
    print('Checking the following packages: {}'.format(packages))
    envs = get_conda_envs()
    print('Found the following conda environments: {}'.format(envs))
    envs_with_package = {}
    if args.multiprocess:
        print('Using multiprocess with {} cores'.format(args.cores))
        pool = Pool(processes=args.cores)
        for package in tqdm(packages, desc='Checking packages', disable=args.progress):
            envs_with_package[package] = pool.starmap(check_env_pckg, tqdm(zip(envs, repeat(package)), total=len(envs), desc='Checking {}'.format(package), disable=args.progress))
        pool.close()
        pool.join()
    else:
        for package in tqdm(packages, desc='Checking packages', disable=args.progress):
            envs_with_package[package] = []
            for env in tqdm(envs, desc='Checking environments for package {}'.format(package), disable=args.progress):
                envs_with_package[package].append(check_env_pckg(env, package))
    for package in packages:
        envs_with_package[package] = [x for x in envs_with_package[package] if x is not None]
    print('Results per package: {}'.format(envs_with_package))
    # Now merge and return condas with all packages
    envs_with_all_packages = []
    for env in envs:
        found = True
        for package in packages:
            if env not in envs_with_package[package]:
                found = False
                break
        if found:
            envs_with_all_packages.append(env)
    print('\n\n\nFound the following conda environments containing all packages:\n\t{}'.format(envs_with_all_packages))
    print("Time taken: {:4f} sec".format(time.time() - time1))

if __name__ == '__main__':
    main()
