{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
    nativeBuildInputs = [
        pkgs.python3
        pkgs.python312Packages.pygame
        pkgs.python312Packages.tkinter

    ];
    shellHook = ''
    eval $(ssh-agent -s)
    ssh-add ~/.ssh/github
    '';
}
