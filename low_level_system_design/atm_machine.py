from enum import Enum
from abc import ABC, abstractmethod

# Here are the required enums, data types, and constants


class TransactionType(Enum):
    BALANCE_INQUIRY = 1
    DEPOSIT_CASH = 2
    DEPOSIT_CHECK = 3
    WITHDRAW = 4
    TRANSFER = 5


class TransactionStatus(Enum):
    SUCCESS = 1
    FAILURE = 2
    BLOCKED = 3
    FULL = 4
    PARTIAL = 5
    NONE = 6


class CustomerStatus(Enum):
    ACTIVE = 1
    BLOCKED = 2
    BANNED = 3
    COMPROMISED = 4
    UNKNOWN = 5


class Address:
    def __init__(self, street, city, state, zip_code, country):
        self.__street_address = street
        self.__city = city
        self.__state = state
        self.__zip_code = zip_code
        self.__country = country


class Customer:
    def __init__(self, name, address, email, phone, status):
        self.__name = name
        self.__address = address
        self.__email = email
        self.__phone = phone
        self.__status = status
        self.__card = Card()
        self.__account = Account

    def make_transaction(self, transaction):
        pass

    def get_billing_address(self):
        pass


class Card:
    def __init__(self, number, customer_name, expiry, pin):
        self.__card_number = number
        self.__customer_name = customer_name
        self.__card_expiry = expiry
        self.__pin = pin

    def get_billing_address(self):
        pass


class Account:
    def __init__(self, account_number):
        self.__account_number = account_number
        self.__total_balance = 0.0
        self.__available_balance = 0.0

    def get_available_balance(self):
        return self.__available_balance


class SavingAccount(Account):
    def __init__(self, account_number, withdraw_limit):
        super().__init__(account_number)
        self.__withdraw_limit = withdraw_limit


class CheckingAccount(Account):
    def __init__(self, debit_card_number, account_number):
        super().__init__(account_number)
        self.__debit_card_number = debit_card_number


class Bank:
    def __init__(self, name, bank_code):
        self.__name = name
        self.__bank_code = bank_code

    def get_bank_code(self):
        return self.__bank_code

    def add_atm(self, atm):
        pass


class ATM:
    def __init__(self, id, location):
        self.__atm_id = id
        self.__location = location

        self.__cash_dispenser = CashDispenser()
        self.__keypad = Keypad()
        self.__screen = Screen()
        self.__printer = Printer()
        self.__check_deposit = CheckDeposit()
        self.__cash_deposit = CashDeposit()

    def authenticate_user(self):
        pass

    def make_transaction(self, customer, transaction):
        pass


class CashDispenser:
    def __init__(self):
        self.__total_five_dollar_bills = 0
        self.__total_twenty_dollar_bills = 0

    def dispense_cash(self, amount):
        pass

    def can_dispense_cash(self):
        pass


class Keypad:
    def get_input(self):
        pass


class Screen:
    def show_message(self, message):
        pass

    def get_input(self):
        pass


class Printer:
    def print_receipt(self, transaction):
        pass


class DepositSlot(ABC):
    def __init__(self):
        self.__total_amount = 0.0

    def get_total_amount(self):
        return self.__total_amount


class CheckDepositSlot(DepositSlot):
    def get_check_amount(self):
        pass


class CashDepositSlot(DepositSlot):
    def receive_dollar_bill(self):
        pass


from abc import ABC, abstractmethod

class Transaction(ABC):
  def __init__(self, id, creation_date, status):
    self.__transaction_id = id
    self.__creation_time = creation_date
    self.__status = status

  def make_transation(self):
    None


class BalanceInquiry(Transaction):
  def __init__(self, account_id):
    self.__account_id = account_id

  def get_account_id(self):
    return self.__account_id


class Deposit(Transaction):
  def __init__(self, amount):
    self.__amount = amount

  def get_amount(self):
    return self.__amount


class CheckDeposit(Deposit):
  def __init__(self, check_number, bank_code):
    self.__check_number = check_number
    self.__bank_code = bank_code

  def get_check_number(self):
    return self.__check_number


class CashDeposit(Deposit):
  def __init__(self, cash_deposit_limit):
    self.__cash_deposit_limit = cash_deposit_limit


class Withdraw(Transaction):
  def __init__(self, amount):
    self.__amount = amount

  def get_amount(self):
    return self.__amount


class Transfer(Transaction):
  def __init__(self, destination_account_number):
    self.__destination_account_number = destination_account_number

  def get_destination_account(self):
    return self.__destination_account_number