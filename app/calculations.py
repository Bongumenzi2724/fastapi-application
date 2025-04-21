def add(num1:int,num2:2):
    return num1 + num2

def subtract(num1:int,num2:int):
    return num1 - num2

def multiply(num1:int,num2:int):
    return num1 * num2

def divide(num1:int,num2:int):
    if(num2==0):
        return f"cannot divide by zero:{num2}"
    
    return num1 / num2

class test_insufficient_funds(Exception):
    pass

class BankAccount():
    def __init__(self,starting_balance=0):
        self.balance=starting_balance
    
    def deposit(self,amount):
        self.balance+=amount
    
    def withdraw(self,amount):
        if amount>self.balance:
            raise test_insufficient_funds("You have insufficient funds bro")
        
        self.balance-=amount
        
    def collect_interest(self):
        self.balance*=1.1
    