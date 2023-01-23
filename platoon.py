import random
from typing import List

import carla.libcarla as carla

from agents.navigation.behavior_agent import BehaviorAgent

# CONFIGURATION
NB_VEHICLES = 5


def main():
    vehicle_list = []
    agent_list = []

    client = carla.Client('localhost', 2000)
    client.set_timeout(20.0)
    try:
        world: carla.World = client.get_world()

        print(world.get_map().name)

        if world.get_map().name != "Carla/map/Town05_Opt":
            world: carla.World = client.load_world('Town05_Opt')

        world.unload_map_layer(carla.MapLayer.All)

        spawn_points = world.get_map().get_spawn_points()
        spawn_point = spawn_points[0]
        destination = random.choice(spawn_points).location

        print('Found %d spawn points.' % len(spawn_points))

        vehicle_bp = world.get_blueprint_library().find('vehicle.audi.a2')
        new_spawn_point = spawn_point

        vehicle_leader = world.spawn_actor(vehicle_bp, new_spawn_point)
        vehicle_leader.set_autopilot(False)
        print(vehicle_leader.id)

        agent = BehaviorAgent(vehicle_leader, behavior='normal')
        agent.ignore_traffic_lights(True)
        agent.ignore_stop_signs(True)

        agent.set_destination(destination)

        agent_list.append(agent)
        vehicle_list.append(vehicle_leader)

        for i in range(NB_VEHICLES - 1):
            vehicle_bp = world.get_blueprint_library().find('vehicle.audi.a2')
            new_spawn_point = spawn_point
            new_spawn_point.location.y = (i + 1) * 10

            vehicle = world.spawn_actor(vehicle_bp, new_spawn_point)
            vehicle.set_autopilot(False)

            agent = BehaviorAgent(vehicle, behavior='normal')
            agent.ignore_traffic_lights(True)
            agent.ignore_stop_signs(True)

            agent_list.append(agent)
            vehicle_list.append(vehicle)

            print('created %s' % vehicle.type_id)
            
        isReached = False
        while not isReached:
            for (vehicle, agent) in zip(vehicle_list, agent_list):
                if agent.done():
                    print("The target has been reached, stopping the simulation")
                    isReached = True
                    break
                if vehicle.id != vehicle_leader.id:
                    agent.set_destination(vehicle_leader.get_location())
                    
                vehicle.apply_control(agent.run_step())


    finally:
        for vehicle in vehicle_list:
            vehicle.destroy()
        print('Finish simulation')


if __name__ == '__main__':
    main()
