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

https://github.com/rcastellotti/tinyben/blob/40ee71051109a1fbc0cdbcb628b51074fffd5964/run.py#L1-L23
## benchmarks i need now (will be removed)

+ __cpu__ ~> compilation (llvm,linux, imagemagick, godot), lz4
+ __memory__ ~> tinymembench, mbw
+ __I/O__ ~> redis, sqlite


## sample run
![image](https://github.com/rcastellotti/tinyben/assets/43064224/ee953b86-1141-4623-ad2a-ad211f74707d)
