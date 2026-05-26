import statistics


def gerar_estatisticas(resultados):

    tempos = [
        r["tempo"]
        for r in resultados
    ]

    iteracoes = [
        r["iteracoes"]
        for r in resultados
    ]

    sucessos = [
        r for r in resultados
        if r["sucesso"]
    ]

    fitnesses = [
        28 - r["h_final"]
        for r in resultados
    ]

    # ==========================
    # 5 melhores soluções
    # ==========================

    ordenados = sorted(
        resultados,
        key=lambda r: r["h_final"]
    )

    melhores = []
    vistos = set()

    for r in ordenados:

        solucao = tuple(r["estado_final"])

        if solucao not in vistos:

            vistos.add(solucao)

            melhores.append({

                "solucao":
                    r["estado_final"],

                "fitness":
                    28 - r["h_final"],

                "h_final":
                    r["h_final"],

                "algoritmo":
                    r["algoritmo"],

                "tempo":
                    r["tempo"]
            })

        if len(melhores) == 5:
            break

    return {

        "media_tempo":
            statistics.mean(tempos),

        "desvio_padrao_tempo":
            statistics.stdev(tempos)
            if len(tempos) > 1 else 0,

        "media_iteracoes":
            statistics.mean(iteracoes),

        "desvio_padrao_iteracoes":
            statistics.stdev(iteracoes)
            if len(iteracoes) > 1 else 0,

        "taxa_sucesso":
            (
                len(sucessos)
                / len(resultados)
            ) * 100,

        "media_fitness":
            statistics.mean(fitnesses),

        "desvio_padrao_fitness":
            statistics.stdev(fitnesses)
            if len(fitnesses) > 1 else 0,

        "5_melhores_solucoes":
            melhores
    }