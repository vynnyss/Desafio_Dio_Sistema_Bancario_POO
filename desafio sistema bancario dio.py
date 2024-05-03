from abc import ABC, abstractmethod

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
        
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero    
        
    @property
    def agencia(self):
        return self._agencia    
            
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return Conta( numero, cliente)
    
    def sacar(self, valor):
        if valor > self.saldo or valor < 0:
            print("operação falhou!!!")
            return False   
            
        else:
            print("Saque realizado com sucesso")
            self._saldo -= valor
            return True 
        
    def depositar(self, valor):
        if valor > 0:
            print("Deposito realizado com sucesso")
            self._saldo += valor
            return True
        else:
            print("Operação Falhou!!!")
            return False
               
class ContaCorrente(Conta):
    def __init__(self, numero, cliente):
        super().__init__(numero, cliente)
        self.limite = 500
        self.limite_saques = 3
        
    def sacar(self, valor):
        numero_saques = 0
        if numero_saques > self.limite_saques:
            print("Operação falhou, você atingiu o limite de saques")
            
        elif valor > self.limite:
            print("Operação falhou, o valor ultapassa o seu limite")
            
        else:
            numero_saques += 1
            return super().sacar(valor)
        
        return False
        
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
       
class Historico():
    def __init__(self):
        self._transacoes = ""
        pass
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao, valor):
        self._transacoes += f'Tipo de transação realizada {transacao}.\nValor da transação realizada {valor:.2f}\n\n\n.'
        
class Transacao(ABC):
    
    @abstractmethod
    def registrar(self, conta):
        pass
    
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_sucesso = conta.sacar(self.valor)
        if transacao_sucesso == True:
            conta.historico.adicionar_transacao("Saque", self.valor)
            
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_sucesso = conta.depositar(self.valor)
        if transacao_sucesso == True:
            conta.historico.adicionar_transacao("Deposito", self.valor)
            
class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self.contas = []
        
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)
          
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
    
       
def menu():
    menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova Conta
    [lc] Listar Contas
    [nu] Novo Usuario
    [q] Sair
    =>"""

    return input(menu)

def recuperar_conta_cliente(cliente):
    
    if not cliente.contas:
        print("Cliente não possui conta!")
        return
    elif len(cliente.contas) > 1:
        for conta in cliente.contas:
            print(f'Agência: {conta.agencia}| numero: {int(conta.numero):04d}')
        opcao = input("digite o numero da conta que deseja utilizar")
        for conta in cliente.contas:
            if int(opcao) == int(conta.numero):
                return conta
    return cliente.contas[0]

def depositar(clientes):
    cpf = int(input("informe seu CPF"))
    cliente = filtrar_clientes(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado")
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    valor = float(input("Informe o valor do deposito: "))    
    transacao = Deposito(valor)    
    cliente.realizar_transacao(conta, transacao)
    
def saque (clientes):
    cpf = int(input("informe seu CPF"))
    cliente = filtrar_clientes(cpf, clientes)    
    
    if not cliente:
        print("Cliente não encontrado")
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
        
    valor = float(input("Informe o valor do : "))
    transacao = Saque(valor)
    
    cliente.realizar_transacao(conta, transacao)    
    
def exibir_extrato(clientes):
    cpf = int(input("informe seu CPF"))
    cliente = filtrar_clientes(cpf, clientes)    
    
    if not cliente:
        print("Cliente não encontrado")
        return    

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return    
    
    print('             Extrato             ')    
    
    transacoes = conta.historico.transacoes
    
    if not transacoes:
        print('Não foram realizadas movimentações')
        
    else:
        print(transacoes)
        
    print(f'Saldo: R${conta.saldo:.2f}')
    
def criar_cliente(clientes):
    cpf = int(input("Informe o CPF: "))
    cliente = filtrar_clientes(cpf, clientes)
    
    if cliente:
        print("Já existe um usuário com esse CPF!")
        return
    
    nome = input("Digite o seu nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    cliente = PessoaFisica( cpf = cpf, nome = nome, data_nascimento = data_nascimento, endereco = endereco)
    
    clientes.append(cliente)
    
    print("Usuário criado com sucesso!")
       
def criar_conta(clientes, contas, numero_conta):
    cpf = int(input("informe o CPF do usuário: "))
    cliente = filtrar_clientes(cpf, clientes)
    
    if cliente:
        conta = ContaCorrente.nova_conta(cliente = cliente, numero = numero_conta)
        contas.append(conta)
        cliente.contas.append(conta)
    
        print("Conta criada com sucesso!")    
        return    
    print("Usuario não encontrado, criação de conta encerrada!")
    return

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(conta.cliente, conta.numero)

def filtrar_clientes(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def main():
    
    clientes = []
    contas = []    

    while True: 
        opcao = menu()
        
        
        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            saque(clientes)
               

        elif opcao == "e":
            exibir_extrato(clientes)
            
        elif opcao == "nu":
            criar_cliente(clientes)
        
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(clientes, contas, numero_conta)
                
        elif opcao == "lc":
            listar_contas(contas)
            
        elif opcao == "p":
            print(clientes)
            teste(clientes)
            
        elif opcao == "q":
            break
        
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
            
def teste (clientes):
    for cliente in clientes:
        print(cliente.cpf, cliente.contas)

main()
