import carla
from typing import List

# CONFIGURATION
NB_VEHICLES = 4


def main():
    global client, actor_list
    try:
        actor_list = []

        client = carla.Client('localhost', 2000)
        client.set_timeout(20.0)

        # world: carla.World = client.load_world('Town04_Opt')

        client.start_recorder("recording01.log", True)

        world: carla.World = client.get_world()

        settings: carla.WorldSettings = world.get_settings()
        settings.no_rendering_mode = False
        world.apply_settings(settings)

        print('SETTINGS: ', settings)

        spawn_points: List[carla.Transform] = world.get_map().get_spawn_points()
        spawn_point = spawn_points[0]

        print('Found %d spawn points.' % len(spawn_points))

        for i in range(NB_VEHICLES):
            blueprint_library: carla.BlueprintLibrary = world.get_blueprint_library()
            vehicle_bp: carla.ActorBlueprint = blueprint_library.filter('vehicle')[0]
            new_spawn_point = spawn_point
            new_spawn_point.location.x += -i * 5
            vehicle: carla.Actor = world.spawn_actor(vehicle_bp, new_spawn_point)
            vehicle.set_autopilot(True)
            actor_list.append(vehicle)
            print('created %s' % vehicle.type_id)

        while True:
            for vehicle in actor_list:
                print("Vehicle %s at %s" % (vehicle.type_id, vehicle.get_location()))
                # print(vehicle.get_acceleration())
                # print(vehicle.get_velocity())
            res = input()
            if res == 'q':
                break
    finally:
        client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])
        client.stop_recorder()
        print(client.show_recorder_file_info("recording01.log"))
        print('Finish simulation')


if __name__ == '__main__':
    main()
