"""
QUEUE: Parking Garage Simulator
Vertical Parking using FIFO Queue

Arrival and Departure values represent
the order of entry and exit, not time
"""

# PARKING GARAGE CLASS DEFINITION
class ParkingGarage:
    def __init__(self, max_parking=10):
        self.max_parking = max_parking      # max parking size
        self.queue = [None] * max_parking   # parking queue
        
# OPTION 1: ENQUEUE CAR
    def car_arrives(self):
        # If parking is full
        if None not in self.queue:
            print("Parking Garage is Full")
            return
        
        plate_number = input("Enter Plate Number: ")
        
        car = {
            'plate_number': plate_number,
            'arrival_count': 1,
            'departure_count': "-"
        }
        
        # Enqueue car in first empty slot
        for i in range(self.max_parking):
            if self.queue[i] is None:
                self.queue[i] = car
                break
        
        self.arrival_counter += 1
        print("Car Parked Successfully!")

# OPTION 2: DEQUEUE CAR
    def car_departs(self):
        # If parking is empty
        if all(slots is None for slots in self.queue):
            print("Parking Garage is Empty")
            return
        
        target_plate = input("Enter Plate Number to Depart: ")
        found = False
        
        # Rotate queue
        for _ in range(self.max_parking):
            front_car = self.queue[0]
            
            # Shift front car to back if not target
            for i in range(self.max_parking - 1):
                self.queue[i] = self.queue[i + 1]
            self.queue[self.max_parking - 1] = None  # Temporarily empty last slot

            if front_car is None:
                continue
        
            if front_car['plate_number'] == target_plate and not found:
                front_car['departure_number'] = self.departure_counter
                self.departure_counter += 1
                found = True
                print(f"Car with Plate Number {target_plate} Departed Successfully!.")
                break
            else:
                front_car['departure_number'] = self.departure_counter
                self.departure_counter += 1
                
                # Enqueue back the front car to rear
                for i in range(self.max_parking):
                    if self.queue[i] is None:
                        self.queue[i] = front_car
                        break
                
        if not found:
            print(f"Car with Plate Number {target_plate} Not Found in Garage.")
        
# OPTION 3: DISPLAY PARKING TABLE
    def display_table(self):
        # Display table header
        # : formatting starts ^ center aligned 15 width of column
        print("\n{:^7} | {:^15} | {:^15} | {:^15}".format(
            'Slot', 'Plate Number', 'Arrival No.', 'Departure No.'))
        print("-" * 55)
        
        # Display each car in the queue
        for i in range(self.max_parking):
            car = self.queue[i]
            if car is None:
                print("{:^7} | {:^15} | {:^15} | {:^15}".format(
                    i + 1, 'EMPTY', '-', '-'
                ))
            else:
                print("{:^7} | {:^15} | {:^15} | {:^15}".format(
                    i + 1,
                    car['plate_number'],
                    car['arrival_number'],
                    car['departure_number']
                ))

# MAIN PROGRAM LOOP
garage = ParkingGarage(max_parking=10)  # Set max parking size

while True:
    garage.display_table()
    
    # Display Menu Options
    print("\n===== Parking Garage Menu =====")
    print("1. Car Arrives")
    print("2. Car Departs")
    print("3. Exit")
    choice = input("Enter your choice (1-3): ")
    
    if choice == '1':
        garage.car_arrives()
    elif choice == '2':
        garage.car_departs()
    elif choice == '3':
        print("Exiting Parking Garage Simulator. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 3.")
