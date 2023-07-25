# let
#   pkgs = import <nixpkgs> {};
# in
# pkgs.mkShell {
#   nativeBuildInputs = with pkgs; [
#     pkgs.pre-commit
#     ruff
#     git
#     pkg-config #redis
#     cmake #llvm
#     ninja #llvm
#     flex #linux
#     bison #linux
#     bc #linux
#     elfutils #linux
#     fakeroot #linux
#     openssl #linux
#     scons #godot
#     lz4 #lz4 :)
#     python3.withPackages (pyPkgs: with pyPkgs; [ black requests tqdm])

#   ];
# }   
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
];
}