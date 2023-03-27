{pkgs, poetry2nix, python, ...}: 

pkgs.poetry2nix.mkPoetryApplication rec {
  inherit python;

  projectDir = ./.;

  pyproject = projectDir + "/pyproject.toml";
  poetrylock = projectDir + "/poetry.lock";

  doCheck = false;

  overrides = pkgs.poetry2nix.defaultPoetryOverrides.extend
    (self: super: {
        iniconfig = super.iniconfig.overridePythonAttrs ( old: { buildInputs = (old.buildInputs or [ ]) ++ [ super.hatchling ];});
    });
}
