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
            pkgs.python314
            pkgs.uv
            pkgs.git
          ];

          env = {
            PIP_DISABLE_PIP_VERSION_CHECK = "1";
          };

          shellHook = ''
            GREEN="\033[0;32m"
            BLUE="\033[0;34m"
            RESET="\033[0m"

            echo -e "$BLUEProject Tree dev shell loaded.$RESET"
            echo -e "$GREENInstalling Project Tree package (editable)...$RESET"
            uv pip install -e ".[dev]"
          '';
        };
      });
    };
}
