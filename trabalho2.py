import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2

def carregar_pdf():
    caminho_pdf = filedialog.askopenfilename(
        title="Selecione um arquivo PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    
    if not caminho_pdf:
        return

    try:
        with open(caminho_pdf, "rb") as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            texto_total = ""
            for pagina in leitor.pages:
                texto_total += pagina.extract_text() or ""
        
        print("PDF carregado.")
        print(f"Número de páginas: {len(leitor.pages)}")
        messagebox.showinfo("Sucesso", "PDF carregado.")

    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível ler o PDF:\n{e}")

janela = tk.Tk()
janela.title("Trabalho")
janela.geometry("300x150")

botao = tk.Button(janela, text="Selecione um PDF", command=carregar_pdf)
botao.pack(pady=40)

janela.mainloop()
