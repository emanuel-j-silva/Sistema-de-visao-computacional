import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import cv2

def carregaImagens():
    img1 = Image.open('./imagens/padrao.jpeg')
    img1 = img1.resize((350, 262))
    img1 = ImageTk.PhotoImage(img1)
    e1 = tk.Label(root)
    e1.grid(row = 2, column = 0)
    e1.image = img1
    e1['image'] = img1

    img2 = Image.open('./imagens/peca.jpeg')
    img2 = img2.resize((350, 262))
    img2 = ImageTk.PhotoImage(img2)
    e2 = tk.Label(root)
    e2.grid(row = 2, column = 1)
    e2.image = img2
    e2['image'] = img2


def comparaImagens():
    # definir um limiar para aprovado
    limiar = 150000.0
    
    # carrega a imagem padrão e gera o histograma para comparação
    padrao = cv2.imread('./imagens/padrao.jpeg')
    padrao_cinza = cv2.cvtColor(padrao, cv2.COLOR_BGR2GRAY)
    padrao_histograma = cv2.calcHist ([padrao_cinza], [0], None, [256], [0, 256])

    # tira a foto da peca e gera o histograma para comparação
    cam = cv2.VideoCapture(0)
    return_value, image = cam.read()
    cv2.imwrite('./imagens/peca.jpeg', image)
    peca = cv2.imread('./imagens/peca.jpeg')
    peca_cinza = cv2.cvtColor(peca, cv2.COLOR_BGR2GRAY)
    peca_histograma = cv2.calcHist ([peca_cinza], [0], None, [256], [0, 256]) 

    # compara os dois histogramas gerados
    # verificação de qual algoritmo é mais eficiente
    print(cv2.compareHist(padrao_histograma, peca_histograma, cv2.HISTCMP_CORREL))
    print(cv2.compareHist(padrao_histograma, peca_histograma, cv2.HISTCMP_CHISQR))
    print(cv2.compareHist(padrao_histograma, peca_histograma, cv2.HISTCMP_INTERSECT))
    print(cv2.compareHist(padrao_histograma, peca_histograma, cv2.HISTCMP_BHATTACHARYYA))

    result = cv2.compareHist(padrao_histograma, peca_histograma, cv2.HISTCMP_CHISQR)

    if (result <= limiar):        
        l4.configure(text = 'APROVADA', fg = 'green')
    else:
        l4.configure(text = 'REPROVADA', fg = 'red')

    carregaImagens()

# janela principal
root = Tk()
root.title('Sistema de Visão')
window_width = 1280
window_height = 720

# verifica a dimensão da tela
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# verifica o centro da tela
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# posiciona a janela no centro da tela
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)

# divide a tela em duas colunas
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
# divide a tela em cinco linhas
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=3)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)

# configura fontes dos textos
font1 = ('times', 24, 'bold')
font2 = ('times', 17, 'bold')

# textos da tela principal
l1 = Label(root, text = 'SISTEMA DE VERIFICAÇÃO DE PEÇAS', font = font1)
l2 = Label(root, text = 'PEÇA PADRÃO', font = font1)
l3 = Label(root, text = 'PEÇA VERIFICADA', font = font1)
l4 = Label(root, text = 'INDEFINIDO', font = font2)

# posiciona o textos na tela
l1.grid(row = 0, column = 0, columnspan = 2)
l2.grid(row = 1, column = 0)
l3.grid(row = 1, column = 1)
l4.grid(row = 4, column = 0, columnspan = 2)

# botao para verificação
verificar = Button(root, text ="VERIFICAR", command = lambda:comparaImagens(), font = font2, fg = 'blue')
verificar.grid(row = 3, column = 0, columnspan = 2)
    
carregaImagens()

if __name__ == '__main__':
    root.mainloop()
