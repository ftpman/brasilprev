from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Jogador import Jogador

class Propriedade():
    """Classe que representa uma Propriedade no Tabuleiro"""
    
    def __init__(self, valor: float, aluguel: float) -> None:
        """
        Cria uma nova Propriedade

        Parâmetros:
        -----------
        valor: float
            Valor de Venda da Propriedade. Precisa ser > 0
        aluguel: float
            Valor de Aluguel da Propriedade. Precisa ser > 0
        """
        if not valor > 0:
            raise ValueError("Valor de Venda precisa ser > 0")
        if not aluguel > 0:
            raise ValueError("Valor do Aluguel precisa ser > 0")
        self._venda = valor
        self._aluguel = aluguel
        self._proprietario = None
    
    @property
    def valor(self) -> float:
        """Valor de Venda da Propriedade"""
        return self._venda
    
    @property
    def aluguel(self):
        """Valor do Aluguel da Propriedade"""
        return self._aluguel
    
    @property
    def proprietario(self) -> Jogador:
        """Proprietário da Propriedade"""
        return self._proprietario

    @proprietario.setter
    def proprietario(self, proprietario: Jogador):
        self._proprietario = proprietario

    @property
    def possui_proprietario(self) -> bool:
        """Indica se a propriedade já possui um Jogador como Proprietário"""
        return not self._proprietario is None

    def __str__(self) -> str:
        return str(self.toJSON())

    def __repr__(self) -> str:
        return self.__str__()

    def toJSON(self) -> dict:
        return {
            'valor': self.valor,
            'aluguel': self.aluguel,
            'proprietario': self.proprietario,
            'possui_proprietario': self.possui_proprietario
        }