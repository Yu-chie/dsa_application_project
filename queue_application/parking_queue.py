"""
QUEUE: Parking Garage Simulator
Vertical Parking using FIFO Queue

Arrival and Departure values represent
the order of entry and exit, not time
"""

# ------------------------------
# DATA TO STORE FOR EACH CAR
# ------------------------------
# plate_number          -> string (car identifier)
# arrival_number        -> integer (order of arrival)
# departure_number      -> integer or "-" (order of departure)
# parking_slot          -> integer (assigned parking slot vertically)

# INITIALIZE VARIABLES
max_parking = 10        # max parking size
queue = []              # parking queue
arrival_counter = 1     # counts arrivals
departure_counter = 1   # counts departures


# MAIN PROGRAM LOOP
while True:
    # Display Menu Options
    print("\n===== Parking Garage Menu =====")
    print("1. Car Arrives")
    print("2. Car Departs")
    print("3. Display Parking Table")
    print("4. Exit")
    choice = input("Enter your choice (1-4): ")

# OPTION 1: ENQUEUE CAR
    if choice == '1':
        # If parking is full
        if len(queue) >= max_parking:
            print("Parking Garage is Full")
        else:
            plate_number = input("Enter Plate Number: ")
            car = {
                'plate_number': plate_number,
                'arrival_number': arrival_counter,
                'departure_number': "-",
                'parking_slot': len(queue) + 1
            }
            queue.append(car)       # Enqueue FIFO
            arrival_counter += 1
            print("Car Parked Successfully!")

# OPTION 2: DEQUEUE CAR
    elif choice == '2':
        # If parking is empty
        if len(queue) == 0:
            print("Parking Garage is Empty")
        else:
            # Dequeue car
            car = queue.pop(0)
            car['departure_number'] = departure_counter
            departure_counter += 1
            print(f"Car with Plate Number {car['plate_number']} Departed Successfully!")

# OPTION 3: DISPLAY PARKING TABLE
    elif choice == '3':
        # If parking is empty
        if len(queue) == 0:
            print("Parking Garage is Empty")
        else:
            # Display table header
            # : formatting starts ^ center aligned 15 width of column
            print("\n{:^10} | {:^10} | {:^10} | {:^10}".format('Plate Number', 'Arrival No.', 'Departure No.', 'Parking Slot'))
            print("-" * 55)
            for car in queue:
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

