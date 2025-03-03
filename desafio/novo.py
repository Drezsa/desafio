# cliente.py
from datetime import date

class Cliente:
    def __init__(self, endereco, cpf, nome, data_nascimento):
        self.endereco = endereco
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

# conta.py
from abc import ABC, abstractmethod
from .historico import Historico # type: ignore
from .excecoes import SaldoInsuficienteError # type: ignore

class Conta(ABC):
    def __init__(self, numero, agencia, cliente):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo(self):
        return self.saldo

    def sacar(self, valor):
        if self.saldo >= valor:
            self.saldo -= valor
            return True
        raise SaldoInsuficienteError("Saldo insuficiente")

    def depositar(self, valor):
        self.saldo += valor
        return True

    @abstractmethod
    def nova_conta(self, cliente, numero):
        pass

class ContaCorrente(Conta):
    def __init__(self, numero, agencia, cliente, limite, limite_saques):
        super().__init__(numero, agencia, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    def sacar(self, valor):
        if self.saques_realizados < self.limite_saques and (self.saldo + self.limite) >= valor:
            self.saldo -= valor
            self.saques_realizados += 1
            return True
        raise SaldoInsuficienteError("Limite de saque excedido ou saldo insuficiente")

    def nova_conta(self, cliente, numero):
        return ContaCorrente(numero, "0001", cliente, 500, 3)

class ContaPoupanca(Conta):
    def __init__(self, numero, agencia, cliente):
        super().__init__(numero, agencia, cliente)

    def nova_conta(self, cliente, numero):
        return ContaPoupanca(numero, "0001", cliente)

# transacao.py
from abc import ABC, abstractmethod

class Transacao(ABC):
    def __init__(self, valor):
        self.valor = valor

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def registrar(self, conta):
        conta.depositar(self.valor)
        conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def registrar(self, conta):
        conta.sacar(self.valor)
        conta.historico.adicionar_transacao(self)

# historico.py
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)
