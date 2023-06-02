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

https://github.com/stevemar/code-reference-in-readme/blob/031e04f922c14ecd5b03a79d8c979ba8f3ab1e39/src/main.py#L1-L6


## benchmarks supported at the moment

+ compilation https://openbenchmarking.org/suite/pts/compilation
<!-- + Timed FFmpeg Compilation -->
+ Timed Godot Game Engine Compilation
