with import <nixpkgs> {};

mkShell {
  buildInputs = [ stdenv.cc.cc.lib ];

  shellHook = ''
    export LD_LIBRARY_PATH=${stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
  '';
}
