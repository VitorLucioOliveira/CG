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

        v1 = (round(reta["v1"][0]), round(reta["v1"][1]))
        v2 = (round(reta["v2"][0]), round(reta["v2"][1]))

        if reta["tipo"] == "reta":
            if algoritmo_reta == "dda":
                dda(v1, v2)

            else:
                bres_generico(v1, v2)

        elif reta["tipo"] == "circulo":
            bres_circun(v1, v2)

def aplicar_transformacao():
    global retas

    try:
        # centro da tela (ponto de referência)
        cx = screen.get_width() / 2
        cy = screen.get_height() / 2

        for reta in retas:

            x1, y1 = reta["v1"]
            x2, y2 = reta["v2"]

            # -------------------------
            # 1. MOVER PARA ORIGEM
            # -------------------------
            x1 -= cx
            y1 -= cy
            x2 -= cx
            y2 -= cy

            # -------------------------
            # 2. APLICAR TRANSFORMAÇÃO
            # -------------------------

            if tipo_transformacao == "translacao":

                dx, dy = map(float, input_texto.split(","))
                x1 += dx
                y1 += dy
                x2 += dx
                y2 += dy

            elif tipo_transformacao == "escala":

                sx, sy = map(float, input_texto.split(","))
                x1 *= sx
                y1 *= sy
                x2 *= sx
                y2 *= sy

            elif tipo_transformacao == "rotacao":

                ang = math.radians(float(input_texto))

                nx1 = x1 * math.cos(ang) - y1 * math.sin(ang)
                ny1 = x1 * math.sin(ang) + y1 * math.cos(ang)

                nx2 = x2 * math.cos(ang) - y2 * math.sin(ang)
                ny2 = x2 * math.sin(ang) + y2 * math.cos(ang)

                x1, y1 = nx1, ny1
                x2, y2 = nx2, ny2

            elif tipo_transformacao == "reflexao":

                modo = input_texto.lower()

                if modo == "x":
                    y1 = -y1
                    y2 = -y2

                elif modo == "y":
                    x1 = -x1
                    x2 = -x2

                elif modo == "xy":
                    x1 = -x1
                    y1 = -y1
                    x2 = -x2
                    y2 = -y2

            # -------------------------
            # 3. VOLTAR PARA TELA
            # -------------------------
            x1 += cx
            y1 += cy
            x2 += cx
            y2 += cy

            reta["v1"] = (x1, y1)
            reta["v2"] = (x2, y2)

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
tipo_transformacao = "rotacao"

menu_transforme = False
menu_reta = False
menu_janela= False

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


btn_dda = Botao(90, 75, 80, 40)
btn_bres = Botao(90, 120, 80, 40)

btn_lian = Botao(300, 75, 80, 40)
btn_cohen = Botao(300, 120, 80, 40)

btn_translacao = Botao(440, 75, 100, 40)
btn_escala = Botao(440, 120, 100, 40)
btn_rotacao = Botao(440, 165, 100, 40)
btn_reflexao = Botao(440, 210, 100, 40)

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
                    input_ativo = False

                elif btn_circulo.clicado(event.pos):
                    ferramenta = "circulo"
                    menu_reta = False
                    menu_janela = False
                    menu_transforme = False
                    input_ativo = False

                elif btn_livre.clicado(event.pos):
                    ferramenta = "livre"
                    menu_reta = False
                    menu_janela = False
                    menu_transforme = False
                    input_ativo = False

                elif btn_subtela.clicado(event.pos):
                    ferramenta = "subtela"
                    menu_reta = False
                    menu_janela = not menu_janela
                    menu_transforme = False
                    input_ativo = False

                elif btn_limpar.clicado(event.pos):
                    canvas.fill("white")
                    clipping_window = None
                    menu_reta = False
                    menu_janela = False
                    menu_transforme = False
                    input_ativo = False
                    retas.clear()

                elif btn_transforme.clicado(event.pos):
                    ferramenta = "transforme"
                    menu_reta = False
                    menu_janela = False
                    menu_transforme = not menu_transforme

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

                if len(vertices) == 2:

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

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
