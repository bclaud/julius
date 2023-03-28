{
  description = "A very basic python flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix, ... }@inputs:
    flake-utils.lib.eachDefaultSystem (
      system: 
      let
        inherit (nixpkgs.lib) optional;
        poetry = poetry2nix.legacyPackages.${system};
        pkgs = import nixpkgs {
          inherit system;
        };

        start = pkgs.writeScriptBin "start" "poetry run uvicorn main:app --reload";
        format = pkgs.writeScriptBin "format" "black .";
      in
        with pkgs; {
          #packages = { default = callPackage ./default.nix {python = pkgs.python3; poetry2nix = inputs.poetry2nix; }; };
          packages = rec {
            default = poetry.mkPoetryApplication { projectDir = ./.; python = python311; };
            devEnv = poetry.mkPoetryEnv { projectDir = ./.;  };
            scripts = poetry.mkPoetryScriptsPackage { projectDir = ./.; python = python311; };
            dependencyEnv = default.dependencyEnv;
          };
          devShell = mkShell { name = "development-shell"; buildInputs = [ format start python311 pkgs.poetry python311Packages.poetry-core python311Packages.black python311Packages.pytest ffmpeg ]; };
        }
    );
}


