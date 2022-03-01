# bsimage - build & scan image tool

## Requirements 
- [Trivy](https://aquasecurity.github.io/trivy)
- [Docker](https://www.docker.com/get-started)

## Usage
```
usage: bsimage.py [--dockerfile DOCKERFILE] [--only-os] image
```
### Syntax
- --dockerfile or -d: if this option is set, bsimage will automatically build the image with the specified file
- --only-os or -o: this option forces the scan to scan only the operating system layer
- image: image name
#### Examples
- Building image using Dockerfile
```
bsimage.py -d Dockerfile myimage:1.0
bsimage.py -d dockerfile-customized myimage:1.0
bsimage.py --dockerfile Dockerfile myimage:1.0
```

- Scanning only the operating system layer
```
bsimage.py -o myimage:1.0
bsimage.py --only-os myimage:1.0
```

- Building and Scanning (only OS layer)
```
bsimage.py -d Dockerfile -o myimage:1.0
```