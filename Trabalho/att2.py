import pygame
import math
import sys
import os

pygame.init()

screen = pygame.display.set_mode((1000, 700))
canvas = pygame.Surface((1000, 700))
clock = pygame.time.Clock()

screen.fill("white")
canvas.fill("white")
# ------------------------------
# CARREGAR ICONES
# ------------------------------
def caminho_recurso(rel_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_path)

icone_reta = pygame.image.load(caminho_recurso("icons/reta.png"))
icone_circulo = pygame.image.load(caminho_recurso("icons/circulo.png"))
icone_livre = pygame.image.load(caminho_recurso("icons/livre.png"))
icone_limpar = pygame.image.load(caminho_recurso("icons/delete.png"))
icone_subtela = pygame.image.load(caminho_recurso("icons/subtela.png"))
icone_cor = pygame.image.load(caminho_recurso("icons/color.png"))
icone_transform = pygame.image.load(caminho_recurso("icons/transform.png"))

icone_reta = pygame.transform.scale(icone_reta, (24, 24))
icone_circulo = pygame.transform.scale(icone_circulo, (24, 24))
icone_livre = pygame.transform.scale(icone_livre, (24, 24))
icone_limpar = pygame.transform.scale(icone_limpar, (24, 24))
icone_transform = pygame.transform.scale(icone_transform, (24, 24))


# ------------------------------
# CLASSE BOTÃO
# ------------------------------

class Botao:

    def __init__(self, x, y, w, h, icone=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.icone = icone
        self.hover = False

    def desenhar(self, tela, ativo=False):

        cor_normal = (60, 63, 65)
        cor_hover = (90, 93, 95)
        cor_ativo = (0, 120, 215)

        cor = cor_normal

        if self.hover:
            cor = cor_hover

        if ativo:
            cor = cor_ativo

        pygame.draw.rect(tela, cor, self.rect, border_radius=8)

        if self.icone:
            rect_icon = self.icone.get_rect(center=self.rect.center)
            tela.blit(self.icone, rect_icon)

    def hover_check(self, pos):
        self.hover = self.rect.collidepoint(pos)

    def clicado(self, pos):
        return self.rect.collidepoint(pos)


# ------------------------------
# ALGORITMOS
# ------------------------------

def get_placeholder():

    if tipo_transformacao == "translacao":
        return "ex: 50,30"

    elif tipo_transformacao == "escala":
        return "ex: 2,2"

    elif tipo_transformacao == "rotacao":
        return "ex: 45°"

    elif tipo_transformacao == "reflexao":
        return "ex: x ou y ou xy"

    return ""
def redesenhar_canvas():

    canvas.fill("white")

    for reta in retas:

        if reta["tipo"] == "reta":
            v1 = (round(reta["v1"][0]), round(reta["v1"][1]))
            v2 = (round(reta["v2"][0]), round(reta["v2"][1]))
            if algoritmo_reta == "dda":
                dda(v1, v2)

            else:
                bres_generico(v1, v2)

        elif reta["tipo"] == "circulo":
            v1 = (round(reta["v1"][0]), round(reta["v1"][1]))
            v2 = (round(reta["v2"][0]), round(reta["v2"][1]))
            bres_circun(v1, v2)

        elif reta["tipo"] == "bezier":
            bezier_cubica(reta["pontos"])

        elif reta["tipo"] == "hermite":
            hermite(reta["pontos"])

def transformar_ponto(x, y, cx, cy):
    # 1. MOVER PARA A ORIGEM (transformações são feitas em torno do centro da tela)
    x -= cx
    y -= cy

    # 2. APLICAR A TRANSFORMAÇÃO ESCOLHIDA
    if tipo_transformacao == "translacao":
        dx, dy = map(float, input_texto.split(","))
        x += dx
        y += dy

    elif tipo_transformacao == "escala":
        sx, sy = map(float, input_texto.split(","))
        x *= sx
        y *= sy

    elif tipo_transformacao == "rotacao":
        ang = math.radians(float(input_texto))
        nx = x * math.cos(ang) - y * math.sin(ang)
        ny = x * math.sin(ang) + y * math.cos(ang)
        x, y = nx, ny

    elif tipo_transformacao == "reflexao":
        modo = input_texto.lower()
        if modo == "x":
            y = -y
        elif modo == "y":
            x = -x
        elif modo == "xy":
            x = -x
            y = -y

    # 3. VOLTAR PARA AS COORDENADAS DA TELA
    x += cx
    y += cy
    return (x, y)


def aplicar_transformacao():
    global retas

    try:
        # centro da tela (ponto de referência)
        cx = screen.get_width() / 2
        cy = screen.get_height() / 2

        for reta in retas:

            # objetos com vários pontos (curvas Bézier/Hermite)
            if "pontos" in reta:
                reta["pontos"] = [
                    transformar_ponto(px, py, cx, cy)
                    for (px, py) in reta["pontos"]
                ]

            # objetos com dois vértices (retas e círculos)
            else:
                x1, y1 = reta["v1"]
                x2, y2 = reta["v2"]
                reta["v1"] = transformar_ponto(x1, y1, cx, cy)
                reta["v2"] = transformar_ponto(x2, y2, cx, cy)

    except Exception as e:
        print(f"Erro na transformação: {e}")
        return

    redesenhar_canvas()

def colorir_simetricos(a, b, xc, yc, cor):
    canvas.set_at((a + xc, b + yc), cor)
    canvas.set_at((a + xc, -b + yc), cor)
    canvas.set_at((-a + xc, b + yc), cor)
    canvas.set_at((-a + xc, -b + yc), cor)
    canvas.set_at((b + xc, a + yc), cor)
    canvas.set_at((b + xc, -a + yc), cor)
    canvas.set_at((-b + xc, a + yc), cor)
    canvas.set_at((-b + xc, -a + yc), cor)


def get_coordenadas(vertice):
    x = int(vertice[0])
    y = int(vertice[1])
    return x, y


def dda(vertice_inicial, vertice_final, cor="black"):
    x_inicial, y_inicial = get_coordenadas(vertice_inicial)
    x_final, y_final = get_coordenadas(vertice_final)

    delta_x = x_final - x_inicial
    delta_y = y_final - y_inicial

    canvas.set_at((x_inicial, y_inicial), cor)
    canvas.set_at((x_final, y_final), cor)

    passo = max(abs(delta_x), abs(delta_y))

    if passo == 0:
        canvas.set_at((x_inicial, y_inicial), cor)
        return

    x_incr = delta_x / passo
    y_incr = delta_y / passo

    for i in range(passo):
        x_inicial += x_incr
        y_inicial += y_incr
        canvas.set_at((int(x_inicial), int(y_inicial)), cor)


def bres_generico(vertice_inicial, vertice_final, cor="black"):
    x, y = get_coordenadas(vertice_inicial)
    x_final, y_final = get_coordenadas(vertice_final)

    delta_x = x_final - x
    delta_y = y_final - y

    canvas.set_at((x, y), cor)

    if delta_x >= 0:
        x_incr = 1
    else:
        x_incr = -1
        delta_x = -delta_x

    if delta_y >= 0:
        y_incr = 1
    else:
        y_incr = -1
        delta_y = -delta_y

    if delta_x > delta_y:

        passo = (2 * delta_y) - delta_x
        const1 = 2 * delta_y
        const2 = 2 * (delta_y - delta_x)

        for i in range(delta_x):

            x += x_incr

            if passo < 0:
                passo += const1
            else:
                passo += const2
                y += y_incr

            canvas.set_at((x, y), cor)

    else:

        passo = (2 * delta_x) - delta_y
        const1 = 2 * delta_x
        const2 = 2 * (delta_x - delta_y)

        for i in range(delta_y):

            y += y_incr

            if passo < 0:
                passo += const1
            else:
                passo += const2
                x += x_incr

            canvas.set_at((x, y), cor)


def bres_circun(vertice_inicial, vertice_final, cor="black"):
    x_centro, y_centro = get_coordenadas(vertice_inicial)
    x_final, y_final = get_coordenadas(vertice_final)

    raio = int(math.sqrt((x_final - x_centro) ** 2 + (y_final - y_centro) ** 2))

    x = 0
    y = raio
    passo = 3 - (2 * raio)

    colorir_simetricos(x, y, x_centro, y_centro, cor)

    while x < y:

        if passo < 0:
            passo += (4 * x) + 6
        else:
            passo += (4 * (x - y)) + 10
            y -= 1

        x += 1
        colorir_simetricos(x, y, x_centro, y_centro, cor)

def aplicar_clipping():

    canvas.fill("white")

    for reta in retas:

        x1,y1 = reta["v1"]
        x2,y2 = reta["v2"]

        if reta["tipo"] == "reta":
            if algoritmo_janela == "cohen":
                cohen_sutherland(x1,y1,x2,y2)
            else:
                lian_barsky(x1,y1,x2,y2)

def get_codigo(x,y):

    codigo = 0

    if x < clipping_window["xmin"]:# esquerda
        codigo += 1
    if x > clipping_window["xmax"]: # direita
        codigo += 2
    if y < clipping_window["ymin"]:# abaixo
        codigo += 4
    if y > clipping_window["ymax"]: # acima
        codigo += 8

    return codigo

def cohen_sutherland(xA, yA, xB, yB):

    feito = False  # Tem calculo pra fazer
    aceite = False # Tem algo pra axibir

    xmin = clipping_window["xmin"]
    ymax = clipping_window["ymax"]
    ymin = clipping_window["ymin"]
    xmax = clipping_window["xmax"]

    x = y = 0

    codA = codB = codTemp = 0

    while not feito: # Não termina os calculos

        codA = get_codigo(xA,yA)
        codB = get_codigo(xB,yB)


        if codA == 0 and codB==0: # Ta tudo dentro da janela
            feito = aceite = True

        elif (codA & codB) != 0: # Ta tudo fora da janela
            feito = True

        else: # Tem algo dentro que deve ser calculado

            if codA != 0:
                codTemp = codA
            else:
                codTemp = codB

            #esquerda
            if ((codTemp >> 0) & 1) == 1:
                x = xmin
                y = yA + (yB-yA) * ((xmin - xA)/(xB-xA))

            #direita
            elif ((codTemp >> 1) & 1) == 1:
                x = xmax
                y = yA + (yB-yA) * ((xmax-xA)/(xB-xA))

            #inferior
            elif ((codTemp >> 2) & 1) == 1:
                y = ymin
                x = xA + (xB -xA) * ((ymin -yA)/(yB-yA))

            #superior
            elif ((codTemp >> 3) & 1) == 1:
                y = ymax
                x = xA + (xB - xA) * ((ymax - yA) / (yB - yA))

            if codTemp == codA:
                xA=x
                yA=y
            else:
                xB = x
                yB =y

    if aceite:
        if algoritmo_reta == "dda":
            dda((round(xA), round(yA)), (round(xB),round(yB)))
        else:
            bres_generico((round(xA), round(yA)), (round(xB),round(yB)))

def cliptest(p,q, u):

    resultado = True

    if p < 0: #Dentro do plano

        r = q/p
        if r> u[1]:
            resultado = False
        elif r > u[0]:
            u[0] = r

    elif p>0: # Fora do plano

        r =q/p
        if r < u[0]:
            resultado = False
        elif r < u[1]:
            u[1] = r

    elif q < 0 :
        resultado = False

    return resultado

def lian_barsky(x1,y1,x2,y2):

    u = [0.0 , 1] # u1 e u2, python nao tem ponteiro
    dx = x2 - x1
    dy= y2 - y1

    xmin = clipping_window["xmin"]
    ymax = clipping_window["ymax"]
    ymin = clipping_window["ymin"]
    xmax = clipping_window["xmax"]


    if(cliptest((-dx),x1-xmin, u)): #esq
        if (cliptest(dx, xmax - x1, u)):  # dir
            if (cliptest((-dy), y1 - ymin, u)):  # inf
                if (cliptest(dy, ymax - y1, u)):  # sup

                    if u[1] < 1.0:
                        x2 = x1 + u[1] * dx
                        y2 = y1 + u[1] * dy

                    if u[0] > 0.0:
                        x1 = x1 + u[0] * dx
                        y1 = y1 + u[0] * dy

                    if algoritmo_reta == "dda":
                        dda((round(x1), round(y1)), (round(x2), round(y2)))
                    else:
                        bres_generico((round(x1), round(y1)), (round(x2), round(y2)))



# ------------------------------
# CURVAS PARAMÉTRICAS
# ------------------------------
# Quanto maior o número de subdivisões (NUM_PASSOS), mais suave fica a curva,
# pois os segmentos de reta ficam menores e mais próximos do traçado ideal.

NUM_PASSOS = 200       # quantidade de subdivisões usadas para amostrar a curva
ESCALA_TANGENTE = 3.0  # fator que dá "força" às tangentes de Hermite.
                       # Sem ele, a tangente (guia - ponto) fica fraca e a curva
                       # quase não dobra (parece uma reta). O fator 3 é a mesma
                       # relação usada na conversão Bézier <-> Hermite e faz a
                       # curva se curvar de forma visível, sem mudar os extremos.


def pontos_curva_bezier(pontos):
    """
    Calcula e RETORNA a lista de pontos (x, y) de uma Bézier CÚBICA.
    """
    p0, p1, p2, p3 = pontos
    saida = []

    for i in range(NUM_PASSOS + 1):
        t = i / NUM_PASSOS      # t vai de 0.0 até 1.0
        u = 1 - t               # (1 - t), usado várias vezes

        # polinômios de Bernstein de grau 3 (os "pesos" de cada ponto)
        b0 = u ** 3
        b1 = 3 * (u ** 2) * t
        b2 = 3 * u * (t ** 2)
        b3 = t ** 3

        x = b0 * p0[0] + b1 * p1[0] + b2 * p2[0] + b3 * p3[0]
        y = b0 * p0[1] + b1 * p1[1] + b2 * p2[1] + b3 * p3[1]
        saida.append((x, y))

    return saida


def pontos_curva_hermite(pontos):
    """
    Calcula e RETORNA a lista de pontos (x, y) de uma curva de HERMITE.
    """
    p0, p1, guia0, guia1 = pontos

    # vetores tangentes definidos pelos pontos-guia (com fator de força)
    t0 = ((guia0[0] - p0[0]) * ESCALA_TANGENTE,
          (guia0[1] - p0[1]) * ESCALA_TANGENTE)
    t1 = ((guia1[0] - p1[0]) * ESCALA_TANGENTE,
          (guia1[1] - p1[1]) * ESCALA_TANGENTE)

    saida = []

    for i in range(NUM_PASSOS + 1):
        t = i / NUM_PASSOS  # parâmetro t de 0.0 a 1.0
        t2 = t * t          # t^2
        t3 = t2 * t         # t^3

        # funções de mistura (blending functions) de Hermite
        h00 = 2 * t3 - 3 * t2 + 1
        h10 = t3 - 2 * t2 + t
        h01 = -2 * t3 + 3 * t2
        h11 = t3 - t2

        x = h00 * p0[0] + h10 * t0[0] + h01 * p1[0] + h11 * t1[0]
        y = h00 * p0[1] + h10 * t0[1] + h01 * p1[1] + h11 * t1[1]
        saida.append((x, y))

    return saida


def _desenhar_amostra(pontos_amostrados, cor):
    """Liga os pontos amostrados da curva usando o DDA (traço final no canvas)."""
    anterior = None
    for (x, y) in pontos_amostrados:
        atual = (round(x), round(y))
        if anterior is not None:
            dda(anterior, atual, cor)  # curva contínua, sem buracos
        anterior = atual


def bezier_cubica(pontos, cor="black"):
    """Desenha a Bézier cúbica no canvas. NÃO usa funções prontas (.bezier())."""
    _desenhar_amostra(pontos_curva_bezier(pontos), cor)


def hermite(pontos, cor="black"):
    """Desenha a curva de Hermite no canvas. NÃO usa funções prontas (.hermite())."""
    _desenhar_amostra(pontos_curva_hermite(pontos), cor)


# ------------------------------
# ORIENTAÇÃO VISUAL DA CONSTRUÇÃO
# ------------------------------
# Cores usadas só na orientação enquanto a curva está sendo construída.
COR_PREVIA = (0, 120, 215)       # azul: prévia da curva
COR_GUIA = (150, 150, 150)       # cinza: polígono de controle / tangentes
COR_PONTO = (220, 50, 50)        # vermelho: pontos já clicados
COR_PONTO_MOUSE = (0, 170, 90)   # verde: ponto que está sendo posicionado


def desenhar_guia_curva(mouse_pos):
    """
      - texto dizendo qual ponto clicar agora;
      - marcadores coloridos e rotulados dos pontos já clicados;
      - polígono de controle (Bézier) ou linhas de tangente (Hermite);
      - prévia da curva acompanhando o mouse antes do último clique.
    """
    if algoritmo_curva == "bezier":
        rotulos = ["P0", "P1", "P2", "P3"]
        instrucoes = [
            "Bezier: clique P0 (inicio da curva)",
            "Bezier: clique P1 (ponto de controle)",
            "Bezier: clique P2 (ponto de controle)",
            "Bezier: clique P3 (fim da curva)",
        ]
    else:
        rotulos = ["P0", "P1", "T0", "T1"]
        instrucoes = [
            "Hermite: clique P0 (inicio)",
            "Hermite: clique P1 (fim)",
            "Hermite: clique a guia da tangente em P0",
            "Hermite: clique a guia da tangente em P1",
        ]

    n = len(vertices)

    # 1) Texto de instrução (qual ponto clicar agora)
    if n < 4:
        msg = fonte.render(instrucoes[n], True, (0, 0, 0))
        fundo = pygame.Rect(10, 78, msg.get_width() + 16, 26)
        pygame.draw.rect(screen, (255, 255, 230), fundo, border_radius=6)
        pygame.draw.rect(screen, (0, 0, 0), fundo, 1, border_radius=6)
        screen.blit(msg, (fundo.x + 8, fundo.y + 4))

    # Pontos da prévia: o que já foi clicado + o mouse no lugar dos que faltam.
    previa = list(vertices)
    while len(previa) < 4:
        previa.append(mouse_pos)

    # 2) Linhas auxiliares (polígono de controle OU tangentes)
    if algoritmo_curva == "bezier":
        # polígono de controle: liga P0-P1-P2-P3
        pygame.draw.lines(screen, COR_GUIA, False,
                          [(int(p[0]), int(p[1])) for p in previa], 1)
    else:
        # tangentes: P0 -> guia0 e P1 -> guia1
        p0, p1, g0, g1 = previa
        pygame.draw.line(screen, COR_GUIA,
                         (int(p0[0]), int(p0[1])), (int(g0[0]), int(g0[1])), 1)
        pygame.draw.line(screen, COR_GUIA,
                         (int(p1[0]), int(p1[1])), (int(g1[0]), int(g1[1])), 1)

    # 3) Prévia da curva (azul, suavizada) usando os MESMOS cálculos do traço final
    if algoritmo_curva == "bezier":
        amostra = pontos_curva_bezier(previa)
    else:
        amostra = pontos_curva_hermite(previa)
    amostra = [(int(x), int(y)) for (x, y) in amostra]
    if len(amostra) >= 2:
        pygame.draw.aalines(screen, COR_PREVIA, False, amostra)

    # 4) Marcadores dos pontos já clicados (vermelho) + rótulo
    for i, p in enumerate(vertices):
        px, py = int(p[0]), int(p[1])
        pygame.draw.circle(screen, COR_PONTO, (px, py), 5)
        pygame.draw.circle(screen, (255, 255, 255), (px, py), 5, 1)
        screen.blit(fonte.render(rotulos[i], True, COR_PONTO), (px + 8, py - 8))

    # 5) Marcador do próximo ponto, acompanhando o mouse (verde)
    if n < 4:
        mx, my = int(mouse_pos[0]), int(mouse_pos[1])
        pygame.draw.circle(screen, COR_PONTO_MOUSE, (mx, my), 5)
        pygame.draw.circle(screen, (255, 255, 255), (mx, my), 5, 1)
        screen.blit(fonte.render(rotulos[n], True, COR_PONTO_MOUSE), (mx + 8, my - 8))




# ------------------------------
# ESTADO
# ------------------------------
retas = []
vertices = []
cor = "black"

input_ativo = False
input_texto = ""

ferramenta = "livre"
algoritmo_reta = "dda"
algoritmo_janela = "cohen"
algoritmo_curva = "bezier"
tipo_transformacao = "rotacao"

menu_transforme = False
menu_reta = False
menu_janela= False
menu_curva = False

pos_anterior = None
clipping_window = None


# ------------------------------
# BOTÕES
# ------------------------------

menu = pygame.Rect(0, 0, 1000, 70)

btn_cor = Botao(20, 10, 50, 50, icone_cor)
btn_reta = Botao(90, 10, 50, 50, icone_reta)
btn_circulo = Botao(160, 10, 50, 50, icone_circulo)
btn_livre = Botao(230, 10, 50, 50, icone_livre)
btn_subtela = Botao(300, 10, 50, 50, icone_subtela)
btn_limpar = Botao(370, 10, 50, 50, icone_limpar)
btn_transforme = Botao(440, 10, 50, 50, icone_transform)
# botão de curva: sem ícone (usa rótulo de texto "Curva"), posicionado à
# direita da caixa de entrada de transformações (que termina em x≈660)
btn_curva = Botao(670, 10, 60, 50)


btn_dda = Botao(90, 75, 80, 40)
btn_bres = Botao(90, 120, 80, 40)

btn_lian = Botao(300, 75, 80, 40)
btn_cohen = Botao(300, 120, 80, 40)

btn_translacao = Botao(440, 75, 100, 40)
btn_escala = Botao(440, 120, 100, 40)
btn_rotacao = Botao(440, 165, 100, 40)
btn_reflexao = Botao(440, 210, 100, 40)

# submenu de curvas: escolher entre Bézier e Hermite
btn_bezier = Botao(670, 75, 90, 40)
btn_hermite = Botao(670, 120, 90, 40)

fonte = pygame.font.SysFont("Arial", 16)
transform_rect = pygame.Rect(btn_transforme.rect.right + 10, 15, 160, 35)
# ------------------------------
# LOOP
# ------------------------------

running = True

while running:

    mouse = pygame.mouse.get_pos()

    # hover check
    btn_reta.hover_check(mouse)
    btn_circulo.hover_check(mouse)
    btn_livre.hover_check(mouse)
    btn_limpar.hover_check(mouse)
    btn_cor.hover_check(mouse)
    btn_subtela.hover_check(mouse)
    btn_transforme.hover_check(mouse)

    btn_dda.hover_check(mouse)
    btn_bres.hover_check(mouse)

    btn_lian.hover_check(mouse)
    btn_cohen.hover_check(mouse)

    btn_translacao.hover_check(mouse)
    btn_rotacao.hover_check(mouse)
    btn_escala.hover_check(mouse)
    btn_reflexao.hover_check(mouse)

    btn_curva.hover_check(mouse)
    btn_bezier.hover_check(mouse)
    btn_hermite.hover_check(mouse)


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and input_ativo:
            menu_transforme = False
            if event.key == pygame.K_RETURN:

                aplicar_transformacao()


            elif event.key == pygame.K_BACKSPACE:

                input_texto = input_texto[:-1]

            else:

                input_texto += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:

            # CLIQUE NO MENU
            if menu.collidepoint(event.pos):

                if btn_reta.clicado(event.pos):
                    ferramenta = "reta"
                    menu_reta = not menu_reta
                    menu_janela = False
                    menu_transforme = False
                    menu_curva = False
                    input_ativo = False

                elif btn_circulo.clicado(event.pos):
                    ferramenta = "circulo"
                    menu_reta = False
                    menu_janela = False
                    menu_transforme = False
                    menu_curva = False
                    input_ativo = False

                elif btn_livre.clicado(event.pos):
                    ferramenta = "livre"
                    menu_reta = False
                    menu_janela = False
                    menu_transforme = False
                    menu_curva = False
                    input_ativo = False

                elif btn_subtela.clicado(event.pos):
                    ferramenta = "subtela"
                    menu_reta = False
                    menu_janela = not menu_janela
                    menu_transforme = False
                    menu_curva = False
                    input_ativo = False

                elif btn_limpar.clicado(event.pos):
                    canvas.fill("white")
                    clipping_window = None
                    menu_reta = False
                    menu_janela = False
                    menu_transforme = False
                    menu_curva = False
                    input_ativo = False
                    retas.clear()

                elif btn_transforme.clicado(event.pos):
                    ferramenta = "transforme"
                    menu_reta = False
                    menu_janela = False
                    menu_curva = False
                    menu_transforme = not menu_transforme

                elif btn_curva.clicado(event.pos):
                    ferramenta = "curva"
                    menu_reta = False
                    menu_janela = False
                    menu_transforme = False
                    menu_curva = not menu_curva
                    input_ativo = False

                vertices.clear()
                continue

            # MENU DE ALGORITMO RETA
            if menu_reta:

                if btn_dda.clicado(event.pos):
                    algoritmo_reta = "dda"
                    menu_reta = False
                    continue


                if btn_bres.clicado(event.pos):
                    algoritmo_reta = "bres"
                    menu_reta = False
                    continue
                vertices.clear()

            # MENU DE ALGORITMO JANELA
            if menu_janela:

                if btn_cohen.clicado(event.pos):
                    algoritmo_janela = "cohen"
                    menu_janela = False
                    continue

                if btn_lian.clicado(event.pos):
                    algoritmo_janela = "lian"
                    menu_janela = False
                    continue
                vertices.clear()

            # MENU DE ALGORITMO CURVA
            if menu_curva:

                if btn_bezier.clicado(event.pos):
                    algoritmo_curva = "bezier"
                    menu_curva = False
                    continue

                if btn_hermite.clicado(event.pos):
                    algoritmo_curva = "hermite"
                    menu_curva = False
                    continue
                vertices.clear()



            # MENU DE ALGORITMO TRANSFORMAÇÃO
            if menu_transforme:

                if btn_translacao.clicado(event.pos):

                    tipo_transformacao = "translacao"
                    input_texto = ""
                    input_ativo = True

                elif btn_escala.clicado(event.pos):

                    tipo_transformacao = "escala"
                    input_texto = ""
                    input_ativo = True

                elif btn_rotacao.clicado(event.pos):

                    tipo_transformacao = "rotacao"
                    input_texto = ""
                    input_ativo = True

                elif btn_reflexao.clicado(event.pos):

                    tipo_transformacao = "reflexao"
                    input_texto = ""
                    input_ativo = True

            # AREA DE DESENHO
            if ferramenta != "livre":

                vertices.append(event.pos)

                # curvas paramétricas precisam de 4 pontos (cliques)
                if ferramenta == "curva":

                    if len(vertices) == 4:

                        reta = {
                            "pontos": list(vertices),
                            "tipo": algoritmo_curva  # "bezier" ou "hermite"
                        }

                        retas.append(reta)  # salva os 4 pontos da curva

                        if algoritmo_curva == "bezier":
                            bezier_cubica(vertices, cor)
                        else:
                            hermite(vertices, cor)

                        vertices.clear()

                elif len(vertices) == 2:

                    if ferramenta == "reta":

                        reta = {
                            "v1": vertices[0],
                            "v2": vertices[1],
                            "tipo": "reta"
                        }

                        retas.append(reta) # Salva as coordenadas
                        if clipping_window is not None:
                            x1, y1 = get_coordenadas(vertices[0])
                            x2, y2 = get_coordenadas(vertices[1])

                            cohen_sutherland(x1, y1, x2, y2)

                        else:
                            if algoritmo_reta == "dda":
                                dda(vertices[0], vertices[1], cor)

                            elif algoritmo_reta == "bres":
                                bres_generico(vertices[0], vertices[1], cor)

                    elif ferramenta == "circulo":

                        reta = {
                            "v1": vertices[0],
                            "v2": vertices[1],
                            "tipo": "circulo"
                        }

                        retas.append(reta)  # Salva as coordenadas
                        bres_circun(vertices[0], vertices[1], cor)

                    elif ferramenta == "subtela":
                        x1, y1 = get_coordenadas(vertices[0])
                        x2, y2 = get_coordenadas(vertices[1])

                        clipping_window = {
                            "xmin": min(x1, x2),
                            "xmax": max(x1, x2),
                            "ymin": min(y1, y2),
                            "ymax": max(y1, y2)
                        }

                        aplicar_clipping()

                    vertices.clear()

    # ------------------------------
    # RENDER
    # ------------------------------
    screen.fill("white")
    screen.blit(canvas, (0, 0))

    pygame.draw.rect(screen, (40, 42, 45), menu)

    btn_cor.desenhar(screen)
    btn_reta.desenhar(screen, ferramenta == "reta")
    btn_circulo.desenhar(screen, ferramenta == "circulo")
    btn_livre.desenhar(screen, ferramenta == "livre")
    btn_subtela.desenhar(screen, ferramenta == "subtela")
    btn_limpar.desenhar(screen)
    btn_transforme.desenhar(screen, ferramenta == "transforme" )
    btn_curva.desenhar(screen, ferramenta == "curva")

    # rótulo de texto do botão de curva (não tem ícone)
    txt_curva = fonte.render("Curva", True, (255, 255, 255))
    screen.blit(txt_curva, txt_curva.get_rect(center=btn_curva.rect.center))




    if menu_reta:
        btn_dda.desenhar(screen, algoritmo_reta == "dda")
        btn_bres.desenhar(screen, algoritmo_reta == "bres")

        txt1 = fonte.render("DDA", True, (255, 255, 255))
        txt2 = fonte.render("Bres", True, (255, 255, 255))

        screen.blit(txt1, txt1.get_rect(center=btn_dda.rect.center))
        screen.blit(txt2, txt2.get_rect(center=btn_bres.rect.center))

    if menu_janela:
        btn_lian.desenhar(screen, algoritmo_janela == "lian")
        btn_cohen.desenhar(screen, algoritmo_janela == "cohen")

        txt3 = fonte.render("Lian", True, (255, 255, 255))
        txt4 = fonte.render("Cohen", True, (255, 255, 255))

        screen.blit(txt3, txt3.get_rect(center=btn_lian.rect.center))
        screen.blit(txt4, txt4.get_rect(center=btn_cohen.rect.center))

    if menu_curva:
        btn_bezier.desenhar(screen, algoritmo_curva == "bezier")
        btn_hermite.desenhar(screen, algoritmo_curva == "hermite")

        txt_bz = fonte.render("Bezier", True, (255, 255, 255))
        txt_hm = fonte.render("Hermite", True, (255, 255, 255))

        screen.blit(txt_bz, txt_bz.get_rect(center=btn_bezier.rect.center))
        screen.blit(txt_hm, txt_hm.get_rect(center=btn_hermite.rect.center))

    if clipping_window is not None:
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (
                clipping_window["xmin"],
                clipping_window["ymin"],
                clipping_window["xmax"] - clipping_window["xmin"],
                clipping_window["ymax"] - clipping_window["ymin"]
            ),
            2
        )

    if menu_transforme:
        btn_translacao.desenhar(screen, tipo_transformacao == "translacao")
        btn_escala.desenhar(screen, tipo_transformacao == "escala")
        btn_rotacao.desenhar(screen, tipo_transformacao == "rotacao")
        btn_reflexao.desenhar(screen, tipo_transformacao == "reflexao")

        txt5 = fonte.render("Trans", True, (255, 255, 255))
        txt6 = fonte.render("Escala", True, (255, 255, 255))
        txt7 = fonte.render("Rotação", True, (255, 255, 255))
        txt8 = fonte.render("Reflex", True, (255, 255, 255))

        screen.blit(txt5, txt5.get_rect(center=btn_translacao.rect.center))
        screen.blit(txt6, txt6.get_rect(center=btn_escala.rect.center))
        screen.blit(txt7, txt7.get_rect(center=btn_rotacao.rect.center))
        screen.blit(txt8, txt8.get_rect(center=btn_reflexao.rect.center))

    if input_ativo:
        pygame.draw.rect(screen, (255, 255, 255), transform_rect)
        pygame.draw.rect(screen, (0, 0, 0), transform_rect, 2)

        if input_texto == "":
            placeholder = fonte.render(get_placeholder(), True, (180, 180, 180))
            screen.blit(placeholder, (transform_rect.x + 8, transform_rect.y + 8))
        else:
            texto = fonte.render(input_texto, True, (0, 0, 0))
            screen.blit(texto, (transform_rect.x + 8, transform_rect.y + 8))
    # ------------------------------
    # DESENHO LIVRE
    # ------------------------------

    mouse_click = pygame.mouse.get_pressed()
    pos_atual = pygame.mouse.get_pos()

    if mouse_click[0]:

        if ferramenta == "livre" and not menu.collidepoint(pos_atual):

            if pos_anterior is not None:
                pygame.draw.line(canvas, cor, pos_anterior, pos_atual, 3)

            pos_anterior = pos_atual

    else:
        pos_anterior = None

    # orientação visual da construção da curva (overlay sobre a tela)
    if ferramenta == "curva":
        desenhar_guia_curva(mouse)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()