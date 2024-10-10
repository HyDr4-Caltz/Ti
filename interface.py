from tkinter import *
from tkinter import ttk
import sqlite3

janela = Tk()

#back-end
class Funcs():
    def limpa_tela(self):
        self.palavra_ent.delete(0,END)
        self.tag_ent.delete(0,END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("palavras.bd")
        self.cursor = self.conn.cursor()
    def desconect_bd(self):
        self.conn.close()
    def montaTabela(self):
        self.conecta_bd(); print('Conectando no Banco de dados...')
        #Criar tabelas
        self.cursor.execute("""
        CREAT TABLE IF NOT EXISTS palavras(
            pal INTEGER PRIMARY KEY,
            erros CHAR(1),
            acertos CHAR(1)
        )""")

#front-end
class Application(Funcs):
    def __init__(self):
        #Selfs

        self.janela = janela
        self.tela()
        self.frames()
        self.widgets_1()
        self.widgets_2()
        self.list_frame2()
        janela.mainloop()
    def tela(self):
        #Configurar Tela

        self.janela.title("Jogo da forca")
        self.janela.config(background= '#82cdce')
        self.janela.geometry("1000x600")
        self.janela.resizable(True,True )
    def frames(self):
        #Definindo Frame 1
        self.frame_1 = Frame(self.janela, bd = 4, bg='#d4e8ed',highlightbackground='#02303b',
                             highlightthickness=2)
        self.frame_1.place(relx=0.02,rely=0.02, relwidth = 0.96, relheight = 0.46)

        #Definindo Frame 2
        self.frame_2 = Frame(self.janela, bd = 4, bg='#d4e8ed',highlightbackground='#02303b',
                             highlightthickness=2)
        self.frame_2.place(relx=0.02,rely=0.5, relwidth = 0.96, relheight = 0.46)
    def widgets_1(self):
        #Botao Adicionar

        self.bt_add = Button(self.frame_1,text="Adicionar",bd=4,font= ('Courier', 8,'bold'),command=self.limpa_tela)
        self.bt_add.place(relx=0.2,rely=0.27,relwidth=0.1,relheight=0.1)

        #Palavra Aleatoria

        self.bt_random = Button(self.frame_1, text="Aleatoria", bd=4,font= ('Courier', 8,'bold'))
        self.bt_random.place(relx=0.01, rely=0.883, relwidth=0.1, relheight=0.1)

        #Label e Entrada Palavra

        self.lb_palavra = Label(self.frame_1, text="Palavra",bg='#d4e8ed')
        self.lb_palavra.place(relx=0.068,rely=0.01)

        self.palavra_ent = Entry(self.frame_1)
        self.palavra_ent.place(relx=0.01,rely=0.11,relwidth=0.17,relheight=0.1)
        #Label e Entrada Tag

        self.lb_tag = Label(self.frame_1, text="Tag",bg='#d4e8ed')
        self.lb_tag.place(relx=0.074,rely=0.3)

        self.tag_ent = Entry(self.frame_1)
        self.tag_ent.place(relx=0.03,rely=0.41,relwidth=0.12,relheight=0.1)
    def widgets_2(self):
        def limit_cr(*args):
            entrada = texto.get()
            if len(entrada) > 1:
                texto.set(entrada[0])
        #Tentar
        self.bt_try = Button(self.frame_2, text="Tentar", bd=4,font= ('Times', 8,'bold'))
        self.bt_try.place(relx=0.02, rely=0.3, relwidth=0.1, relheight=0.1)
        #Label e Entrada try
        texto = StringVar()
        texto.trace_add("write", limit_cr)

        self.lb_try = Label(self.frame_2, text="Letra",bg='#d4e8ed',)
        self.lb_try.place(relx=0.05,rely=0.01)

        self.try_ent = Entry(self.frame_2,textvariable=texto)
        self.try_ent.place(relx=0.01,rely=0.11,relwidth=0.12,relheight=0.1)
    def list_frame2(self):

        #Define nome/colunas

        self.list_pal = ttk.Treeview(self.frame_2, height=3, columns=("col1","col2","col3"))
        self.list_pal.heading("#0", text="")
        self.list_pal.heading("#1", text="Erros")
        self.list_pal.heading("2", text="Acertos")

        #Define padrão

        self.list_pal.column("#0",width=1)
        self.list_pal.column("1",width=250)
        self.list_pal.column("2",width=250)

        #Define proporção

        self.list_pal.place(relx=0.15,rely=0.01,relwidth=0.81,relheight=0.85)

        #Define Scroll

        self.scroolList = Scrollbar(self.frame_2,orient='vertical')
        self.list_pal.configure(yscrollcommand=self.scroolList.set)
        self.scroolList.place(relx=0.96,rely=0.01,relwidth=0.04,relheight=0.85)
Application()