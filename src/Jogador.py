from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from random import getrandbits, randint

if TYPE_CHECKING:
    from src.Propriedade import Propriedade
    from src.Tabuleiro import Tabuleiro

class Comportamento(ABC):
    """Classe Abstrata que Representa o Comportamento de um Jogador"""
    
    @abstractmethod
    def decide_comprar(self, propriedade: Propriedade, saldo: float) -> bool:
        """Método que determina o Comportamento do Jogador"""
        raise NotImplementedError()
    
    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return self.__str__()

class Impulsivo(Comportamento):
    """Classe que Implementa o Comportamento Impulsivo"""
    
    def decide_comprar(self, propriedade: Propriedade, saldo: float) -> bool:
        """Compra qualquer propriedade"""
        return not propriedade.possui_proprietario

class Exigente(Comportamento):
    """Classe que Implementa o Comportamento Exigente"""
    
    def decide_comprar(self, propriedade: Propriedade, saldo: float) -> bool:
        """Compra a propriedade caso o valor do aluguel seja maior que 50"""
        return not propriedade.possui_proprietario and propriedade.aluguel > 50

class Cauteloso(Comportamento):
    """Classe que Implementa o Comportamento Cauteloso"""
    
    def decide_comprar(self, propriedade: Propriedade, saldo: float) -> bool:
        """Compra a propriedade caso fique com 80 de saldo após a compra"""
        return not propriedade.possui_proprietario and saldo - propriedade.valor >= 80

class Aleatorio(Comportamento):
    """Classe que Implementa o Comportamento Aleatorio"""
    
    def decide_comprar(self, propriedade: Propriedade, saldo: float) -> bool:
        """Compra a propriedade com uma probabilidade de 50%"""
        return not propriedade.possui_proprietario and getrandbits(1)

class Jogador():
    """Classe que representa um Jogador"""

    def __init__(self, tipo: Comportamento, tabuleiro: Tabuleiro) -> None:
        """
        Cria um novo Jogador no Tabuleiro

        Parâmetros:
        -----------
        tipo: Comportamento
            Define o Comportamento que o Jogador terá durante o Jogo
        tabuleiro: Tabuleiro
            Define o Tabuleiro em que o Jogador irá Jogar
        """
        self._saldo = 0
        self._posicao = 0
        self._propriedades = []
        self._tipo = tipo
        self._tabuleiro = tabuleiro
        self._venceu = None
        self._perdeu = None
    
    @property
    def saldo(self) -> float:
        """Representa o Saldo do Jogador no Jogo"""
        return self._saldo
    
    @saldo.setter
    def saldo(self, saldo: float):
        self._saldo = saldo
        if saldo < 0:
            self.perde_partida()

    @property
    def perdeu(self) -> bool:
        """Indica se o Jogador perdeu a partida"""
        return self._perdeu is True
    
    @property
    def venceu(self) -> bool:
        """Indica se o Jogador venceu a partida"""
        return self._venceu is True
    
    @property
    def tipo(self) -> Comportamento:
        """Representa o Tipo de Comportamento do Jogador"""
        return self._tipo

    def nova_partida(self) -> Jogador:
        """Prepara o Jogador para uma nova partida"""
        if self._tabuleiro is None or self._tabuleiro.propriedades is None or len(self._tabuleiro.propriedades) == 0:
            raise RuntimeError("Partida não pode ser iniciada: Não foram criadas as Propriedades")
        self.saldo = 300
        self._posicao = 0
        self._propriedades.clear()
        self._venceu = None
        self._perdeu = None
        return self

    def joga_dado(self) -> Jogador:
        """Joga o dado e movimenta o Jogador no Tabuleiro"""
        if not self.perdeu:
            return self.anda_no_tabuleiro(randint(1, 6))
        return self

    def anda_no_tabuleiro(self, distancia: int) -> Jogador:
        """Movimenta o Jogador no Tabuleiro"""
        self._posicao += distancia
        total_propriedades = len(self._tabuleiro.propriedades)
        if self._posicao > total_propriedades:
            self.saldo += 100
            self._posicao -= total_propriedades
        
        propriedade = self._tabuleiro.propriedades[self._posicao - 1]
        
        if propriedade.possui_proprietario:
            if not propriedade.proprietario is self:
                return self.paga_aluguel_propriedade(propriedade)
            return self
        
        return self.compra_propriedade(propriedade)

    def compra_propriedade(self, propriedade: Propriedade) -> Jogador:
        """Método usado para comprar uma propriedade do Tabuleiro, de acordo com o seu tipo de Comportamento"""
        if not propriedade.possui_proprietario and propriedade.valor <= self.saldo and self.tipo.decide_comprar(propriedade, self.saldo):
            self.saldo -= propriedade.valor
            propriedade.proprietario = self
            self._propriedades.append(propriedade)
        return self

    def paga_aluguel_propriedade(self, propriedade: Propriedade) -> Jogador:
        """Efetua o pagamento do valor do Aluguel ao Proprietário"""
        if propriedade.possui_proprietario:
            self.saldo -= propriedade.aluguel
            propriedade.proprietario.recebe_aluguel_propriedade(propriedade)
        return self

    def recebe_aluguel_propriedade(self, propriedade: Propriedade):
        """Registra no Saldo o valor recebido pelo Aluguel da Propriedade"""
        if propriedade.proprietario is self:
            self.saldo += propriedade.aluguel

    def vence_partida(self) -> bool:
        """Registra que o Jogador venceu a partida"""
        if self.perdeu:
            raise RuntimeError("Jogador não pode vencer pois não está mais na partida")

        [self._venceu, self._perdeu] = [True, False]
        return self.venceu

    def perde_partida(self):
        """Registra que o Jogador perdeu a partida, liberando suas propriedades para serem compradas por outro Jogador"""

        def perde_propriedade(p: Propriedade):
            if p.proprietario is self:
                p.proprietario = None

        [self._perdeu, self._venceu] = [True, False]
        list(map(perde_propriedade, self._propriedades))
    
    def __str__(self) -> str:
        return str(self.toJSON())

    def __repr__(self) -> str:
        return self.__str__()

    def toJSON(self) -> dict:
        return {
            'saldo': self.saldo,
            'perdeu': self.perdeu,
            'venceu': self.venceu,
            'tipo': str(self.tipo)
        }
