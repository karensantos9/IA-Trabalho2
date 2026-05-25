import random

from utils import (
    N,
    calcular_conflitos,
    gerar_vizinhos
)


# ==========================================
# Construção gulosa aleatória
# ==========================================

def construir_solucao_grasp(alpha=0.3):

    estado = [-1] * N

    for col in range(N):

        candidatos = []

        for linha in range(N):

            conflitos = 0

            for c in range(col):

                if estado[c] == linha:
                    conflitos += 1

                elif abs(estado[c] - linha) == abs(c - col):
                    conflitos += 1

            candidatos.append((linha, conflitos))

        candidatos.sort(key=lambda x: x[1])

        melhor = candidatos[0][1]
        pior = candidatos[-1][1]

        limite = melhor + alpha * (pior - melhor)

        lrc = [
            c for c in candidatos
            if c[1] <= limite
        ]

        escolhido = random.choice(lrc)

        estado[col] = escolhido[0]

    return estado


# ==========================================
# Busca local
# ==========================================

def hill_climbing_estado_inicial(
    estado,
    max_iter=1000,
    max_laterais=10
):

    h_atual = calcular_conflitos(estado)

    iteracoes = 0
    movimentos_laterais = 0
    houve_otimo_local = False

    if h_atual == 0:
        return (
            estado,
            h_atual,
            0,
            0,
            False
        )
    
    while iteracoes < max_iter:

        vizinhos = gerar_vizinhos(estado)

        melhor_vizinho = None
        melhor_h = float("inf")

        for v in vizinhos:

            h = calcular_conflitos(v)

            if h < melhor_h:
                melhor_h = h
                melhor_vizinho = v

        if melhor_h < h_atual:

            estado = melhor_vizinho
            h_atual = melhor_h

            movimentos_laterais = 0

        elif melhor_h == h_atual:

            estado = melhor_vizinho

            movimentos_laterais += 1

        else:

            houve_otimo_local = True
            break

        iteracoes += 1

        if h_atual == 0:
            break

        if movimentos_laterais >= max_laterais:
            break

    return (
        estado,
        h_atual,
        iteracoes,
        movimentos_laterais,
        houve_otimo_local
    )


# ==========================================
# GRASP
# ==========================================

def grasp_8_rainhas(
    max_iter=1000,
    max_grasp=30,
    alpha=0.3
):

    melhor_estado = None
    melhor_h = float("inf")

    total_iteracoes = 0
    total_laterais = 0
    houve_otimo_local = False

    estado_inicial_grasp = None

    for _ in range(max_grasp):

        estado_inicial = construir_solucao_grasp(alpha)

        if estado_inicial_grasp is None:
            estado_inicial_grasp = estado_inicial.copy()

        (
            estado_final,
            h_final,
            iteracoes,
            laterais,
            otimo_local
        ) = hill_climbing_estado_inicial(
            estado_inicial,
            max_iter
        )

        total_iteracoes += iteracoes
        total_laterais += laterais

        if otimo_local:
            houve_otimo_local = True

        if h_final < melhor_h:

            melhor_h = h_final
            melhor_estado = estado_final

        if melhor_h == 0:
            break

    return {
        "estado_inicial": estado_inicial_grasp,
        "estado_final": melhor_estado,
        "h_final": melhor_h,
        "iteracoes": total_iteracoes,
        "movimentos_laterais": total_laterais,
        "houve_otimo_local": houve_otimo_local,
        "sucesso": melhor_h == 0
    }