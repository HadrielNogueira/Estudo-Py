from abc import ABC, abstractclassmethod, abstractproperty


class Account:
    def __init__(self, account_number, client):
     self._balance = 0.00
     self._account_number = account_number
     self._agency_number = "0001"
     self._client = client
     self._history = History()
    
    @classmethod
    def new_account(cls, account_number, client):
       return cls(account_number, client)
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def account_number(self):
        return self._account_number
    
    @property
    def agency_number(self):
        return self._agency_number
    
    @property
    def client(self):
        return self._client
    
    @property
    def history(self):
        return self._history

    def withdraw(self, value):
        exceeded_balance = value > self.balance

        if exceeded_balance:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif value > 0:
            self.balance -= value
            extrato += f"Saque realizado com sucesso!!\nValor do saque: R$ {value:.2f}\n"
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
        return False
    
    def deposit(self, value):
        if value > 0:
            self.balance += value
            print("Deposito realizado com Sucesso!")
        else:
            print("Valor de deposito invalido")
            return False
        return True

class History:
    def __init__(self):
        self._transactions = []
    
    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction):
       self._transactions.append(
           {
               "type": transaction.__class__.__name__,
               "value": transaction.value
           }
       )
    
class CheckingAccount(Account):
    def __init__(self, account_number, client, withdrawal_limit = 3, cash_withdrawal_limit = 500):
        super().__init__(account_number, client)
        self.withdrawal_limit = withdrawal_limit
        self.cash_withdrawal_limit = cash_withdrawal_limit

    def withdraw(self, value):
        withdrawal_number = len([
            transaction for transaction in self.history.transactions 
            if transaction["type"] == Withdrawal.__name__
        ])


        exceeded_balance = value > self.balance
        exceeded_withdrawal_limit = withdrawal_number > self.withdrawal_limit

        if exceeded_balance:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif exceeded_withdrawal_limit:
            print("Operação falhou! Seu limite de saques foi excedido!.")
        else:
            return super().withdraw(value)
        
        return False

class Client:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def process_transaction(self, account, transaction):
        pass

    def add_account(self, account):
        self.accounts.append(account)

class NaturalPerson(Client):
    def __init__(self, address, cpf, name, date_of_birth):
        super().__init__(address)
        self.cpf = cpf
        self.name = name
        self.date_of_birth = date_of_birth

class Transaction(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def register(self, account):
        pass

class Withdrawal(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self.value
    
    def register(self, account):
        sucess_transaction = account.withdraw(self.value)
        if sucess_transaction:
            account.history.add_transaction(self)

class Deposit(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self.value
    
    def register(self, account):
        sucess_transaction = account.withdraw(self.value)
        if sucess_transaction:
            account.history.add_transaction(self)