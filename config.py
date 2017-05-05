
HOST = "localhost"
PORT = 4223

DESK_ID = "A"

MODULES = [
    ("MenuModule", "navigation"),
    ("InputModule", "inputs"),
    ("SchedulerModule", "scheduler"),
    ]
MENU_MODULES = [
    ("SensorModule", "sensors"),
    ("LightingModule", "lighting"),
    ("PowerModule", "power"),
    ]

VA_POSITIONS = {
    'a': "Laptop Charger Power",
    'b': "Monitor Power",
    'c': "USB Outlets",
    'd': "Lighting Power",
}

RELAY_POSITIONS = {
    'a': ("Laptop Charger", "Monitor"),
    'b': ("USB Outlets", "Lighting"),
}
