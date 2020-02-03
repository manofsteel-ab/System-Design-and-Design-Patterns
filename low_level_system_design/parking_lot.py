# enum and constants
from enum import Enum


class VehicleType(Enum):
    # supported vehicle
    CAR = 'car'
    TRUCK = 'truck'
    VAN = 'van'
    MOTORBIKE = 'motorbike'


class ParkingSpotType(Enum):
    # available spot type in parking lot
    COMPACT = 'compact'
    LARGE = 'large'
    MOTORBIKE = 'motorbike'
    ELECTRIC = 'electric'


class AccountStatus(Enum):
    # account status of users
    ACTIVE = 'active'
    BLOCKED = 'blocked'
    BANNED = 'banned'


class ParkingTicketStatus(Enum):
    ACTIVE = 'active'
    PAID = 'paid'
    LOST = 'lost'


class ContactType:
    PHONE = 'phone'
    EMAIL = 'email'


# Informational class
class Address:
    # to store address information of PLOT
    def __init__(self, state, city, country, zip_code, street=None):
        self.state = state
        self.city = city
        self.country = country
        self.zip_code = zip_code
        self.street = street


class Contact:
    # TO store contact information of PLOT
    def __init__(self, contact_type, name, value, sequence):
        self.type = contact_type
        self.name = name
        self.value = value
        self.sequence = sequence


class UserDetails:
    # TO store user personal details
    def __init__(self, name, addresses=[], contacts=[]):
        self.name = name
        self.addresses = addresses
        self.contacts = contacts


class Account:
    # to store user account related information
    def __init__(self, username, password, user_details, status):
        self.username = username
        self.password = password
        self.user_info = user_details
        self.status = status


class Admin(Account):
    def __init__(
            self, username, password, user_details,
            status=AccountStatus.ACTIVE
    ):
        super().__init__(username, password, user_details, status)

    # Admin actions

    def add_floors(self, floor):
        pass

    def add_parking_spot(self, floor, spot):
        pass

    def add_entrance(self, entrance):
        pass

    def add_exit(self, exits):
        pass

    def add_parking_display_board(self, floor, display_board):
        pass


class ParkingAttendant(Account):
    def __init__(
            self, username, password, user_details,
            status=AccountStatus.ACTIVE
    ):
        super().__init__(username, password, user_details, status)

    def generate_ticket(self, vehicle):
        pass

    def process_ticket(self, ticket_number):
        pass

    def assign_spot(self, spot, vehicle):
        pass


