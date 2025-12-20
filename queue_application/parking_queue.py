# ==============================
# QUEUE: PARKING GARAGE SIMULATOR
# VERTICAL PARKING (FIFO)
# ==============================

# ------------------------------
# DATA TO STORE FOR EACH CAR
# ------------------------------
# plate_number          -> string (car identifier)
# arrival_number        -> integer (order of arrival)
# departure_number      -> integer or "-" (order of departure)
# parking_slot          -> integer (assigned parking slot vertically)

# ------------------------------
# INITIALIZE VARIABLES
# ------------------------------
max_parking = 10        # max parking size
queue = []              # parking queue
arrival_counter = 1     # counts arrivals
departure_counter = 1   # counts departures

# ------------------------------
# MAIN PROGRAM LOOP
# ------------------------------
# WHILE program is running:
#   Display menu:
#       1. Car Arrives
#       2. Car Departs
#       3. Display Parking Table
#       4. Exit
# Input user choice

while True:
    print("\n===== Parking Garage Menu =====")
    print("1. Car Arrives")
    print("2. Car Departs")
    print("3. Display Parking Table")
    print("4. Exit")
    choice = input("Enter your choice (1-4): ")

# ------------------------------
# OPTION 1: ENQUEUE CAR
# ------------------------------
# IF parking is full:
#   Display "Parking Garage is Full" message
# ELSE:
#   Input plate number
#   Create car record with:
#       Set plate_number = input plate number
#       Set arrival = arrival_counter
#       Set departure = "-"
#       Set parking_slot = queue size + 1
#   ENQUEUE car at REAR
#   arrival_counter += 1
#   Display "Car Parked Successfully" message

    if choice == '1':
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
            queue.append(car)
            arrival_counter += 1
            print("Car Parked Successfully!")

# ------------------------------
# OPTION 2: DEQUEUE CAR
# ------------------------------`
# IF parking is empty:
#   Display "Parking Garage is Empty" message
# ELSE:
#   DEQUEUE car from FRONT
#   Set car's departure = departure_counter
#   departure_counter += 1
#   Display "Car Departed Successfully" message

    elif choice == '2':
        if len(queue) == 0:
            print("Parking Garage is Empty")
        else:
            car = queue.pop(0)
            car['departure_number'] = departure_counter
            departure_counter += 1
            print(f"Car with Plate Number {car['plate_number']} Departed Successfully!")

# ------------------------------
# OPTION 3: DISPLAY PARKING TABLE
# ------------------------------
# IF parking is empty:
#   Display "Parking Garage is Empty" message
# ELSE:
#   Display table header
#       Plate Number | Arrival No. | Departure No. | Parking Slot
#   FOR each car in queue:
#       Display car's plate_number, arrival_number, departure_number, parking_slot

    elif choice == '3':
        if len(queue) == 0:
            print("Parking Garage is Empty")
        else:
            print("\n{:<15} {:<12} {:<14} {:<12}".format('Plate Number', 'Arrival No.', 'Departure No.', 'Parking Slot'))
            print("-" * 55)
            for car in queue:
                print("{:<15} {:<12} {:<14} {:<12}".format(
                    car['plate_number'],
                    car['arrival_number'],
                    car['departure_number'],
                    car['parking_slot']
                ))

# ------------------------------
# OPTION 4: EXIT PROGRAM
# ------------------------------
#   Display "Exiting Program" message
#   Terminate program

# ------------------------------
# END OF PROGRAM
# ------------------------------
