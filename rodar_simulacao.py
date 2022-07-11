from json import dumps
from src.Jogador import Aleatorio, Cauteloso, Exigente, Impulsivo
from src.Tabuleiro import Tabuleiro

QTD_JOGOS=300

def total_partidas_terminadas_timeout(resultados: list[dict]):
    return len(list(filter(lambda resultado:resultado["timeout"], resultados)))

def media_rodadas(resultados: list[dict]):
    return sum(list(map(lambda resultado: resultado["total_rodadas"], resultados))) / QTD_JOGOS

def porcentagem_vitorias_comportamento(resultados: list[dict]):
    return list(map(lambda comportamento: {
        "Comportamento": comportamento,
        "Porcentagem": len(list(filter(lambda resultado: resultado["vencedor"]["tipo"] == comportamento, resultados))) / QTD_JOGOS * 100
    }, [
        str(Impulsivo()),
        str(Exigente()),
        str(Cauteloso()),
        str(Aleatorio()),
    ]))

def comportamento_vitorioso(vitorias: list[dict]):
    return sorted(vitorias, key=lambda o:o["Porcentagem"], reverse=True)[0]["Comportamento"]

def inicia_simulacao():
    tabuleiro = Tabuleiro()
    print("")
    print("**********************************")
    print(" Simulação Iniciada, Aguarde...")
    print("\r\n")
    resultados = list(map(lambda i: tabuleiro.inicia_partida(), range(QTD_JOGOS)))

    print(" RESULTADOS")
    print("**********************************\r\n")
    print(f" Quantas partidas terminaram por timeout: {total_partidas_terminadas_timeout(resultados)}\r\n")

    print(f" Quantos turnos em média demorou uma partida: {media_rodadas(resultados):.2f}\r\n")

    vitorias = porcentagem_vitorias_comportamento(resultados)
    print(" Qual a porcentagem de vitórias por comportamento dos jogadores:\r\n")
    list(map(lambda o: print(f" --- {o['Comportamento']} \t: {o['Porcentagem']:.1f}\t%"), vitorias))
    
    print("")
    print(f"Qual o comportamento que mais venceu: {comportamento_vitorioso(vitorias)}\r\n")

    print("**********************************")
    print("")


if __name__ == "__main__":
    inicia_simulacao()
