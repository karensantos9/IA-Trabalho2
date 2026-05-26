import random

from utils import (
    N,
    calcular_conflitos,
    gerar_estado_aleatorio
)

# ==========================================
# CONFIGURAÇÕES OBRIGATÓRIAS
# ==========================================

TAMANHO_POPULACAO = 20
TAXA_CRUZAMENTO = 0.8
TAXA_MUTACAO = 0.03
MAX_GERACOES = 1000


# ==========================================
# CONVERSÃO BINÁRIA
# Cada rainha usa 3 bits (0-7)
# ==========================================

def estado_para_binario(estado):

    binario = ""

    for valor in estado:
        binario += format(valor, "03b")

    return binario


def binario_para_estado(binario):

    estado = []

    for i in range(0, len(binario), 3):

        bits = binario[i:i+3]

        valor = int(bits, 2)

        if valor > 7:
            valor = 7

        estado.append(valor)

    return estado


# ==========================================
# FITNESS
# Quanto menor conflito, melhor
# ==========================================

def fitness(estado):

    conflitos = calcular_conflitos(estado)

    max_conflitos = 28

    return max_conflitos - conflitos


# ==========================================
# POPULAÇÃO INICIAL
# ==========================================

def criar_populacao():

    populacao = []

    for _ in range(TAMANHO_POPULACAO):

        estado = gerar_estado_aleatorio()

        individuo = estado_para_binario(estado)

        populacao.append(individuo)

    return populacao


# ==========================================
# SELEÇÃO POR ROLETA
# ==========================================

def selecionar_pais(populacao):

    estados = [
        binario_para_estado(ind)
        for ind in populacao
    ]

    fitnesses = [
        fitness(e)
        for e in estados
    ]

    soma = sum(fitnesses)

    if soma == 0:
        return random.sample(populacao, 2)

    pais = random.choices(
        populacao,
        weights=fitnesses,
        k=2
    )

    return pais[0], pais[1]


# ==========================================
# CROSSOVER DE PONTO DE CORTE
# ==========================================

def crossover(pai1, pai2):

    if random.random() > TAXA_CRUZAMENTO:

        return pai1, pai2

    ponto = random.randint(1, len(pai1) - 1)

    filho1 = pai1[:ponto] + pai2[ponto:]
    filho2 = pai2[:ponto] + pai1[ponto:]

    return filho1, filho2


# ==========================================
# MUTAÇÃO BIT FLIP
# ==========================================

def mutacao(individuo):

    individuo = list(individuo)

    for i in range(len(individuo)):

        if random.random() < TAXA_MUTACAO:

            individuo[i] = (
                "1"
                if individuo[i] == "0"
                else "0"
            )

    return "".join(individuo)


# ==========================================
# ELITISMO
# Mantém melhores indivíduos
# ==========================================

def ordenar_populacao(populacao):

    return sorted(
        populacao,
        key=lambda ind: fitness(
            binario_para_estado(ind)
        ),
        reverse=True
    )


# ==========================================
# ALGORITMO GENÉTICO
# ==========================================

def algoritmo_genetico(
    max_geracoes=MAX_GERACOES
):

    populacao = criar_populacao()

    melhor_individuo = None
    melhor_fitness = -1

    estado_inicial = binario_para_estado(
        populacao[0]
    )

    for geracao in range(max_geracoes):

        populacao = ordenar_populacao(populacao)

        elite = populacao[:2]

        melhor_atual = elite[0]

        estado_melhor = binario_para_estado(
            melhor_atual
        )

        fitness_atual = fitness(estado_melhor)

        if fitness_atual > melhor_fitness:

            melhor_fitness = fitness_atual
            melhor_individuo = melhor_atual

        if calcular_conflitos(estado_melhor) == 0:

            return {
                "estado_inicial": estado_inicial,
                "estado_final": estado_melhor,
                "h_final": 0,
                "geracoes": geracao,
                "sucesso": True,
                "movimentos_laterais": None,
                "houve_otimo_local": None
            }

        nova_populacao = elite.copy()

        while len(nova_populacao) < TAMANHO_POPULACAO:

            pai1, pai2 = selecionar_pais(populacao)

            filho1, filho2 = crossover(
                pai1,
                pai2
            )

            filho1 = mutacao(filho1)
            filho2 = mutacao(filho2)

            nova_populacao.append(filho1)

            if len(nova_populacao) < TAMANHO_POPULACAO:
                nova_populacao.append(filho2)

        populacao = nova_populacao

    melhor_estado = binario_para_estado(
        melhor_individuo
    )

    return {
        "estado_inicial": estado_inicial,
        "estado_final": melhor_estado,
        "h_final": calcular_conflitos(
            melhor_estado
        ),
        "iteracoes": max_geracoes,
        "sucesso": False,
        "movimentos_laterais": None,
        "houve_otimo_local": None
    }