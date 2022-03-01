#!/usr/bin/env python

import argparse
import subprocess
import sys
from datetime import datetime

""" Version """
version = '2.0'

""" Variables """
trivy_bin = 'trivy'
docker_bin = 'docker'
platform = '--platform=linux/amd64'

""" Logs """
now = datetime.now().strftime("%Y%m%d%H%M%S")
logfile = 'evidence_'+now+'.log'

""" Styles """
class style():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

""" Arguments """
parser = argparse.ArgumentParser(description='bsimage - build & scan image tool', prog='bsimage')
parser.add_argument('image', help='Image name for build and/or scan')
parser.add_argument('--dockerfile', '-d', help='If specified, start a build before performing the scan')
parser.add_argument('--only-os', '-o', action='store_true', help='Only vuln checks of the OS layer')
parser.add_argument('--version', '-v', action='version', version=f'%(prog)s {version}')
args = parser.parse_args()

def check_program(name):
    status, response = subprocess.getstatusoutput(f'which {name}')
    return status

def check_pre_reqs():
    trivy_installed = check_program(trivy_bin)
    if trivy_installed == 1:
        print(f'{style.WARNING}(*) Trivy is a prerequisite and is not installed. Go to https://aquasecurity.github.io/trivy and install it.{style.ENDC}')
    docker_installed = check_program(docker_bin)
    if docker_installed == 1:
        print(f'{style.WARNING}(*) Docker is a prerequisite and is not installed. Go to https://docs.docker.com/get-docker/ and install it.{style.ENDC}')
    if trivy_installed or docker_installed:
        print(f'\n{style.FAIL}(*) You cannot continue. The prerequisites have not been met.\n(*) Please install them and try again.\n{style.ENDC}')
        sys.exit(1)
    return True

def check_image_exists(name):
    print(f'{style.OKCYAN}(*) Checking if image {style.BOLD}{style.UNDERLINE}{name}{style.ENDC}{style.OKCYAN} exists...{style.ENDC}')
    check_image_command = ['docker', 'image', 'inspect']
    check_image_command.append(name)
    check_image_run = subprocess.run(check_image_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check_image_run.returncode == 1:
        print(f'{style.FAIL}(*) The image does not exist. Please download it to continue.\n{style.ENDC}')
        sys.exit(126)

if args.dockerfile:
    print(f'{style.OKCYAN}bsimage {version}\n(*) Starting the build...{style.ENDC}\n')
    build_command = ['docker', 'build', '-t', args.image, '-f', args.dockerfile, '.', platform]
    build_run = subprocess.run(build_command)
    if build_run.returncode == 1:
        print(f'{style.FAIL}\n(*) A problem occurred while the image was being built.{style.ENDC}')
        sys.exit(1)

check_pre_reqs()

check_image_exists(args.image)

trivy_command = ['trivy', 'image', '--exit-code', '1', '--format', 'table', '--output', logfile]
trivy_command.append(args.image)
trivy_run = subprocess.run(trivy_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if trivy_run.returncode == 1:
    print(f'{style.FAIL}(*) Image not approved. Please check the logs for more details. See {style.BOLD}{style.UNDERLINE}{logfile}{style.ENDC}{style.FAIL}.{style.ENDC}')
else:
    print(f'{style.OKGREEN}(*) No vulnerability issues found in your image with specified parameters. Congratulations!{style.ENDC}')

read_log = input('\nDo you want to see more details now? (Y/n) ')
if read_log and read_log[0].lower() == 'y':
    print(trivy_run.stdout.decode())


print(f'{style.OKBLUE}Please contribute to this project! Visit {style.UNDERLINE}https://github.com/pcfeduardo/bsimage{style.ENDC}')