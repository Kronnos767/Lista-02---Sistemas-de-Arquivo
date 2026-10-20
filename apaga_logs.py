#!/usr/bin/env python3
"""Remove interativamente arquivos .log maiores que N bytes, sem seguir symlinks."""
import argparse
import os
import stat
from pathlib import Path


def candidates(root: Path, minimum: int):
    """Produz arquivos regulares elegíveis; links simbólicos são ignorados."""
    try:
        with os.scandir(root) as entries:
            for entry in entries:
                path = Path(entry.path)
                try:
                    info = entry.stat(follow_symlinks=False)
                except OSError as exc:
                    print(f"AVISO: não foi possível verificar {path}: {exc}")
                    continue

                if stat.S_ISLNK(info.st_mode):
                    continue
                if stat.S_ISDIR(info.st_mode):
                    yield from candidates(path, minimum)
                elif (
                    stat.S_ISREG(info.st_mode)
                    and info.st_size > minimum
                    and path.suffix.lower() == ".log"
                ):
                    yield path
    except OSError as exc:
        print(f"AVISO: não foi possível listar {root}: {exc}")


def main():
    parser = argparse.ArgumentParser(
        description="Localiza e pergunta antes de apagar arquivos .log maiores que N."
    )
    parser.add_argument("diretorio", help="raiz da busca")
    parser.add_argument("N", type=int, help="limite em bytes; seleciona tamanho > N")
    args = parser.parse_args()

    if args.N < 0:
        parser.error("N deve ser zero ou positivo")

    root = Path(args.diretorio)
    if not root.is_dir() or root.is_symlink():
        parser.error("o caminho inicial deve ser um diretório real, não symlink")

    for path in candidates(root, args.N):
        # A confirmação é exibida no stdout e exige resposta explícita.
        answer = input(f"Apagar este arquivo? [s/N] {path} ")
        if answer.strip().lower() not in {"s", "sim"}:
            print(f"MANTIDO: {path}")
            continue

        # Revalida imediatamente antes da remoção para evitar seguir symlinks.
        try:
            info = path.lstat()
            if not stat.S_ISREG(info.st_mode) or path.is_symlink():
                print(f"IGNORADO (não é arquivo regular): {path}")
                continue
            if info.st_size <= args.N or path.suffix.lower() != ".log":
                print(f"IGNORADO (o arquivo mudou): {path}")
                continue
            path.unlink()
            print(f"REMOVIDO: {path}")
        except OSError as exc:
            print(f"ERRO ao remover {path}: {exc}")


if __name__ == "__main__":
    main()
