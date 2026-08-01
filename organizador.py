import os
import shutil
import sys

PASTA_DOWNLOADS = os.path.expanduser("~/Downloads")

REGRAS_ORGANIZACAO = {
    "Imagens": [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"],
    "Documentos": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
    "Compactados": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Instaladores": [".deb", ".rpm", ".tar.zst", ".sh", ".bin", ".appimage"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Outros": []
}

def organizar_downloads():
    if not os.path.exists(PASTA_DOWNLOADS):
        print("❌ Pasta Downloads não encontrada.")
        return

    arquivos = [f for f in os.listdir(PASTA_DOWNLOADS) if os.path.isfile(os.path.join(PASTA_DOWNLOADS, f))]
    
    if not arquivos:
        print("✨ A pasta de Downloads já está limpa!")
        return

    for nome_arquivo in arquivos:
        caminho_completo = os.path.join(PASTA_DOWNLOADS, nome_arquivo)
        _, extensao = os.path.splitext(nome_arquivo)
        extensao = extensao.lower()

        pasta_destino_nome = "Outros"
        for nome_pasta, extensoes_permitidas in REGRAS_ORGANIZACAO.items():
            if extensao in extensoes_permitidas:
                pasta_destino_nome = nome_pasta
                break

        pasta_destino_completa = os.path.join(PASTA_DOWNLOADS, pasta_destino_nome)
        if not os.path.exists(pasta_destino_completa):
            os.makedirs(pasta_destino_completa)

        try:
            shutil.move(caminho_completo, os.path.join(pasta_destino_completa, nome_arquivo))
            print(f"💀 [Movido]: {nome_arquivo} -> {pasta_destino_nome}")
        except Exception as e:
            print(f"❌ Erro ao mover {nome_arquivo}: {e}")

def desfazer_organizacao():
    print("⏳ Iniciando ritual de reversão... Trazendo arquivos de volta.")
    
    # Varre as pastas que o script gerou
    for nome_pasta in REGRAS_ORGANIZACAO.keys():
        caminho_pasta = os.path.join(PASTA_DOWNLOADS, nome_pasta)
        
        if os.path.exists(caminho_pasta) and os.path.isdir(caminho_pasta):
            # Pega todos os arquivos guardados dentro dela
            for nome_arquivo in os.listdir(caminho_pasta):
                caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
                
                # Move de volta para a raiz do Downloads
                try:
                    shutil.move(caminho_arquivo, os.path.join(PASTA_DOWNLOADS, nome_arquivo))
                    print(f"🔄 [Restaurado]: {nome_arquivo} voltou para Downloads")
                except Exception as e:
                    print(f"❌ Erro ao restaurar {nome_arquivo}: {e}")
            
            # Deleta a pasta vazia que sobrou
            try:
                os.rmdir(caminho_pasta)
            except:
                pass
                
    print("✨ Tudo voltou ao caos original!")

if __name__ == "__main__":
    # Verifica se o usuário digitou "--desfazer" no terminal
    if len(sys.argv) > 1 and sys.argv[1] == "--desfazer":
        desfazer_organizacao()
    else:
        print("🛸 Organizador Abissal Ativo. Limpando o caos...")
        organizar_downloads()
        print("✨ Limpeza concluída!")
