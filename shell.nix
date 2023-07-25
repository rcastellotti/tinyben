with import <nixpkgs> { };
mkShell {
  nativeBuildInputs = [
    pre-commit
    ruff
    python311Packages.black
    pkg-config #redis
    python311Packages.requests
    python311Packages.tqdm

  ];
}