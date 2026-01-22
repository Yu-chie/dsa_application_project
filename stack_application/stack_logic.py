import datetime

class Car:
    def __init__(self, plate_number, slot):
        self.plate_number = plate_number
        self.arrival = datetime.datetime.now().strftime("%I:%M %p")
        self.departure = "---"
        self.slot = slot 

class ParkingManager:
    def __init__(self):
        self.stack = [] # This is your Stack (LIFO)
        self.max_capacity = 10

    def park_car(self, plate):
        if len(self.stack) < self.max_capacity:
            # PUSH: Adding to the top of the stack
            new_car = Car(plate, len(self.stack) + 1)
            self.stack.append(new_car) 
            return new_car, None
        return None, "Garage Full!"

    def exit_car(self):
        if self.stack:
            # POP: Removing from the top (Last-In, First-Out)
            car = self.stack.pop() 
            car.departure = datetime.datetime.now().strftime("%I:%M %p")
            return car
        return None