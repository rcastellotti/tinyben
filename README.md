# tinyben

tinyben is an attempt to create a bencharking suite, similar to [phoronix-test-suite](https://www.phoronix-test-suite.com/), but simpler and easier to use. tinyBen is designed to ben <1000 lines of code [1](https://github.com/geohot/minikeyvalue).

Where possible `tinyben` appends data to a file in `./results` in csv format (useful for `pd.read_csv()`), when it's not possible (i.e. when running an external benchmark that does not support machine readable output, like [`ssvb/tinymembench`](https://github.com/ssvb/tinymembench)) it appends results to a `.txt` file.

Artifacts (cloned tarballs etc.) are stored in `.cache/`.

`tinyben` uses the [nix](https://nixos.org/) package manager, to run benchmarks enter the nix-shell using `nix-shell`
# Usage 

Using `tinyben` is incredibly simple, just import the benchmark and run it, for example:

```python3
#run.py
import tinyben.benchmarks.llvm as llvm
import logging
from tinyben.log import logger
logger.setLevel(logging.INFO)
llvm.main()
```
