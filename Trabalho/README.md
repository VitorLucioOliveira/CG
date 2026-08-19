# 🖥️ Aplicação de Computação Gráfica 2D

## 📌 Descrição

Este projeto foi desenvolvido como parte da disciplina de Computação Gráfica e tem como objetivo implementar algoritmos fundamentais de gráficos 2D, incluindo:

- Transformações geométricas
- Rasterização de retas e circunferências
- Recorte de linhas
- Curvas paramétricas

A aplicação utiliza interface gráfica baseada em pixels, conforme especificado no trabalho.

---

## 🎯 Funcionalidades Implementadas

### 🔹 Transformações 2D
- Translação
- Escala
- Rotação
- Reflexão (X, Y, origem)

### 🔹 Rasterização
- Retas:
  - DDA
  - Bresenham
- Circunferência:
  - Bresenham

### 🔹 Recorte
- Cohen-Sutherland
- Liang-Barsky

### 🔹 Curvas Paramétricas
- Bézier cúbica
- Hermite

---

## 🖱️ Interface e Botões

A aplicação possui um menu superior com ferramentas interativas:

### 🎨 Cor
Seleciona a cor de desenho (atualmente padrão: preto).

---

### 📏 Reta
Permite desenhar retas clicando em dois pontos.

- Algoritmos disponíveis:
  - DDA
  - Bresenham

---

### ⚪ Círculo
Desenha uma circunferência a partir de dois pontos:
- Centro
- Ponto na borda (define o raio)

---

### ✏️ Livre
Modo de desenho livre com o mouse.

---

### 🧱 Subtela (Clipping)
Permite definir uma janela retangular para recorte.

- Algoritmos:
  - Cohen-Sutherland
  - Liang-Barsky

---

### 🗑️ Limpar
Limpa toda a área de desenho.

---

### 🔄 Transformações
Ativa o menu de transformações geométricas.

---

### 〰️ Curva
Desenha curvas paramétricas a partir de **4 cliques**.

- Algoritmos disponíveis:
  - Bézier cúbica
  - Hermite

Enquanto a curva é construída, a aplicação mostra uma **orientação visual em tempo real** (que some quando a curva é finalizada):

- texto indicando qual ponto clicar em seguida;
- pontos já clicados marcados em vermelho e rotulados;
- próximo ponto em verde, acompanhando o cursor;
- linhas auxiliares (polígono de controle na Bézier, linhas de tangente na Hermite);
- prévia da curva em azul, atualizada conforme o mouse se move.

---

## 🔧 Transformações Geométricas

Todas as transformações seguem o modelo:

1. Transladar objeto para a origem (centro da tela)
2. Aplicar transformação
3. Retornar para a posição original

---

### ➡️ Translação

Move o objeto no plano.

**Entrada:** dx,dy

**Exemplo:** 50,30

**Equação:** x' = x + dx  | y' = y + dy


---

### 🔍 Escala

Altera o tamanho do objeto.

**Entrada:** sx,sy

**Exemplo:** 2,2 → dobra o tamanho  | 0.5,0.5 → reduz pela metade

**Equação:** x' = x * sx | y' = y * sy


---

### 🔁 Rotação

Rotaciona o objeto em torno do centro.

**Entrada:** ângulo em graus

**Exemplo:** 45

**Equação:** x' = xcos(θ) - ysin(θ) | y' = xsin(θ) + ycos(θ)


---

### 🔄 Reflexão

Espelha o objeto em relação a um eixo.

**Entrada:** x → eixo X
y → eixo Y
origem → origem (0,0)


**Equações:**

- Eixo X: x' = x e y' = -y
- Eixo Y: x' = -x e y' = y

- Origem: x' = -x e y' = -y


---

## ✂️ Recorte de Linhas

### Cohen-Sutherland
- Utiliza códigos binários para determinar regiões
- Remove partes fora da janela

---

### Liang-Barsky
- Baseado em equação paramétrica
- Mais eficiente que Cohen-Sutherland

---

## 〰️ Curvas Paramétricas

Uma curva paramétrica descreve cada coordenada `(x, y)` em função de um único parâmetro `t`, que varia de `0` a `1`. Para `t = 0` estamos no início da curva e para `t = 1` no fim.

O algoritmo percorre vários valores de `t` (no código, `NUM_PASSOS = 200` subdivisões), calcula o ponto correspondente e liga os pontos consecutivos com pequenos segmentos de reta, reaproveitando o **DDA** já implementado. Quanto mais subdivisões, mais suave fica o traçado.

> **Importante:** as duas curvas são calculadas ponto a ponto a partir das suas fórmulas matemáticas. **Não** são usadas funções prontas como `.bezier()` ou `.hermite()`.

---

### 📈 Bézier cúbica

Usa **quatro pontos de controle**: P0, P1, P2, P3.

- A curva **passa** apenas por P0 (início) e P3 (fim).
- P1 e P2 **não são tocados**: apenas "puxam" o traçado, controlando direção e curvatura.

**Entrada:** 4 cliques, na ordem P0, P1, P2, P3.

**Equação (forma de Bernstein):**

B(t) = (1-t)³·P0 + 3(1-t)²·t·P1 + 3(1-t)·t²·P2 + t³·P3

Os quatro coeficientes são os **polinômios de Bernstein de grau 3**. Eles funcionam como pesos: definem quanto cada ponto de controle influencia o ponto atual. A soma dos quatro pesos é sempre 1, ou seja, cada ponto da curva é uma média ponderada dos pontos de controle.

---

### 📉 Hermite

Usa **dois pontos** pelos quais a curva passa — P0 (início) e P1 (fim) — e **dois vetores tangentes**, T0 e T1, que controlam a direção e a "força" com que a curva sai de P0 e chega em P1.

No paint, as tangentes vêm de dois **pontos-guia** clicados e são multiplicadas por um fator de escala (`ESCALA_TANGENTE = 3`):

T0 = (guia0 - P0) * 3   | T1 = (guia1 - P1) * 3

**Entrada:** 4 cliques, na ordem P0 (início), P1 (fim), guia da tangente em P0, guia da tangente em P1.

**Equação (funções de mistura de Hermite):**

- h00(t) =  2t³ - 3t² + 1   (peso de P0)
- h10(t) =   t³ - 2t² + t   (peso de T0)
- h01(t) = -2t³ + 3t²       (peso de P1)
- h11(t) =   t³ -  t²       (peso de T1)

H(t) = h00·P0 + h10·T0 + h01·P1 + h11·T1

Em t = 0 apenas h00 vale 1 (a curva está em P0); em t = 1 apenas h01 vale 1 (a curva está em P1). Por isso os pontos extremos não dependem da escala da tangente: o fator 3 só intensifica a curvatura, evitando que a curva fique quase reta.

---

### Diferença prática

| | Bézier cúbica | Hermite |
|---|---|---|
| Entrada | 4 pontos de controle | 2 pontos + 2 tangentes |
| Passa por | P0 e P3 | P0 e P1 |
| Controle do formato | posição de P1 e P2 | direção/intensidade das tangentes |

---

### Fontes

As implementações são próprias, baseadas nas fórmulas padrão dessas curvas. Referências consultadas:

- GeeksForGeeks — *Cubic Bezier Curve Implementation*: https://www.geeksforgeeks.org/cubic-bezier-curve-implementation-in-c/

---

## 🧠 Estrutura de Dados

Retas e círculos são armazenados com dois vértices:


reta = {
"v1": (x1, y1),
"v2": (x2, y2),
"tipo": "reta" ou "circulo"
}


As curvas paramétricas são armazenadas com a lista dos 4 pontos clicados:


curva = {
"pontos": [p0, p1, p2, p3],
"tipo": "bezier" ou "hermite"
}


---

## ▶️ Execução

### Pré-requisitos
- Python 3
- Biblioteca Pygame

Instalação:


pip install pygame


---

### Executar


python arquivo.py


---

## 📦 Executável

O projeto pode ser distribuído como `.exe` utilizando:


pyinstaller --onefile --windowed --add-data "icons;icons" arquivo.py


---

## 📚 Observações

- O sistema utiliza coordenadas baseadas no Pygame (origem no canto superior esquerdo)
- As transformações são aplicadas em relação ao centro da tela
- Entrada de dados é feita via interface gráfica
- As curvas paramétricas exigem 4 cliques e contam com orientação visual durante a construção

---

## 👨‍💻 Autor

Projeto desenvolvido para a disciplina de Computação Gráfica.