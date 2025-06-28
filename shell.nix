# shell.nix
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.uv
  ];

  shellHook = ''
    export PYTHONPATH=$(pwd)
    echo "Virtual environment ready. Use: uv venv && source .venv/bin/activate"
    
    export upy="uv run python manage.py"

    alias run="$upy runserver"
    alias migrations="$upy makemigrations"
    alias migrate="$upy migrate"
    alias createapp="$upy startapp"
    alias createadmin="$upy createadmin"
  '';
}

