from random import randint, shuffle

from src.Propriedade import Propriedade
from src.Jogador import Jogador, Aleatorio, Cauteloso, Exigente, Impulsivo

class Tabuleiro():
    """Classe que representa o Tabuleiro do Jogo"""

    def __init__(self, quantidade=20, limite_rodadas=1000) -> None:
        """
        Cria um novo Tabuleiro para rodar o Jogo

        Parâmetros
        ----------
        quantidade: int, opcional
            Define a quantidade de propriedades que o Tabuleiro terá
            (padrão é 20)

        limite_rodadas: int, opcional
            Define a quantidade limite de rodadas, antes que o jogue acabe
            sem nenhum vencedor, por tempo limite (padrão é 1000)
        """
        self._rodada_atual = 0
        self._limite_rodadas = limite_rodadas
        self._propriedades = self.__cria_propriedades(quantidade)
        self._jogadores_criados = self.__cria_jogadores()
        self._jogando = []
        self._jogador_vencedor = None
        self._resultado = None
    
    @property
    def propriedades(self) -> list[Propriedade]:
        """Representa a lista de Propriedades disponíveis do Tabuleiro"""
        return self._propriedades

    @property
    def jogadores(self) -> list[Jogador]:
        """Representa a lista de Jogadores que estão Jogando"""
        return list(filter(lambda j: not j.perdeu, self._jogando))

    @property
    def resultado(self) -> dict | None:
        """Ao final da Partida, contém o Resultado da Partida"""
        return self._resultado

    def __cria_jogadores(self) -> list[Jogador]:
        """Cria a lista de jogadores que serão utilizados durante todas as partidas, com este Tabuleiro"""
        return list(map(
            lambda c: Jogador(c(), self), [
                Impulsivo,
                Exigente,
                Cauteloso,
                Aleatorio,
            ]
        ))
        pass

    def __cria_propriedades(self, quantidade: int) -> list[Propriedade]:
        """Cria a lista de Propriedades que serão utilizadas durante todas as partidas, com este Tabuleiro"""
        return list(map(
            lambda i: Propriedade(valor=randint(40, 200), aluguel=randint(10, 80)),
            range(quantidade)
        ))
        
    def __inicializa_jogadores(self):
        """Prepara a lista de Jogadores para uma nova partida"""
        self._jogando = list(map(lambda j: j.nova_partida(), self._jogadores_criados))
        self._jogador_vencedor = None

    def __sorteia_ordem_jogadores(self):
        """Define a ordem em que cada Jogador irá Jogar na partida"""
        if not len(self.jogadores) > 0:
            self.__inicializa_jogadores()
        shuffle(self._jogando)

    def __inicializa_propriedades(self):
        """Prepara a lista de Propriedades para uma nova partida"""
        for propriedade in self.propriedades:
            propriedade.proprietario = None
    
    def __executa_rodada(self):
        """Executa uma rodada da Partida, fazendo cada Jogador que ainda está na partida, jogar o dado"""
        for jogador in self.jogadores:
            if jogador.joga_dado().perdeu and self.__restou_um_jogador():
                return

    def __partida_finalizada(self) -> bool:
        """É responsável por executar as Rodadas e retornar quando a partida é Finalizada"""
        if self._rodada_atual > 0:
            self.__executa_rodada()
        return not self._jogador_vencedor is None or self._rodada_atual == self._limite_rodadas

    def __restou_um_jogador(self) -> bool:
        """Verifica se restou apenas um jogador com saldo positivo, e o declara vencedor"""
        jogadores_restantes = self.jogadores
        if len(jogadores_restantes) == 1:
            self._jogador_vencedor = jogadores_restantes[0]
            return self._jogador_vencedor.vence_partida()
        return False

    def __verifica_vencedor(self) -> Jogador:
        """Verifica se a partida possui um vencedor ou usa o critério de desempate"""
        vencedor = self._jogador_vencedor
        if vencedor is None:
            jogador_maior_saldo = sorted(self.jogadores, key=lambda j: j.saldo, reverse=True)[0]
            jogadores_mesmo_saldo = list(filter(lambda j: j.saldo == jogador_maior_saldo.saldo, self.jogadores))
            if len(jogadores_mesmo_saldo) > 1:
                jogador_maior_saldo = jogadores_mesmo_saldo[0]
            vencedor = jogador_maior_saldo
        return vencedor

    def inicia_partida(self) -> dict:
        """
        Inicia a execução de uma nova Partida e retorna o resultado

        Retorna:
        --------
        dict
            Contém o resultado da partida com os seguintes campos
            {
                "total_rodadas": int,
                "timeout": bool,
                "vencedor": dict, ## veja Jogador.toJSON()
            }
        """
        if not self._rodada_atual > 0:
            self.__inicializa_jogadores()
            self.__inicializa_propriedades()
            self.__sorteia_ordem_jogadores()

            for self._rodada_atual in range(1, self._limite_rodadas + 1):
                if self.__partida_finalizada():
                    return self.finaliza_partida()

            raise RuntimeError("Partida não finalizada corretamente")
        raise RuntimeError("Partida em andamento")

    def finaliza_partida(self) -> dict:
        """
        Finaliza a partida atual e registra o resultado

        Retorna:
        --------
        dict
            Contém o resultado da partida com os seguintes campos
            {
                "total_rodadas": int,
                "timeout": bool,
                "vencedor": dict,   ## veja Jogador.toJSON()
            }
        """
        self._resultado = {
            "total_rodadas": self._rodada_atual,
            "timeout": self._jogador_vencedor is None,
            "vencedor": self.__verifica_vencedor().toJSON(),
        }
        self._jogando.clear()
        self._rodada_atual = 0
        self._jogador_vencedor = None
        return self._resultado
