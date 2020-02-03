from abc import ABC, abstractmethod

# enum and constants
from enum import Enum
from uuid import UUID
from time import time
import threading


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


class ParkingSpotStatus(Enum):
    AVAILABLE = 'available'
    UNAVAILABLE = 'unavailable'


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


# Parking spot

class ParkingSpot(ABC):

    def __init__(
            self, spot_number, status, base_charge, special_charge,
            spot_type
    ):
        self.spot_number = spot_number
        self.status = status
        self.base_charge = base_charge
        self.special_charge_per_hour = special_charge
        self.type = spot_type
        self.allocated_vehicle = None

    def set_spot_status(self, status):
        self.status = status

    def get_spot_status(self):
        return self.status

    def allocate_vehicle(self, vehicle):
        self.allocated_vehicle = vehicle
        self.set_spot_status(ParkingSpotStatus.UNAVAILABLE)

    def remove_vehicle(self):
        self.allocated_vehicle = None
        self.set_spot_status(ParkingSpotStatus.AVAILABLE)


class CompactSpot(ParkingSpot):

    def __init__(self, spot_number, base_charge, special_charge):
        super().__init__(
            spot_number, ParkingSpotStatus.AVAILABLE, base_charge,
            special_charge, ParkingSpotType.COMPACT
        )


class LargeSpot(ParkingSpot):

    def __init__(self, spot_number, base_charge, special_charge):
        super().__init__(
            spot_number, ParkingSpotStatus.AVAILABLE, base_charge,
            special_charge, ParkingSpotType.COMPACT
        )


class MotorbikeSpot(ParkingSpot):

    def __init__(self, spot_number, base_charge, special_charge):
        super().__init__(
            spot_number, ParkingSpotStatus.AVAILABLE, base_charge,
            special_charge, ParkingSpotType.COMPACT
        )


#  Vehicle

class Vehicle(ABC):
    def __init__(self, vehicle_number, ticket, vehicle_type):
        self.number = vehicle_number
        self.ticket = ticket
        self.type = vehicle_type


class Car(Vehicle):
    def __init__(self, vehicle_number, ticket):
        super().__init__(vehicle_number, ticket, VehicleType.CAR)


class Truck(Vehicle):
    def __init__(self, vehicle_number, ticket):
        super().__init__(vehicle_number, ticket, VehicleType.TRUCK)


class Motorbike(Vehicle):
    def __init__(self, vehicle_number, ticket):
        super().__init__(vehicle_number, ticket, VehicleType.MOTORBIKE)

# Parking ticket


class Ticket:
    def __init__(
            self, gate_number,
            payment_status=ParkingTicketStatus.ACTIVE,
    ):
        self.ticket_number = str(int(time())) + '_' + str(gate_number)
        self.payment_status = payment_status

    def get_payment_status(self):
        return self.payment_status


# Parking floors


class ParkingFloor:
    def __init__(self, floor_number, spot_limits):
        self.number = floor_number
        self.spots = []
        self.spot_sequence_mapping = {}
        self.spot_limits = spot_limits

    def add_spots(self, spot):
        if spot.spot_number in self.spot_sequence_mapping:
            raise Exception('This spot is already present')

        current_len = len(self.spots)

        if current_len == self.spot_limits:
            raise Exception('Maximum limit reached')

        self.spots.append(spot)
        self.spot_sequence_mapping[spot.spot_number] = current_len

    def remove_spot(self, spot):
        if spot.spot_number not in self.spot_sequence_mapping:
            raise Exception('Invalid spot number')

        spot_index = self.spot_sequence_mapping.get(spot.spot_number)

        del self.spot_sequence_mapping[spot.spot_number]

        self.spots.pop(spot_index)

    def get_total_spots(self):
        return len(self.spots)

    def get_available_spots_count(self, spot_type=None):
        count = 0
        for spot in self.spots:
            if spot_type and spot.type != spot_type:
                continue
            if spot.get_spot_status() == ParkingSpotStatus.AVAILABLE:
                count = count+1

        return count

    def get_unavailable_spots_count(self, spot_type=None):
        count = 0
        for spot in self.spots:
            if spot_type and spot.type != spot_type:
                continue
            if spot.get_spot_status() == ParkingSpotStatus.UNAVAILABLE:
                count = count + 1
        return count


class ParkingLot:
    #  singleton ParkingLot to ensure only one object of ParkingLot in the
    #  system
    instance = None

    class __OnlyOne:
        def __init__(self, name, floor_limits):
            self.name = name
            self.addresses = []
            self.contacts = []
            self.floors = []
            self.floor_sequence_mapping = {}
            self.floor_limits = floor_limits
            self.entrance_panels = [1, 2, 3] # for example
            self.exit_panels = [] = [1, 2, 3] # for example
            self.lock = threading.Lock()

        def add_plot_address(self, address):
            self.addresses.append(address)

        def add_contacts(self, contact):
            self.contacts.append(contact)

        def add_floor(self, floor):
            if floor.number in self.floor_sequence_mapping:
                raise Exception('This floor is already present')
            curr_floor_size = len(self.floors)
            if curr_floor_size == self.floor_limits:
                raise Exception('Maximum limit reached')
            self.floors.append(floor)
            self.floor_sequence_mapping[floor.number] = curr_floor_size

        def remove_floor(self):
            # same as spot
            pass

        def get_free_spot(self, spot_type):
            pass

    def __init__(self, name, floor_limit):
        if not ParkingLot.instance:
            ParkingLot.instance = ParkingLot.__OnlyOne(name, floor_limit)
        else:
            ParkingLot.instance.name = name
            ParkingLot.instance.floor_limit = floor_limit

    def __getattr__(self, name):
        return getattr(self.instance, name)


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
        self.parking_lot = ParkingLot(name="XXXX", floor_limit=10)


class Admin(Account):
    def __init__(
            self, username, password, user_details,
            status=AccountStatus.ACTIVE
    ):
        super().__init__(username, password, user_details, status)

    def add_floor(self, floor_number):
        floor = ParkingFloor(floor_number, 100)
        self.parking_lot.add_floor(floor)

    def add_spot(
            self, floor, spot_number, base_charge, special_charge_per_hour,
            spot_type
    ):
        spot = ParkingSpot(
            spot_number, ParkingSpotStatus.AVAILABLE, base_charge,
            special_charge_per_hour, spot_type
        )
        floor.add_spot(spot)


class ParkingAttendant(Account):
    def __init__(
            self, username, password, user_details,
            status=AccountStatus.ACTIVE
    ):
        super().__init__(username, password, user_details, status)

    def generate_ticket(self, vehicle_number, vehicle_type, spot_type):
        ticket = Ticket()
        if vehicle_type == VehicleType.CAR:
            vehicle = Car(vehicle_number, ticket)
        else:
            raise Exception
        spot = self.parking_lot.get_free_spot(spot_type)
        spot.allocate_vehicle(vehicle)
        return {
            'ticket': ticket.ticket_number,
            'spot': spot.spot_number,
        }


