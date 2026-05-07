{
  description = "Project Tree development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSystem = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in {
      devShells = forEachSystem (pkgs: {
        default = pkgs.mkShell {
          packages = [
            pkgs.python310
            pkgs.uv
            pkgs.git
          ];

          env = {
            PIP_DISABLE_PIP_VERSION_CHECK = "1";
          };

          shellHook = ''
            echo "Project Tree dev shell loaded."
            echo "Run: uv pip install -e '.[dev]'"
          '';
        };
      });
    };
}
