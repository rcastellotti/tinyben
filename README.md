# tinyben

tinyben is an attempt to create a bencharking suite, similar to [phoronix-test-suite](https://www.phoronix-test-suite.com/), but simpler and easier to use. It designed to be <1000 lines of code [1](https://github.com/geohot/minikeyvalue).

We are always supporting (at least) the latest Ubuntu LTS version.


todo:

+ implement different ways to save results (csv,json?)
+ implement representation via matplotlib figures
+ every benchmark should describe what it does, report properly what it does
+ implement both interactive and non interactive options (if applicable)
+ implement a cli to run commands
+ implement a web ui to view results and run tests (flask)
+ write a CI pipeline to generate documentation (listing the benchmarks)
+ implement bundles of benchmarks (compilation should run several microbenchmarks such as llvm, kernel..)


sample output 

```
benchmark                status  result
----------------------------------------
llvm-project compilation   ✅     500 s
kernel compilation         ❌       X 
```


## how to use

```python
from tinyben import tinyben
import logging

logging.basicConfig(level=logging.INFO)
tb = tinyben(benchmarks=["llvm"])
tb.run()
```


## benchmarks supported at the moment

+ compilation https://openbenchmarking.org/suite/pts/compilation
+ Timed Erlang/OTP Compilation
+ Timed FFmpeg Compilation
+ Timed GCC Compilation
+ Timed GDB GNU Debugger Compilation
+ Timed Godot Game Engine Compilation
+ Timed ImageMagick Compilation
+ Timed Linux Kernel Compilation
