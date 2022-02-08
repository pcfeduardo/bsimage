# BSImage (build&scan image)

## Requirements 
- [Trivy](https://github.com/aquasecurity/trivy)
- [Docker](https://www.docker.com/get-started)

## BSImage (shell script version)

### Usage of build (shell script version)
```
./bsimage.sh start <image:tag> <dir_path> <dockerfile>
```

## BSImage (golang version)
### Installing bsimage on Linux
```
sudo curl -o /usr/local/bin/bsimage https://raw.githubusercontent.com/pcfeduardo/bsimage/master/bin/bsimage_linux && chmod +x /usr/local/bin/bsimage
```
### Usage of bsimage (golang version)
```
bsimage <image:tag> <dockerfile>
```