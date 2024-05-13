from dataclasses import dataclass, field
from re import finditer, search, findall
from typing import Dict


# Read a line of input from stdin
file_path = input("Path to your file (i.e. path/to/file): ").strip("'")


@dataclass
class Room:
    name: str = "noname"
    furn_count: Dict[str, int] = field(default_factory=dict)
    current_row_no: int = 0
    current_col_start: int = 0
    current_col_end: int = 0

    def __repr__(self):
        return f"{self.name}:\nW: {self.furn_count.get('W', 0)} P: {self.furn_count.get('P', 0)} C: {self.furn_count.get('C', 0)} S: {self.furn_count.get('S', 0)}"


plan = ""

# Open the file in read mode
with open(file_path, "r") as file:
    plan = file.read()

furn_types = "CPSW"
rooms = []
rows = plan.split("\n")
rows.pop(0)
total = {
    "C": 0,
    "P": 0,
    "S": 0,
    "W": 0,
}


# Function to update the room object
def update_room(room, row_no, col_start, col_end, group):
    room.current_row_no = row_no
    room.current_col_start = col_start
    room.current_col_end = col_end
    # Check if the group has a room name
    room_name = search(r"\((.*?)\)", group)
    if room_name:
        room.name = room_name.group(1)

    # Update the furniture in the room
    furniture = findall(r"[CPSW]", group)
    for furn in furniture:
        total[furn] += 1
        room.furn_count[furn] = room.furn_count.get(furn, 0) + 1


# Loop through the rows and update the rooms
for no, row in enumerate(rows):

    found = list(finditer(r"[^/\\|+-]+", row))
    for match in found:
        room_exists = False
        for room in rooms:
            if room.current_row_no + 1 != no:
                continue
            if (
                room.current_col_start == match.start()
                or room.current_col_end == match.end()
                or room.current_col_start - match.start() == 1
                or room.current_col_end - match.end() == 1
                or room.current_col_start - match.start() == -1
                or room.current_col_end - match.end() == -1
            ):
                room_exists = True
                update_room(room, no, match.start(), match.end(), match.group())
        if not room_exists:
            new_room = Room()
            update_room(new_room, no, match.start(), match.end(), match.group())
            rooms.append(new_room)

# Remove the room with the name "noname"
rooms = [r for r in rooms if r.name != "noname"]

# Order rooms by name
rooms = sorted(rooms, key=lambda x: x.name)

# Get total furniture in all rooms
print(
    f"total:\nW: {total.get('W', 0)} P: {total.get('P', 0)} C: {total.get('C', 0)} S: {total.get('S', 0)}"
)

# Print the rooms
for r in rooms:
    print(r)
