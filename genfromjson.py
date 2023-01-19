import json


class Vehicle:
    def __init__(self, name):
        self.name = name


f = open("config.json", "r")
jsonContent = f.read()

parsedJson = json.loads(jsonContent)[0]
platoonsJson = parsedJson["Platoon"]
vehiclesJson = parsedJson["Vehicle"]

print(vehiclesJson)

numberOfVehicles = 0
platoons = {}
for key, value in platoonsJson.items():
    platoons[key] = []
    for vehicle in value["_children"]:
        vehicleToAdd = Vehicle(vehicle)

        vehicleToAdd.parent = key

        # check if the vehicle is the leader of the platoon
        if vehicle in value['_delegProv']['leader'][0]:
            vehicleToAdd.role = "Leader"
        else:
            vehicleToAdd.role = "Follower"

        vehicleToAdd.battery = vehiclesJson[vehicle]["_parameters"]["battery"]

        platoons[key].append(vehicleToAdd)

print(platoons)
