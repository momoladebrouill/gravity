{ pkgs ? import <nixpkgs> {} }:

  pkgs.mkShell {
    nativeBuildInputs = [
        # pretty cool that's only necessary
        pkgs.sfml
    ];
}
