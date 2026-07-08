import os
from pathlib import Path

# Pasta que será analisada
PASTA_RAIZ = Path(".").resolve()

# Arquivo de saída
ARQUIVO_SAIDA = "estrutura_e_conteudo.txt"

# Extensões consideradas binárias
EXTENSOES_BINARIAS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".ico",
    ".webp",
    ".exe",
    ".dll",
    ".so",
    ".bin",
    ".zip",
    ".rar",
    ".7z",
    ".tar",
    ".gz",
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".mp3",
    ".wav",
    ".ogg",
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".class",
    ".pyc",
    ".obj",
}


def escrever_arvore(pasta, arquivo):
    arquivo.write("=" * 80 + "\n")
    arquivo.write("ESTRUTURA DE DIRETÓRIOS\n")
    arquivo.write("=" * 80 + "\n\n")

    for root, dirs, files in os.walk(pasta):
        dirs.sort()
        files.sort()

        nivel = Path(root).relative_to(pasta).parts
        indent = "    " * len(nivel)

        nome = Path(root).name if root != str(pasta) else pasta.name
        arquivo.write(f"{indent}{nome}/\n")

        for f in files:
            arquivo.write(f"{indent}    {f}\n")


def escrever_conteudos(pasta, arquivo):
    arquivo.write("\n\n")
    arquivo.write("=" * 80 + "\n")
    arquivo.write("CONTEÚDO DOS ARQUIVOS\n")
    arquivo.write("=" * 80 + "\n")

    for root, dirs, files in os.walk(pasta):
        dirs.sort()
        files.sort()

        for nome in files:
            caminho = Path(root) / nome

            # Não incluir o próprio arquivo de saída
            if caminho.resolve().name == ARQUIVO_SAIDA:
                continue

            arquivo.write("\n")
            arquivo.write("=" * 80 + "\n")
            arquivo.write(f"ARQUIVO: {caminho.resolve()}\n")
            arquivo.write("=" * 80 + "\n")

            if caminho.suffix.lower() in EXTENSOES_BINARIAS:
                arquivo.write("[Arquivo binário ignorado]\n")
                continue

            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    arquivo.write(f.read())
            except UnicodeDecodeError:
                try:
                    with open(caminho, "r", encoding="latin-1") as f:
                        arquivo.write(f.read())
                except Exception as e:
                    arquivo.write(f"[Erro ao ler arquivo: {e}]\n")
            except Exception as e:
                arquivo.write(f"[Erro ao ler arquivo: {e}]\n")

            arquivo.write("\n")


def main():
    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as saida:
        escrever_arvore(PASTA_RAIZ, saida)
        escrever_conteudos(PASTA_RAIZ, saida)

    print(f"Arquivo gerado: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    main()
