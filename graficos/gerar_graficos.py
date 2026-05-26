import json
import matplotlib.pyplot as plt


# ==========================================
# Ler resultados
# ==========================================

with open("../resultados/grasp.json", "r") as f:
    grasp = json.load(f)

with open("../resultados/genetico.json", "r") as f:
    genetico = json.load(f)


# ==========================================
# Ajustar estrutura do n8n
# ==========================================

grasp = grasp[0]
genetico = genetico[0]


# ==========================================
# Dados
# ==========================================

algoritmos = ["GRASP", "Genético"]

tempo = [
    grasp["estatisticas"]["media_tempo"],
    genetico["estatisticas"]["media_tempo"]
]

iteracoes = [
    grasp["estatisticas"]["media_iteracoes"],
    genetico["estatisticas"]["media_iteracoes"]
]

sucesso = [
    grasp["estatisticas"]["taxa_sucesso"],
    genetico["estatisticas"]["taxa_sucesso"]
]

fitness = [
    grasp["estatisticas"]["media_fitness"],
    genetico["estatisticas"]["media_fitness"]
]


# ==========================================
# GRÁFICO TEMPO
# ==========================================

plt.figure(figsize=(6, 4))

plt.bar(algoritmos, tempo)

plt.ylabel("Tempo Médio (s)")

plt.title("Comparação de Tempo")

plt.savefig("grafico_tempo.png")

plt.close()


# ==========================================
# GRÁFICO ITERAÇÕES
# ==========================================

plt.figure(figsize=(6, 4))

plt.bar(algoritmos, iteracoes)

plt.ylabel("Média de Iterações")

plt.title("Comparação de Iterações")

plt.savefig("grafico_iteracoes.png")

plt.close()


# ==========================================
# GRÁFICO SUCESSO
# ==========================================

plt.figure(figsize=(6, 4))

plt.bar(algoritmos, sucesso)

plt.ylabel("Taxa de Sucesso (%)")

plt.title("Comparação de Sucesso")

plt.savefig("grafico_sucesso.png")

plt.close()


# ==========================================
# GRÁFICO FITNESS
# ==========================================

plt.figure(figsize=(6, 4))

plt.bar(algoritmos, fitness)

plt.ylabel("Fitness Médio")

plt.title("Comparação de Fitness")

plt.savefig("grafico_fitness.png")

plt.close()


print("Gráficos gerados com sucesso na pasta graficos!")