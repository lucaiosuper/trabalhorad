import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import re
import requests

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

        padrao_data = r"\b\d{4}-\d{2}-\d{2}\b"
        datas_encontradas = re.findall(padrao_data, texto_total)

        if not datas_encontradas:
            messagebox.showinfo("Resultado", "Nenhuma data encontrada no PDF.")
            return

        anos = sorted({data.split("-")[0] for data in datas_encontradas})
        feriados_por_ano = {}

        for ano in anos:
            url = f"https://date.nager.at/api/v3/PublicHolidays/{ano}/BR"
            response = requests.get(url)
            if response.status_code == 200:
                feriados = response.json()
                feriados_por_ano[ano] = {f["date"] for f in feriados}
            else:
                feriados_por_ano[ano] = set()

        feriados_no_pdf = [
            data for data in datas_encontradas
            if data in feriados_por_ano.get(data.split("-")[0], set())
        ]

        if feriados_no_pdf:
            resultado = "As seguintes datas são feriados:\n" + "\n".join(feriados_no_pdf)
        else:
            resultado = "Nenhuma das datas encontradas é feriado."

        messagebox.showinfo("Resultado", resultado)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro:\n{e}")

janela = tk.Tk()
janela.title("Trabalho")
janela.geometry("350x150")

botao = tk.Button(janela, text="Selecione um PDF", command=carregar_pdf)
botao.pack(pady=40)

janela.mainloop()
