import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import requests
import time

# CREDITOS: LUIZ / https://github.com/Luwix

class ClimaApp(tk.Tk):
    # ADICIONE SUA CHAVE API ATRAVES DO SITE: https://home.openweathermap.org
    API_KEY = "NUMERO DA CHAVE"

    def __init__(self):
        super().__init__()
        self.title('Clima')
        height = 550
        width = 940
        x = (self.winfo_screenwidth() // 2) - (width // 2)A
        y = (self.winfo_screenheight() // 4) - (height // 4)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.resizable(0, 0)
        self.configure(bg="#050119")

# =============== CIDADE LABEL  ==================== #

        CidadeLabel = Label(
            self,
            text="Nome da Cidade:", 
            fg="#FFFFFF",
            font=("yu gothic ui bold", 20 * -1),
            bg="#050119"
            )
        CidadeLabel.place(x=30, y=20)

# =============== INPUT CIDADE  ==================== #

        self.CidadeValor = Entry(
            self, 
            width=40,
            borderwidth=2,
            highlightthickness=2,
            font=('italic', 17),
            relief='flat'
            )
        self.CidadeValor.place(x=200, y=20)

# =============== PESQUISAR BOTÃO ==================== #

        self.pesquisaIMG = PhotoImage(file="pesquisar.png")
        PesquisaBTN = Button(
            self,
            image=self.pesquisaIMG,
            command=self.Executar,
            borderwidth=0,
            highlightthickness=0,
            relief='flat',
            cursor="hand2",
            width=40,
            height=40,
            bg="#050119",
            activebackground="#050119",
        )
        PesquisaBTN.place(x=750, y=20)

# =============== GRAUS CELSIUS LABEL  ==================== #

        self.TemperaturaLabel = Label(
            self,
            text="",
            fg="blue",
            bg="#050119",
            font=('black', 48)
        )
        self.TemperaturaLabel.place(x=400, y=150)

# =============== DESCRIÇÃO LABEL ==================== #

        self.StatusLabel = Label(
            self, 
            text="", 
            fg="blue", 
            bg="#050119",
            font=('Helvetica', 18)
            )
        self.StatusLabel.place(x=self.winfo_width()/2, y=self.winfo_height()/2)

# =============== TEMPO REAL ( HORA ) LABEL  ==================== #

        self.HoraLabel = Label(
            self, 
            bg="#050119",
            font=('Helvetica', 48),
            borderwidth=0,
            highlightthickness=0,
            )
        self.HoraLabel.place(x=340, y=320)

# =============== FUNÇÃO DE REQUEST DA API  ==================== #

    def ClimaLocal(self):
        Nome_Cidade = self.CidadeValor.get()
        url = f'http://api.openweathermap.org/data/2.5/weather?q={Nome_Cidade}&appid={self.API_KEY}&units=metric&lang=pt_br'
        response = requests.get(url)
        data = response.json()
        if Nome_Cidade == '':
            return
        if data['cod'] == 200:
            temperatura = data['main']['temp']
            temperatura_str = str(temperatura)
            temperatura_int = int(temperatura_str.split('.')[0])
            descricao = data['weather'][0]['description']
            self.TemperaturaLabel.configure(text=f"{temperatura_int}°C")
            palavras = descricao.split()
            palavras_formatadas = [palavra[:1].upper() + palavra[1:].lower() for palavra in palavras]
            descricao_formatada = " ".join(palavras_formatadas)
            self.StatusLabel.configure(text=descricao_formatada)
            self.update_idletasks()
            x = (self.winfo_width() - self.StatusLabel.winfo_width()) / 2
            y = (self.winfo_height() - self.StatusLabel.winfo_height()) / 2
            self.StatusLabel.place(x=x, y=y)
        else:
            messagebox.showinfo("Erro na solicitação", f"{data['message']}")

# =============== FUNÇÃO HORARIO ==================== #

    def TempoReal(self):
        Nome_Cidade = self.CidadeValor.get()
        if Nome_Cidade == '':
            return
        else:
            now = time.strftime("%H:%M:%S")
            self.HoraLabel.configure(fg="blue", text=now)
            self.after(1000, self.TempoReal)

# =============== FUNÇÃO CHECAR SE O INPUT ESTÁ VÁZIO  ==================== #
    
    def CheckInput(self):
        Nome_Cidade = self.CidadeValor.get()
        if Nome_Cidade == '':
            messagebox.showinfo("Alerta", "Adicione um nome de uma Cidade, País ou Estado!")


# =============== FUNÇÃO PARA EXECUTAR TODAS AS DEF NO BOTAO PESQUISAR  ==================== #

    def Executar(self):
        self.CheckInput()
        self.TempoReal()
        self.ClimaLocal()


if __name__ == "__main__":
    app = ClimaApp()
    app.mainloop()
