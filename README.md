# tinyben

tinyben is an attempt to create a bencharking suite, similar to [phoronix-test-suite](https://www.phoronix-test-suite.com/), but simpler and easier to use. tinyBen is designed to ben <1000 lines of code [1](https://github.com/geohot/minikeyvalue).

We are always supporting (at least) the latest Ubuntu LTS version.

## usage

```bash
python3 -m venv venv
pip3 install -r requirements.txt
python3 run.py 
```
If you need to run with root permission (`apt-get` is part of a benchmark) run instead `sudo venv/bin/python3 runner.py`

https://github.com/rcastellotti/tinyben/blob/2c74e54e34ad1a28808c242b9d1a87e2ff788533/run.py#L1-L11

# benchmarks i need now (will be removed)

+ __cpu__ ~> compilation (llvm,linux, imagemagick, godot), lz4
+ __memory__ ~> tinymembench, RAMspeed, mbw
+ __I/O__ ~> redis, sqlite
