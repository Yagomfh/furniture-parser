from dataclasses import dataclass, field
from re import finditer, search, findall
from typing import Dict


# Read a line of input from stdin for the file path and strip any surrounding single quotes
file_path = input("Path to your file (i.e. path/to/file): ").strip("'")


@dataclass  # Define a Room class using the @dataclass decorator
class Room:
    name: str = "noname"  # Default name of the room is "noname"
    furn_count: Dict[str, int] = field(
        default_factory=dict
    )  # Dictionary to count different types of furniture
    current_row_no: int = 0  # Current row number of the room
    current_col_start: int = 0  # Starting column position of the room
    current_col_end: int = 0  # Ending column position of the room

    def __repr__(self):  # Define the string representation of the Room object
        return f"{self.name}:\nW: {self.furn_count.get('W', 0)} P: {self.furn_count.get('P', 0)} C: {self.furn_count.get('C', 0)} S: {self.furn_count.get('S', 0)}"


plan = ""  # Initialize an empty string to hold the plan

# Open the file in read mode and read its content into the plan variable
with open(file_path, "r") as file:
    plan = file.read()

furn_types = "CPSW"  # Define the types of furniture
rooms = []  # Initialize an empty list to hold Room objects
rows = plan.split("\n")  # Split the plan into rows based on newline characters
total = {  # Initialize a dictionary to count total furniture in all rooms
    "C": 0,
    "P": 0,
    "S": 0,
    "W": 0,
}


# Function to update the room object with new data
def update_room(room, row_no, col_start, col_end, group):
    room.current_row_no = row_no  # Update the current row number of the room
    room.current_col_start = (
        col_start  # Update the starting column position of the room
    )
    room.current_col_end = col_end  # Update the ending column position of the room
    room_name = search(
        r"\((.*?)\)", group
    )  # Search for a room name within parentheses in the group
    if room_name:  # If a room name is found
        room.name = room_name.group(1)  # Update the room's name

    furniture = findall(r"[CPSW]", group)  # Find all furniture items in the group
    for furn in furniture:  # Loop through each found furniture item
        total[furn] += 1  # Increment the total count for this furniture type
        room.furn_count[furn] = (
            room.furn_count.get(furn, 0) + 1
        )  # Increment the count for this furniture type in the room


# Loop through each row and update the rooms accordingly
for no, row in enumerate(rows):
    found = list(
        finditer(r"[^/\\|+-]+", row)
    )  # Find all non-separator groups in the row
    for match in found:  # Loop through each match
        room_exists = False  # Initialize a flag to check if the room exists
        for room in rooms:  # Loop through each existing room
            if (
                room.current_row_no + 1 != no
            ):  # Check if the room is in the previous row
                continue
            if (  # Check if the room is adjacent or overlapping with the current match
                room.current_col_start == match.start()
                or room.current_col_end == match.end()
                or room.current_col_start - match.start() == 1
                or room.current_col_end - match.end() == 1
                or room.current_col_start - match.start() == -1
                or room.current_col_end - match.end() == -1
            ):
                room_exists = True  # Set the flag to true if the room exists
                update_room(
                    room, no, match.start(), match.end(), match.group()
                )  # Update the existing room
        if not room_exists:  # If the room does not exist
            new_room = Room()  # Create a new Room object
            update_room(
                new_room, no, match.start(), match.end(), match.group()
            )  # Update the new room with data
            rooms.append(new_room)  # Add the new room to the list of rooms

# Remove rooms with the default name "noname"
rooms = [r for r in rooms if r.name != "noname"]

# Sort the rooms by their name
rooms = sorted(rooms, key=lambda x: x.name)

# Print the total count of each type of furniture
print(
    f"total:\nW: {total.get('W', 0)} P: {total.get('P', 0)} C: {total.get('C', 0)} S: {total.get('S', 0)}"
)

# Print the details of each room
for r in rooms:
    print(r)
