{
  description = "dev shell for TWMA app";

  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };
  in {
    devShells.${system}.default = pkgs.mkShell {
      packages = with pkgs; [
        python314
        python314Packages.pip
        
        #possibly overkill but need everything from qt6
        qt6.qtbase
        qt6.qtwebengine
        qt6.qttranslations
        python314Packages.pyqt6
        python314Packages.pyqt6-webengine

        # python314Packages.pyinstaller
        # python314Packages.pywebview
        # python314Packages.pypdf
        # python314Packages.flask
        # python314Packages.cryptography

      ];
    };
  };
}
