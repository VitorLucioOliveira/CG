# 🖥️ Aplicação de Computação Gráfica 2D

## 📌 Descrição

Este projeto foi desenvolvido como parte da disciplina de Computação Gráfica e tem como objetivo implementar algoritmos fundamentais de gráficos 2D, incluindo:

- Transformações geométricas
- Rasterização de retas e circunferências
- Recorte de linhas

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

## 🧠 Estrutura de Dados

Cada objeto é armazenado como:


reta = {
"v1": (x1, y1),
"v2": (x2, y2),
"tipo": "reta" ou "circulo"
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

---

## 👨‍💻 Autor

Projeto desenvolvido para a disciplina de Computação Gráfica.