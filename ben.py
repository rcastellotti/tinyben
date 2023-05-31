import pygit2
import urllib.request
import pathlib
import subprocess
import tarfile

## pts/compilation

path = pathlib.Path(__file__).parent.resolve()
# https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-16.0.4.tar.gz
# https://llvm.org/docs/GettingStarted.html#getting-the-source-code-and-building-llvm

# cmake -S llvm -DCMAKE_BUILD_TYPE=Release -B build -G Ninja
llvm_tar_gz="llvmorg-16.0.4.tar.gz"
urllib.request.urlretrieve(f"https://github.com/llvm/llvm-project/archive/refs/tags/{llvm_tar_gz}", llvm_tar_gz)
tar = tarfile.open(llvm_tar_gz)
tar.extractall(path="llvm-project")

if retcode == 0:
    print("Extracted successfully")
else:
    raise IOError('tar exited with code %d' % retcode)
