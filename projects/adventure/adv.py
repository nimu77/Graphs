from room import Room
from player import Player
from world import World
from util import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# breakpoint()

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def get_all_room_paths(room_id):
    
    visited = {}

    q = Queue()

    q.enqueue([player.current_room.id])

    while q.size() > 0:
        path = q.dequeue()
        room = path[-1]

        if room not in visited:

            visited[room] = True

        # if room == len(room_graph):

        for door in player.current_room.get_exits():
            # breakpoint()
        # for room in player.current_room.get_exits():
            # print(room)
            # if door not in visited:
                # visited[v]= {f'{door}: {player.current_room.{door} +"_to"}'}
                # traversal_path.append(door)
                # visited[room] = {door: player.current_room.get_room_in_direction(door).name[-1]}
                # new_path = list(path)
                # if door in ["n", "s", "e", "w"]:
            # visited[room] = door
            new_path = path + [int(player.current_room.get_room_in_direction(door).name[-1])]
                # new_path.append(int(player.current_room.get_room_in_direction(door).name[-1]))
                # new_path.append(player.travel(door, True))
                # new_path = path + [door]
            g.enqueue(new_path)
            
            

            
                # breakpoint()

# print(traversal_path)
# print(visited)


# print(path)

# print(v)
# print(g.size())


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
