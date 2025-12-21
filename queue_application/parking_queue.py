"""
QUEUE: Parking Garage Simulator
Vertical Parking using FIFO Queue

Arrival and Departure values represent
the order of entry and exit, not time
"""

# PARKING GARAGE CLASS DEFINITION
class ParkingGarage:
    def __init__(self, max_parking):
        self.max_parking = max_parking  # max parking size
        self.queue = []                 # parking queue
        self.arrival_counter = 1        # counts arrivals
        self.departure_counter = 1      # counts departures

# OPTION 1: ENQUEUE CAR
    def car_arrives(self):
        # If parking is full
        if len(self.queue) >= self.max_parking:
            print("Parking Garage is Full")
        else:
            plate_number = input("Enter Plate Number: ")
            car = {
                'plate_number': plate_number,
                'arrival_number': self.arrival_counter,
                'departure_number': "-",
                'parking_slot': len(self.queue) + 1
            }
            self.queue.append(car)       # Enqueue FIFO
            self.arrival_counter += 1
            print("Car Parked Successfully!")

# OPTION 2: DEQUEUE CAR
    def car_departs(self):
        # If parking is empty
        if len(self.queue) == 0:
            print("Parking Garage is Empty")
        else:
            # Dequeue car
            car = self.queue.pop(0)
            car['departure_number'] = self.departure_counter
            self.departure_counter += 1
            print(f"Car with Plate Number {car['plate_number']} Departed Successfully!")

# OPTION 3: DISPLAY PARKING TABLE
    def display_table(self):
        # If parking is empty
        if len(self.queue) == 0:
            print("Parking Garage is Empty")
        else:
            # Display table header
            # : formatting starts ^ center aligned 15 width of column
            print("\n{:^10} | {:^10} | {:^10} | {:^10}".format('Plate Number', 'Arrival No.', 'Departure No.', 'Parking Slot'))
            print("-" * 55)
            for car in self.queue:
                print("{:^10} | {:^10} | {:^10} | {:^10}".format(
                    car['plate_number'],
                    car['arrival_number'],
                    car['departure_number'],
                    car['parking_slot']
                ))

# OPTION 4: EXIT PROGRAM
    elif choice == '4':
        print("Exiting Program")
        break       # END OF PROGRAM

# MAIN PROGRAM LOOP
while True:
    # Display Menu Options
    print("\n===== Parking Garage Menu =====")
    print("1. Car Arrives")
    print("2. Car Departs")
    print("3. Display Parking Table")
    print("4. Exit")
    choice = input("Enter your choice (1-4): ")
