# BSImage (build&scan image)

## Requirements 
- [Trivy](https://github.com/aquasecurity/trivy)
- [Docker](https://www.docker.com/get-started)

## Usage of build (shell script)
```
./build.sh start <image:tag> <dir_path> <dockerfile>
```

## Usage of bsimage (go application)
```
bsimage <image:tag> <dockerfile>
```