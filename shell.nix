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
  ];
}