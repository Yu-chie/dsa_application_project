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
# INITIALIZE
# ------------------------------
# max_parking_size
# create empty queue
# arrival_counter = 1
# departure_counter = 1

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

# ------------------------------
# OPTION 4: EXIT PROGRAM
# ------------------------------
#   Display "Exiting Program" message
#   Terminate program

# ------------------------------
# END OF PROGRAM
# ------------------------------