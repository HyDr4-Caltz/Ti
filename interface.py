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
        self.conn = sqlite3.connect("palavras.db")
        self.cursor = self.conn.cursor(); print('Conectando no Banco de dados...')
    def desconect_bd(self):
        self.conn.close(); print("Banco de dados desconectado")
    def montaTabela(self):
        self.conecta_bd()
        #Criar tabelas
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS palavras(
                pal CHAR(40) NOT NULL,
                Tag CHAR(40) NOT NULL
            );
        """)
        self.conn.commit(); print("Banco de dados criado")
        self.desconect_bd()
    def variaveis(self):
        self.palavras = self.palavra_ent.get()
        self.tag = self.tag_ent.get()
    def add_palavra(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" INSERT INTO palavras (pal, tag)
        VALUES (?, ?)""", (self.palavras, self.tag))
        self.conn.commit()
        self.desconect_bd()
        self.select_lista()
        self.limpa_tela()
    def select_lista(self):
        self.list_pal.delete(*self.list_pal.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT pal,tag FROM palavras
            ORDER BY pal ASC;""")
        for i in lista:
            self.list_pal.insert("", END, values=i)
        self.desconect_bd()
    def clickduplo(self, event):
        self.limpa_tela()
        self.list_pal.selection()

        for n in self.list_pal.selection():
            col1, col2 = self.list_pal.item(n, 'values')
            self.palavra_ent.insert(END, col1)
            self.tag_ent.insert(END, col2)
    def deleta_pal(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM palavras WHERE pal = ? """, (self.palavras,))
        self.conn.commit()
        self.desconect_bd()
        self.limpa_tela()
        self.select_lista()
    def aleatoria(self):
        self.conecta_bd()
        self.cursor.execute(""" SELECT pal,tag FROM palavras ORDER BY RANDOM() LIMIT 1""")
        resultado = self.cursor.fetchone()
        self.desconect_bd()
        if resultado:
            self.limpa_tela()
            self.palavra_escolhida = resultado[0]
            self.tag_escolhida = resultado [1]
            self.tamanho_palavra = len(self.palavra_escolhida)
            self.lb_tamanho.config(text=f"A palavra escolhida tem {self.tamanho_palavra} letras")
            self.lb_categoria.config(text=f"A palavra escolhida pertence a categoria {self.tag_escolhida}")
#front-end
class Application(Funcs):
    def __init__(self):
        #Selfs
        self.tamanho_palavra = 0
        self.vidas = 6
        self.contador = 0
        self.janela = janela
        self.tela()
        self.frames()
        self.widgets_1()
        self.widgets_2()
        self.list_frame2()
        self.montaTabela()
        self.select_lista()
        self.aleatoria()
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
    def atualizar_vidas(self):
        self.lb_vidas.config(text=f"Voce tem {self.vidas} vidas restantes")
    def widgets_1(self):
        #Botao Adicionar

        self.bt_add = Button(self.frame_1,text="Adicionar",bd=4,font= ('Courier', 8,'bold'),command=self.add_palavra)
        self.bt_add.place(relx=0.2,rely=0.11,relwidth=0.1,relheight=0.1)

        #Apagar palavra

        self.bt_apaga = Button(self.frame_1, text="Apagar", bd=4, font= ('Courier', 8, 'bold'), command=self.deleta_pal)
        self.bt_apaga.place(relx=0.2, rely=0.41,relwidth=0.1, relheight=0.1)

        #Palavra Aleatoria

        self.bt_random = Button(self.frame_1, text="Aleatoria", bd=4,font= ('Courier', 8,'bold'), command=self.aleatoria)
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

        #Vidas

        self.lb_vidas = Label(self.frame_1, text=f"Voce tem {self.vidas} Vidas restantes",bg='#d4e8ed')
        self.lb_vidas.place(relx = 0.5, rely = 0.01)

        #Tamanho das palavras

        self.lb_tamanho = Label(self.frame_1, text=f"A palavra escolhida tem ? letras", bg='#d4e8ed')
        self.lb_tamanho.place(relx = 0.5, rely = 0.2)

        #Tag da palavra

        self.lb_categoria = Label(self.frame_1, text=f"A palavra escolhida pertence a categoria ?", bg='#d4e8ed')
        self.lb_categoria.place(relx = 0.5, rely = 0.3)

        #Quantas letras foram acertadas

        self.lb_acertos = Label(self.frame_1, text=f"Voce acertou ? palavras ate o momento, a palavra agora tem ? letras", bg='#d4e8ed')
        self.lb_acertos.place(relx = 0.5, rely = 0.4)
    def widgets_2(self):
        def limit_cr(*args):
            entrada = texto.get()
            if len(entrada) > 1:
                texto.set(entrada[0])
        #Tentar
        self.bt_try = Button(self.frame_2, text="Tentar", bd=4,font= ('Times', 8,'bold'), command=self.tentar_letra)
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

        self.list_pal = ttk.Treeview(self.frame_2, height=3, columns=("col1","col2"))
        self.list_pal.heading("#0", text="")
        self.list_pal.heading("#1", text="Palavra")
        self.list_pal.heading("#2", text="Tag")
        #self.list_pal.heading("#3", text="Acertos")

        #Define padrão

        self.list_pal.column("#0",width=0, stretch=NO)
        self.list_pal.column("#1",width=50)
        self.list_pal.column("#2", width=50)
        #self.list_pal.column("#3",width=160)
        #self.list_pal.column("#4",width=160)

        #Define proporção

        self.list_pal.place(relx=0.15,rely=0.01,relwidth=0.81,relheight=0.85)

        #Define Scroll

        self.scroolList = Scrollbar(self.frame_2,orient='vertical')
        self.list_pal.configure(yscrollcommand=self.scroolList.set)
        self.scroolList.place(relx=0.96,rely=0.01,relwidth=0.04,relheight=0.85)
        self.list_pal.bind("<Double-1>", self.clickduplo)
    def tentar_letra(self):
        self.letra_tentada = self.try_ent.get().lower()
        if self.letra_tentada in self.palavra_escolhida:
            self.lb_acertos.config(text=f"Voce acertou a letra {self.letra_tentada}")
            self.contador += self.palavra_escolhida.count(self.letra_tentada)
            self.lb_acertos.config(text=f"Voce acertou {self.contador} letras ate o momento")

        else:
            self.vidas -= 1
            self.atualizar_vidas()
        if self.vidas == 0:
            self.limpa_tela()
            self.aleatoria()
            self.vidas = 6
        if self.contador == self.tamanho_palavra:
            self.lb_acertos.config(text=f"Parabens! Voce acertou a palavra inteira, que era {self.palavra_escolhida}")
            self.contador = 0


Application()