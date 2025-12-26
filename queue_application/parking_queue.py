"""
QUEUE: Parking Garage Simulator
Vertical Parking using FIFO Queue

Arrival and Departure values represent
the order of entry and exit, not time
"""

import os

class FileManager:
    def __init__(self, folder='queue_application', default_file='parking_records.txt'):
        self.folder = folder
        self.default_file = default_file
        os.makedirs(self.folder, exist_ok=True) # Ensure folder exists
        
    # Choose to create a new file or use an existing file
    def setup_records_file(self):
        print("Choose Records File Option:")
        print("1. Create New File")
        print("2. Use an existing file")
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == '1':
            file_name = input("Enter new filename: ").strip()
            if not file_name:
                file_name = self.default_file
            elif not file_name.endswith(".txt"):
                file_name += ".txt"
                
        elif choice == '2':
            file_name = input("Enter existing filename: ").strip()
            if not file_name.endswith(".txt"):
                file_name += ".txt"
            if not os.path.exists(os.path.join(self.folder, file_name)):
                print("File does not exist. Using default file instead.")
        else:
            print("Invalid choice. Using default file.")
            file_name = self.default_file
        
        self.file_path = os.path.join(self.folder, file_name)
        
        # Create File if it doesnt exist
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                file.write("Plate Number | Arrival Count | Departure Count\n")
                file.write("-" * 50 + "\n")
                
        return self.file_path

    # Load existing records from file
    def load_records(self):
        records = {}
        try:
            with open(self.records_file, 'r') as file:
                next(file)  # Skip header
                next(file)  # Skip separator
                for line in file:
                    plate_number, arrival_count, departure_count = line.strip().split(' | ')
                    self.records[plate_number] = {
                        'plate_number': plate_number,
                        'arrival_count': int(arrival_count),
                        'departure_count': int(departure_count)
                    }
        except FileNotFoundError:
            pass  # No existing records file
        return records
        
    # Method to save all records in a file
    def save_records(self):
        with open(self.records_file, 'w') as file:
            file.write("Plate Number | Arrival Count | Departure Count\n")
            file.write("-" * 50 + "\n")
            for car in self.records.values():
                file.write(f"{car['plate_number']} | {car['arrival_count']} | {car['departure_count']}\n")
        
# PARKING GARAGE CLASS DEFINITION
class ParkingGarage:
    def __init__(self, max_parking=10, records_file='parking_records.txt'):
        self.max_parking = max_parking      # max parking size
        self.queue = [None] * max_parking   # parking queue'
        self.records = {}                   # to track all car records
        self.records_file = records_file    # file to save records
        
    # OPTION 1: ENQUEUE CAR
    def car_arrives(self):
        # If parking is full
        if None not in self.queue:
            print("Parking Garage is Full")
            return
        
        plate_number = input("Enter Plate Number: ")
        
        # Prevent duplicate entries
        for car in self.queue:
            if car is not None and car['plate_number'] == plate_number:
                print("Car with this Plate Number is already in the Garage.")
                return
        
        # If car already has a record, update arrival count
        if plate_number in self.records:
            car = self.records[plate_number]
            car['arrival_count'] += 1
        # If new car, create record
        else:
            car = {
                'plate_number': plate_number,
                'arrival_count': 1,
                'departure_count': 0
            }
            self.records[plate_number] = car
         
        # Enqueue car in first empty slot
        for i in range(self.max_parking):
            if self.queue[i] is None:
                self.queue[i] = car
                break
        
        print("Car Parked Successfully!")
        self.save_records()

    # OPTION 2: DEQUEUE CAR
    def car_departs(self):
        # If parking is empty
        if all(slots is None for slots in self.queue):
            print("Parking Garage is Empty")
            return
        
        target_plate = input("Enter Plate Number to Depart: ")
        found = False
        
        # Find target car index
        target_index = None
        for i, car in enumerate(self.queue):
            if car is not None and car['plate_number'] == target_plate:
                target_index = i
                break
            
        if target_index is None:
            print(f"Car with Plate Number {target_plate} Not Found in Garage.")
            return
        
        # Cars in front temporarily leave
        temp_queue = []
        for i in range(target_index):
            car = self.queue[i]
            if car is not None:
                # Temporary exit and re-entry
                car['departure_count'] += 1
                car['arrival_count'] += 1
                temp_queue.append(car)
            
        # target car leaves permanently
        target_car = self.queue[target_index]
        target_car['departure_count'] += 1
        print(f"Car with Plate Number {target_plate} Departed Successfully!")
                
        # Shift cars behind forward
        new_queue = self.queue[target_index + 1:self.max_parking]   # cars after target
        new_queue = [c for c in new_queue if c is not None]         # remove None values
        new_queue.extend(temp_queue)                                # add temporarily exited cars
        new_queue += [None] * (self.max_parking - len(new_queue))   # fill remaining with None
        self.queue = new_queue
        self.save_records()

    # OPTION 3: DISPLAY PARKING TABLE
    def display_table(self):
        # Display table header
        # : formatting starts ^ center aligned 15 width of column
        print("\n{:^7} | {:^20} | {:^20} | {:^20}".format(
            'Slot', 'Plate Number', '# of Arrival.', '# of Departure.'))
        print("-" * 70)
        
        # Display each car in the queue
        for i in range(self.max_parking):
            car = self.queue[i]
            if car is None:
                print("{:^7} | {:^20} | {:^20} | {:^20}".format(
                    i + 1, '-', '-', '-'
                ))
            else:
                print("{:^7} | {:^20} | {:^20} | {:^20}".format(
                    i + 1,
                    car['plate_number'],
                    car['arrival_count'],
                    car['departure_count']
                ))

    # MAIN PROGRAM LOOP
    def run(self):
        while True:
            self.display_table()
            
            # Display Menu Options
            print("\n===== Parking Garage Menu =====")
            print("1. Car Arrives")
            print("2. Car Departs")
            print("3. Exit")
            choice = input("Enter your choice (1-3): ")
            
            if choice == '1':
                self.car_arrives()
            elif choice == '2':
                self.car_departs()
            elif choice == '3':
                print("Exiting Parking Garage Simulator. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")

if __name__ == "__main__":
    records_file_path = setup_records_file() # Setup records file
    garage = ParkingGarage(records_file=records_file_path) # Create ParkingGarage instance
    garage.load_records()
    garage.run()