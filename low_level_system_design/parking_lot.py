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
    def __init__(
            self, vehicle_number, vehicle_type, ticket=None, color=None
    ):
        self.number = vehicle_number
        self.type = vehicle_type
        self.ticket = ticket
        self.color = color

    def assign_ticket(self, ticket):
        self.ticket = ticket


class Car(Vehicle):
    def __init__(self, vehicle_number, ticket=None):
        super().__init__(vehicle_number, VehicleType.CAR, ticket=ticket)


class Truck(Vehicle):
    def __init__(self, vehicle_number, ticket=None):
        super().__init__(vehicle_number, VehicleType.TRUCK, ticket=ticket)


class Motorbike(Vehicle):
    def __init__(self, vehicle_number, ticket=None):
        super().__init__(vehicle_number, VehicleType.MOTORBIKE, ticket=ticket)


class VehicleFactory:

    @classmethod
    def get_vehicle(cls, vehicle_number, vehicle_type):
        if vehicle_type == VehicleType.CAR:
            return Car(vehicle_number)
        if vehicle_type == VehicleType.TRUCK:
            return Truck(vehicle_number)
        if vehicle_type == VehicleType.MOTORBIKE:
            return Motorbike(vehicle_number)
        else:
            raise Exception("Unsupported vehicle type")

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

    def get_available_spots_count(self, spot_types=[]):
        count = 0
        for spot in self.spots:
            if spot_types and spot.type not in spot_types:
                continue
            if spot.get_spot_status() == ParkingSpotStatus.AVAILABLE:
                count = count+1

        return count

    def get_unavailable_spots_count(self, spot_types=[]):
        count = 0
        for spot in self.spots:
            if spot_types and spot.type not in spot_types:
                continue
            if spot.get_spot_status() == ParkingSpotStatus.UNAVAILABLE:
                count = count + 1
        return count

    def get_first_free_spot(self, spot_type_list=[]):
        for spot in self.spots:
            if spot.type in spot_type_list:
                return spot
        return None

    @property
    def is_full(self):
        for spot in self.spots:
            if spot.status == ParkingSpotStatus.AVAILABLE:
                return False
        return True


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
            pass

        def get_free_spot(self, spot_types=[]):
            for floor in self.floors:
                free_spot = floor.get_first_free_spot(spot_type_list=spot_types)
                if free_spot:
                    return free_spot
            raise Exception("No available slots")

        def generate_ticket(self, vehicle_number, vehicle_type):
            if self.is_full:
                raise Exception("Parking full")
            self.lock.acquire()
            ticket = Ticket()
            vehicle = VehicleFactory.get_vehicle(vehicle_number, vehicle_type)
            vehicle.assign_ticket(ticket)
            first_free_spot = self.get_free_spot(
                self._spot_types(vehicle_type)
            )
            first_free_spot.allocate_vehicle(vehicle)
            self.lock.release()

        def _spot_types(self, vehicle_type):
            if vehicle_type == VehicleType.MOTORBIKE:
                return [
                    VehicleType.CAR, VehicleType.TRUCK, VehicleType.MOTORBIKE
                ]
            if vehicle_type == VehicleType.CAR:
                return [VehicleType.TRUCK, VehicleType.CAR]
            if vehicle_type == VehicleType.MOTORBIKE:
                return [VehicleType.MOTORBIKE]
            return []

        @property
        def is_full(self):
            for floor in self.floors:
                if not floor.is_full:
                    return False
            return True

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
        self.parking_lot = ParkingLot(name="XXXX", floor_limit=10).instance


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

    def generate_ticket(self, vehicle_number, vehicle_type):
        parking_lot = self.parking_lot
        return parking_lot.generate_ticket(vehicle_number, vehicle_type)



