let
  pkgs = import <nixpkgs> {};
in
pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (ps: [
      ps.black
      ps.requests
      ps.tqdm
    ]))
  pkgs.pre-commit
  pkgs.ruff
  pkgs.git
  pkgs.pkg-config # redis
  pkgs.cmake # llvm
  pkgs.ninja # llvm
  pkgs.flex # linux
  pkgs.bison # linux
  pkgs.bc # linux
  pkgs.elfutils # linux
  pkgs.fakeroot # linux
  pkgs.openssl # linux
  pkgs.scons # godot
  pkgs.lz4 # lz4 :)
  pkgs.redis # redis :)
];
}