with import <nixpkgs> { };
mkShell {
  nativeBuildInputs = [
    pkg-config #redis
    python310Packages.requests
    python310Packages.tqdm

  ];
}