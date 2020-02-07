"""
  Design a shopping cart

"""

# Const Files
import datetime
from uuid import UUID


class ProductCategory:
    ELECTRONIC = 'electronic'
    CLOTHING = 'clothing'
    HOME_KITCHEN = 'home_kitchen'


class CardType:
    VISA = 'visa'
    MASTERCARD = 'master_card'


class AccountStatus:
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class OrderStatus:
    UNSHIPPED = 'unshipped'
    PENDING = 'pending'
    SHIPPED = 'shipped'
    COMPLETED = 'completed'
    CANCELED = 'canceled'


class Address:
    def __init__(self, state, city, country, pin_code, street, contact_number):
        self._state = state
        self._city = city
        self._country = country
        self._pin_code = pin_code
        self._street = street
        self._contact_number = contact_number


class Cards:
    def __init__(
            self, card_number, expire_at, card_holder, card_type, card_provider
    ):
        self._number = card_number
        self._expire_at = expire_at
        self._holder = card_holder
        self._type = card_type
        self._provider = card_provider


class User:
    def __init__(
            self, username: str, first_name: str, last_name: str, email: str,
            phone: str, password: str
    ):
        self._first_name = first_name
        self._last_name = last_name
        self._user_name = username
        self._email = email
        self._phone = phone
        self._password = password
        self._account_status = AccountStatus.ACTIVE
        self._last_login = None
        self.addresses = []
        self.cards = []
        self._default_card = None
        self._default_address = None

    def _set_user_name(self, username):
        self._user_name = username

    def _get_user_name(self):
        return self._user_name

    def _set_email(self, email):
        self._email = email

    def _get_email(self):
        return self._email

    def _set_phone(self, phone):
        self._phone = phone

    def _get_phone(self):
        return self._phone

    def _set_password(self, password):
        self._password = password

    def _get_last_login(self):
        return self._last_login

    def _set_last_login(self, last_login):
        self._last_login = last_login

    def _is_valid_password(self, password):
        return self._password == password

    def add_address(self, address: Address):
        self.addresses.append(address)

    def add_card(self, card: Cards):
        self.cards.append(card)

    def update_default_card(self, card: Cards):
        self._default_card = card

    def update_default_address(self, address: Address):
        self._default_address = address


class Customer(User):
    def __init__(
            self, username: str, first_name: str, last_name: str, email: str,
            phone: str, password: str
    ):
        super().__init__(
            username, first_name, last_name, email, phone, password
        )
        self._cart = Cart()

    def add_review(self, product_id, review):
        return

    def add_rating(self, product_id, rating):
        return

    def add_to_cart(self, product_id, quantity, price):
        item = Item(product_id, quantity, price)
        self._cart.add_item(item)

    def remove_item(self, item):
        self._cart.remove_item(item)


class Seller(User):
    def __init__(
            self, username: str, first_name: str, last_name: str,
            email: str, phone: str, password: str, gstin:str
    ):
        super().__init__(
            username, first_name, last_name, email, phone,
            password
        )
        self.gstin = gstin


class Product:
    def __init__(
            self, product_id, name, price, available_items, category,
            seller, description, item_per_customer=1
    ):
        self._product_id = product_id,
        self._name = name,
        self._price = price,
        self._category = category,
        self._seller = seller,
        self._description = description,
        self._ratings = None
        self._available_items = available_items,
        self._item_per_customer = item_per_customer,
        self._total_review = 0
        self._reviews = []

    def get_product_list(
            self, **filter_args
    ):
        return


class Item:
    def __init__(self, product_id: str, quantity: str, price: float):
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    def update_price(self, price):
        pass


class Cart:
    def __init__(self):
        self._id = UUID()
        self.items = []

    def add_item(self, item: Item):
        self.items.append(item)

    def remove_item(self, item):
        pass

    def update_item(self, item):
        pass

    def get_items(self):
        return self.items

    def check_out(self):
        pass


class Order:
    def __init__(self):
        self._id = UUID()
        self._status = OrderStatus.PENDING
        self._date = str(datetime.datetime.utcnow())
        self.cart_ids = []
        self.order_logs = []

    def send_for_shipment(self, order_id):
        pass

    def add_order_log(self, order_log):
        pass

    def make_payment(self):
        pass


class OrderLog:
    def __init__(self, order_status, created_at):
        self.status = order_status
        self.created_at = created_at


