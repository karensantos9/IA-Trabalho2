import random

from utils import (
    N,
    fitness,
    calcular_conflitos,
    gerar_estado_aleatorio
)


# ==========================================
# População inicial
# ==========================================

def criar_populacao(tamanho_pop):

    return [
        gerar_estado_aleatorio()
        for _ in range(tamanho_pop)
    ]


# ==========================================
# Seleção
# ==========================================

def selecionar_pais(populacao):

    pesos = [
        fitness(ind)
        for ind in populacao
    ]

    total = sum(pesos)

    if total == 0:
        return random.sample(populacao, 2)

    pais = random.choices(
        populacao,
        weights=pesos,
        k=2
    )

    return pais[0], pais[1]


# ==========================================
# Crossover
# ==========================================

def crossover(p1, p2):

    corte = random.randint(1, N - 2)

    filho1 = p1[:corte] + p2[corte:]
    filho2 = p2[:corte] + p1[corte:]

    return filho1, filho2


# ==========================================
# Mutação
# ==========================================

def mutacao(individuo, taxa_mutacao=0.1):

    novo = individuo.copy()

    if random.random() < taxa_mutacao:

        col = random.randint(0, N - 1)

        novo[col] = random.randint(0, N - 1)

    return novo


# ==========================================
# Algoritmo Genético
# ==========================================

def algoritmo_genetico(
    tamanho_pop=50,
    max_geracoes=300,
    taxa_mutacao=0.15
):

    populacao = criar_populacao(tamanho_pop)

    melhor_estado = None
    melhor_h = float("inf")

    for geracao in range(max_geracoes):

        for individuo in populacao:

            h = calcular_conflitos(individuo)

            if h < melhor_h:

                melhor_h = h
                melhor_estado = individuo

            if h == 0:

                return {
                    "estado_inicial": populacao[0],
                    "estado_final": individuo,
                    "h_final": 0,
                    "iteracoes": geracao,
                    "movimentos_laterais": 0,
                    "houve_otimo_local": False,
                    "sucesso": True
                }

        nova_populacao = []

        while len(nova_populacao) < tamanho_pop:

            pai1, pai2 = selecionar_pais(populacao)

            filho1, filho2 = crossover(pai1, pai2)

            filho1 = mutacao(filho1, taxa_mutacao)
            filho2 = mutacao(filho2, taxa_mutacao)

            nova_populacao.append(filho1)
            nova_populacao.append(filho2)

        populacao = nova_populacao

    return {
        "estado_inicial": populacao[0],
        "estado_final": melhor_estado,
        "h_final": melhor_h,
        "iteracoes": max_geracoes,
        "movimentos_laterais": 0,
        "houve_otimo_local": False,
        "sucesso": False
    }