from fastapi import FastAPI

import uuid
import time

from grasp import grasp_8_rainhas
from genetico import algoritmo_genetico

app = FastAPI()


# ==========================================
# EXECUÇÃO
# ==========================================

def executar_algoritmo(
    algoritmo="grasp",
    max_iter=1000
):

    inicio = time.time()

    if algoritmo == "grasp":

        resultado = grasp_8_rainhas(max_iter)

    elif algoritmo == "genetico":

        resultado = algoritmo_genetico(
            max_geracoes=max_iter
        )

    else:

        return {
            "erro": "Algoritmo inválido"
        }

    fim = time.time()

    return {
        "execucao": str(uuid.uuid4()),
        "algoritmo": algoritmo,
        "estado_inicial": resultado["estado_inicial"],
        "estado_final": resultado["estado_final"],
        "h_final": resultado["h_final"],
        "iteracoes": resultado["iteracoes"],
        "tempo": fim - inicio,
        "sucesso": resultado["sucesso"],
        "movimentos_laterais": resultado["movimentos_laterais"],
        "houve_otimo_local": resultado["houve_otimo_local"]
    }


# ==========================================
# ENDPOINT
# ==========================================

@app.post("/executar")
def executar(data: dict):

    algoritmo = data.get("algoritmo", "grasp")

    max_iter = data.get("max_iter", 1000)

    return executar_algoritmo(
        algoritmo,
        max_iter
    )