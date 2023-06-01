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