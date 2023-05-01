# To Run a package
1) Build the triton config for a model, such as flang-t5-small, by running the build_config.py file located in the model's directory. This will build the model repo in /usr/models.
2) Run tritonserver via: ```tritonserver --model-store /usr/models```. You should see a printout stating that the model is loaded and ready, like this
   ```
    I0430 21:58:20.713924 442867 server.cc:633] 
    +----------------------+---------+--------+
    | Model                | Version | Status |
    +----------------------+---------+--------+
    | google_flan_t5_small | 1       | READY  |
    +----------------------+---------+--------+
    ```

# Notes: #
## Create a tar file with all deps
* Download all the wheels for all deps:
```pip download -r requirements.txt -d <directory>```
* tar up the deps. `Don't compress this tar since wheels are already compressed and therefore uncompressible. For testing I was able to tar a directory in 2 seconds and tar.gz the same directory in 60 seconds. 30x slower to compress. The resulting two tar files are the same size.


https://github.com/triton-inference-server/python_backend