with import <nixpkgs> { };
mkShell {
  nativeBuildInputs = [
    pre-commit
    ruff
    git
    python311Packages.black
    python311Packages.requests
    python311Packages.tqdm
    pkg-config #redis
    cmake #llvm
    ninja #llvm
    flex #linux
    bison #linux
    bc #linux
    elfutils #linux
    fakeroot #linux
    openssl #linux
    scons #godot
    lz4 #lz4 :)
  ];
}   