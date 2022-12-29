import random
import carla
from typing import List
import sys
import os

import pygame
try:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/carla')
except IndexError:
    pass
from agents.navigation.behavior_agent import BehaviorAgent

# CONFIGURATION
NB_VEHICLES = 10


def main():
    global client, actor_list
    try:
        actor_list = []
        agent_list = []
        
        client = carla.Client('localhost', 2000)
        client.set_timeout(20.0)

        #client.start_recorder("recording01.log", True)

        world: carla.World = client.get_world()

        settings = world.get_settings()
        settings.synchronous_mode = True # Enables synchronous mode
        settings.fixed_delta_seconds = 0.05 # Sets the fixed time step
        world.apply_settings(settings)

        print(world.get_map().name)

        if(world.get_map().name != "Carla/map/Town05_Opt"):
            world: carla.World = client.load_world('Town05_Opt')
        
        world.unload_map_layer(carla.MapLayer.All)

        spawn_points: List[carla.Transform] = world.get_map().get_spawn_points()
        spawn_point = spawn_points[0]

        print('Found %d spawn points.' % len(spawn_points))

        for i in range(NB_VEHICLES):
            blueprint_library: carla.BlueprintLibrary = world.get_blueprint_library()
            vehicle_bp: carla.ActorBlueprint = blueprint_library.filter('vehicle')[0]
            new_spawn_point = spawn_point
            new_spawn_point.location.y = i * 10

            vehicle: carla.Actor = world.spawn_actor(vehicle_bp, new_spawn_point)

            agent = BehaviorAgent(vehicle, behavior='normal')
            destination = random.choice(spawn_points).location
            agent.set_destination(destination)
            agent_list.append(agent)

            actor_list.append(vehicle)
            print('created %s' % vehicle.type_id)
        
        clock = pygame.time.Clock()
        while True:
            clock.tick()
            world.tick()

            #vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=-1.0))


            #control = agent.run_step()
            #control.manual_gear_shift = False
            #vehicle.apply_control(control)
            for (vehicle,agent) in zip(actor_list,agent_list):
                print("Vehicle %s at %s" % (vehicle.type_id, vehicle.get_location()))
                # print(vehicle.get_acceleration())
                # print(vehicle.get_velocity())
                if agent.done():
                    print("The target has been reached, stopping the simulation")
                    break
                vehicle.apply_control(agent.run_step())

    
        '''
            for vehicle in actor_list:
                print("Vehicle %s at %s" % (vehicle.type_id, vehicle.get_location()))
                # print(vehicle.get_acceleration())
                # print(vehicle.get_velocity())
            res = input()
            if res == 'q':
                break
        '''
    finally:
        client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])
        #client.stop_recorder()
        #print(client.show_recorder_file_info("recording01.log"))
        for actor in actor_list:
            actor.destroy()
        print('Finish simulation')


if __name__ == '__main__':
    main()