import pygame
import math

pygame.init()

screen = pygame.display.set_mode((1000, 700))
canvas = pygame.Surface((1000, 700))
clock = pygame.time.Clock()

screen.fill("white")
canvas.fill("white")
# ------------------------------
# CARREGAR ICONES
# ------------------------------

icone_reta = pygame.image.load("icons/reta.png")
icone_circulo = pygame.image.load("icons/circulo.png")
icone_livre = pygame.image.load("icons/livre.png")
icone_limpar = pygame.image.load("icons/delete.png")

icone_reta = pygame.transform.scale(icone_reta, (24, 24))
icone_circulo = pygame.transform.scale(icone_circulo, (24, 24))
icone_livre = pygame.transform.scale(icone_livre, (24, 24))
icone_limpar = pygame.transform.scale(icone_limpar, (24, 24))


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


def dda(vertice_inicial, vertice_final, cor):
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


def bres_generico(vertice_inicial, vertice_final, cor):
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


def bres_circun(vertice_inicial, vertice_final, cor):
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


# ------------------------------
# ESTADO
# ------------------------------

vertices = []
cor = "black"

ferramenta = "livre"
algoritmo_reta = "dda"

menu_reta = False
pos_anterior = None

# ------------------------------
# BOTÕES
# ------------------------------

menu = pygame.Rect(0, 0, 1000, 70)

btn_reta = Botao(20, 10, 50, 50, icone_reta)
btn_circulo = Botao(90, 10, 50, 50, icone_circulo)
btn_livre = Botao(160, 10, 50, 50, icone_livre)
btn_limpar = Botao(230, 10, 50, 50, icone_limpar)

btn_dda = Botao(20, 70, 80, 40)
btn_bres = Botao(20, 110, 80, 40)

fonte = pygame.font.SysFont("Arial", 16)

# ------------------------------
# LOOP
# ------------------------------

running = True

while running:

    mouse = pygame.mouse.get_pos()

    btn_reta.hover_check(mouse)
    btn_circulo.hover_check(mouse)
    btn_livre.hover_check(mouse)
    btn_limpar.hover_check(mouse)

    btn_dda.hover_check(mouse)
    btn_bres.hover_check(mouse)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            # CLIQUE NO MENU
            if menu.collidepoint(event.pos):

                if btn_reta.clicado(event.pos):
                    ferramenta = "reta"
                    menu_reta = not menu_reta

                elif btn_circulo.clicado(event.pos):
                    ferramenta = "circulo"
                    menu_reta = False

                elif btn_livre.clicado(event.pos):
                    ferramenta = "livre"
                    menu_reta = False

                elif btn_limpar.clicado(event.pos):
                    canvas.fill("white")

                vertices.clear()
                continue

            # MENU DE ALGORITMO
            if menu_reta:

                if btn_dda.clicado(event.pos):
                    algoritmo_reta = "dda"
                    menu_reta = False
                    continue

                if btn_bres.clicado(event.pos):
                    algoritmo_reta = "bres"
                    menu_reta = False
                    continue

            # AREA DE DESENHO
            if ferramenta != "livre":

                vertices.append(event.pos)

                if len(vertices) == 2:

                    if ferramenta == "reta":

                        if algoritmo_reta == "dda":
                            dda(vertices[0], vertices[1], cor)

                        elif algoritmo_reta == "bres":
                            bres_generico(vertices[0], vertices[1], cor)

                    elif ferramenta == "circulo":

                        bres_circun(vertices[0], vertices[1], cor)

                    vertices.clear()

    # ------------------------------
    # RENDER
    # ------------------------------
    screen.fill("white")
    screen.blit(canvas, (0, 0))

    pygame.draw.rect(screen, (40, 42, 45), menu)

    btn_reta.desenhar(screen, ferramenta == "reta")
    btn_circulo.desenhar(screen, ferramenta == "circulo")
    btn_livre.desenhar(screen, ferramenta == "livre")
    btn_limpar.desenhar(screen)

    if menu_reta:
        btn_dda.desenhar(screen, algoritmo_reta == "dda")
        btn_bres.desenhar(screen, algoritmo_reta == "bres")

        txt1 = fonte.render("DDA", True, (255, 255, 255))
        txt2 = fonte.render("Bres", True, (255, 255, 255))

        screen.blit(txt1, txt1.get_rect(center=btn_dda.rect.center))
        screen.blit(txt2, txt2.get_rect(center=btn_bres.rect.center))

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
