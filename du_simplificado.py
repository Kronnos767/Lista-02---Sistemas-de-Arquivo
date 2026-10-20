#!/usr/bin/env python3
"""du_simplificado: compara tamanho lógico e espaço alocado de arquivos."""
import argparse
import os
import stat
from pathlib import Path


def walk_files(root: Path):
    """Percorre a árvore sem seguir links simbólicos."""
    try:
        with os.scandir(root) as entries:
            for entry in entries:
                path = Path(entry.path)
                try:
                    info = entry.stat(follow_symlinks=False)
                except OSError as exc:
                    print(f"AVISO: não foi possível acessar {path}: {exc}")
                    continue

                if stat.S_ISLNK(info.st_mode):
                    continue
                if stat.S_ISDIR(info.st_mode):
                    yield from walk_files(path)
                elif stat.S_ISREG(info.st_mode):
                    yield path, info
    except OSError as exc:
        print(f"AVISO: não foi possível listar {root}: {exc}")


def main():
    parser = argparse.ArgumentParser(
        description="Soma tamanhos lógicos e alocados; identifica arquivos sparse."
    )
    parser.add_argument("diretorio", nargs="?", default=".", help="diretório inicial")
    args = parser.parse_args()
    root = Path(args.diretorio)

    logical_total = allocated_total = 0
    print(f"{'TAMANHO LÓGICO':>15} {'ALOCADO':>15}  TIPO  ARQUIVO")
    for path, info in walk_files(root):
        logical = info.st_size
        allocated = info.st_blocks * 512
        sparse = logical > allocated
        logical_total += logical
        allocated_total += allocated
        label = "SPARSE" if sparse else "-"
        print(f"{logical:15d} {allocated:15d}  {label:6} {path}")

    print("-" * 70)
    print(f"Total lógico:  {logical_total} bytes")
    print(f"Total alocado: {allocated_total} bytes")
    print(f"Diferença:     {logical_total - allocated_total} bytes")


if __name__ == "__main__":
    main()
