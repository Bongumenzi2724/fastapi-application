import pytest
from app.calculations import add,subtract,multiply,divide,BankAccount,test_insufficient_funds

@pytest.fixture
def zero_bank_account():
    print("Creating zero balance instance object")
    return BankAccount()

@pytest.fixture
def bank_account():
    print("Creating non-zero balance instance object")
    return BankAccount(50)

@pytest.mark.parametrize("num1,num2,result",[(5,3,8),(6,6,12),(5,6,11)])
def test_add(num1,num2,result):
    print("testing add function")
    assert add(num1,num2)==result
    
@pytest.mark.parametrize("num1,num2,result",[(9,4,5),(6,6,0),(5,3,2)])
def test_subtract(num1,num2,result):
    print("Testing subtraction")
    assert subtract(num1,num2)==result

def test_bank_set_initial_amount(bank_account):
    print("Class Testing Method")
    assert bank_account.balance==50

def test_default_amount(zero_bank_account):
    print("Default value class")
    assert zero_bank_account.balance==0
    
def test_class_withdraw(bank_account):
    bank_account_value=bank_account
    print("Withdraw an amount")
    bank_account_value.withdraw(20)
    assert bank_account_value.balance==30

def test_class_deposit():
    bank_account=BankAccount(50)
    print("Deposit an amount")
    bank_account.deposit(50)
    assert bank_account.balance==100

def test_insufficient_funds(bank_account):
    with pytest.raises(test_insufficient_funds):
        bank_account.withdraw(200)



@pytest.mark.parametrize("num1,num2,result",[(10,4,40),(6,5,30),(5,3,15)])
def test_multiply(num1,num2,result):
    print("Testing multiplication")
    assert multiply(num1,num2)==result
    
def test_divide():
    print("Testing Division")
    assert divide(4,2)==2
    

@pytest.mark.parametrize("deposited,withdrew,result",[(200,100,100),(50,10,40),(1200,200,1000)])

def test_transfer(zero_bank_account,deposited,withdrew,result):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance==result