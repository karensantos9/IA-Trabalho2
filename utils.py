import random

N = 8


# Estado aleatório
def gerar_estado_aleatorio():
    return [random.randint(0, N - 1) for _ in range(N)]


# Função objetivo
def calcular_conflitos(estado):

    conflitos = 0

    for i in range(N):
        for j in range(i + 1, N):

            # mesma linha
            if estado[i] == estado[j]:
                conflitos += 1

            # diagonal
            elif abs(estado[i] - estado[j]) == abs(i - j):
                conflitos += 1

    return conflitos


# Fitness para algoritmo genético
def fitness(estado):

    max_pairs = (N * (N - 1)) // 2

    return max_pairs - calcular_conflitos(estado)


# Geração de vizinhos
def gerar_vizinhos(estado):

    vizinhos = []

    for col in range(N):

        for linha in range(N):

            if estado[col] != linha:

                novo = estado.copy()

                novo[col] = linha

                vizinhos.append(novo)

    return vizinhos