# Notes: #
## Create a tar file with all deps
* Download all the wheels for all deps:
```pip download -r requirements.txt -d <directory>```
* tar up the deps. `Don't compress this tar since wheels are already compressed and therefore uncompressible. For testing I was able to tar a directory in 2 seconds and tar.gz the same directory in 60 seconds. 30x slower to compress. The resulting two tar files are the same size.


https://github.com/triton-inference-server/python_backend