# tinyben

tinyben is an attempt to create a bencharking suite, similar to [phoronix-test-suite](https://www.phoronix-test-suite.com/), but simpler and easier to use. It designed to be <1000 lines of code [1](https://github.com/geohot/minikeyvalue).

We are always supporting (at least) the latest Ubuntu LTS version.


todo:

+ implement representation via matplotlib figures
+ every benchmark should describe what it does, report properly what it does
+ implement benchmark fields (name, short name, description, required packages)
+ implement cleanup functions (use tmpdirectory)
+ implement status (recode subprocess.call)


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
<!-- + Timed FFmpeg Compilation -->
+ Timed Godot Game Engine Compilation