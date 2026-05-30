{
  description = "Project Tree development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSystem = f: nixpkgs.lib.genAttrs systems (system: f system nixpkgs.legacyPackages.${system});
    in {
      packages = forEachSystem (_: pkgs:
        let
          pythonPkgs = pkgs.python314Packages;
        in {
          default = pythonPkgs.buildPythonApplication {
            pname = "projtree";
            version = "1.2";
            pyproject = true;
            src = self;
            nativeBuildInputs = with pythonPkgs; [ setuptools wheel ];
            propagatedBuildInputs = with pythonPkgs; [ watchdog ];
            pythonImportsCheck = [ "projtree" ];
          };
        });

      apps = forEachSystem (system: _: {
        default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/projtree";
        };
      });

      devShells = forEachSystem (system: pkgs: {
        default = pkgs.mkShell {
          packages = [
            pkgs.python314
            pkgs.uv
            pkgs.git
          ];

          PIP_DISABLE_PIP_VERSION_CHECK = "1";

          shellHook = ''
            GREEN="\033[0;32m"
            BLUE="\033[0;34m"
            RESET="\033[0m"

            printf "%b\n" "''${BLUE}Project Tree dev shell loaded.''${RESET}"
            printf "%b\n" "''${GREEN}Installing editable package...''${RESET}"
            uv pip install -e ".[dev]"
            printf "%b\n" "''${GREEN}Editable package installed. Happy coding!😁''${RESET}"
          '';
        };

        cli = pkgs.mkShell {
          packages = [ self.packages.${system}.default ];
        };
      });
    };
}
