import os
import shutil
import sys

PASTA_DOWNLOADS = os.path.expanduser("~/Downloads")

REGRAS_ORGANIZACAO = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
    "Compressed": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Installers": [".deb", ".rpm", ".tar.zst", ".sh", ".bin", ".appimage"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Others": []
}

def organizar_downloads():
    if not os.path.exists(PASTA_DOWNLOADS):
        print("❌ Downloads folder not found.")
        return

    arquivos = [f for f in os.listdir(PASTA_DOWNLOADS) if os.path.isfile(os.path.join(PASTA_DOWNLOADS, f))]
    
    if not arquivos:
        print("✨ Downloads folder is already clean!")
        return

    for nome_arquivo in arquivos:
        caminho_completo = os.path.join(PASTA_DOWNLOADS, nome_arquivo)
        _, extensao = os.path.splitext(nome_arquivo)
        extensao = extensao.lower()

        pasta_destino_nome = "Others"
        for nome_pasta, extensoes_permitidas in REGRAS_ORGANIZACAO.items():
            if extensao in extensoes_permitidas:
                pasta_destino_nome = nome_pasta
                break

        pasta_destino_completa = os.path.join(PASTA_DOWNLOADS, pasta_destino_nome)
        if not os.path.exists(pasta_destino_completa):
            os.makedirs(pasta_destino_completa)

        try:
            shutil.move(caminho_completo, os.path.join(pasta_destino_completa, nome_arquivo))
            print(f"💀 [Moved]: {nome_arquivo} -> {pasta_destino_nome}")
        except Exception as e:
            print(f"❌ Error moving {nome_arquivo}: {e}")

def desfazer_organizacao():
    print("⏳ Starting reversion ritual... Bringing files back.")
    
    for nome_pasta in REGRAS_ORGANIZACAO.keys():
        caminho_pasta = os.path.join(PASTA_DOWNLOADS, nome_pasta)
        
        if os.path.exists(caminho_pasta) and os.path.isdir(caminho_pasta):
            for nome_arquivo in os.listdir(caminho_pasta):
                caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
                
                try:
                    shutil.move(caminho_arquivo, os.path.join(PASTA_DOWNLOADS, nome_arquivo))
                    print(f"🔄 [Restored]: {nome_arquivo} returned to Downloads")
                except Exception as e:
                    print(f"❌ Error restoring {nome_arquivo}: {e}")
            
            try:
                os.rmdir(caminho_pasta)
            except:
                pass
                
    print("✨ Everything is back to the original chaos!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--desfazer":
        desfazer_organizacao()
    else:
        print("🛸 Abyssal Organizer Active. Clearing the chaos...")
        organizar_downloads()
        print("✨ Cleanup complete!")
