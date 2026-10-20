# Lista 02 — Sistemas de Arquivo

**Aluno:** Guilherme Emanuel  
**Linguagem:** Python 3 (biblioteca padrão; Linux recomendado para `st_blocks`)

## Arquivos
- `du_simplificado.py`: soma tamanho lógico (`st_size`) e espaço alocado (`st_blocks × 512`), marcando possíveis arquivos sparse.
- `apaga_logs.py`: busca recursivamente arquivos regulares `.log` com tamanho estritamente maior que `N`; pede confirmação no terminal e ignora links simbólicos.

## Execução
```bash
python3 du_simplificado.py /caminho/da/pasta
python3 apaga_logs.py /caminho/da/pasta 1048576
```
O segundo comando seleciona arquivos `.log` maiores que 1 MiB (1.048.576 bytes). Para testar com segurança, crie uma pasta temporária com arquivos fictícios antes de usar em dados reais.

## Observações
- `st_blocks` é reportado em unidades de 512 bytes em sistemas POSIX comuns; os valores e a semântica podem variar entre sistemas de arquivos/plataformas.
- Um arquivo é marcado como `SPARSE` quando o tamanho lógico supera o espaço alocado reportado. Isso é um indício prático, não uma prova universal de como o sistema de arquivos armazena cada região.
- A rotina de exclusão pede confirmação para cada caminho e usa `lstat`/`follow_symlinks=False` para não tratar symlinks como arquivos regulares. Como em qualquer programa de sistema de arquivos, ainda pode haver condições de corrida se outro processo modificar a árvore simultaneamente; execute com privilégios mínimos.
