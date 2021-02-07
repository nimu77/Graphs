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
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# list with direction from start to end
traversal_path = []
  
# traversal graph
map_dict = {player.current_room.id: {d: '?' for d in player.current_room.get_exits()}}

# opposite direction 
opposite_dir = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}

# function to get available exits for the current room
def available_exit(room_id):

    '''
    returns a list with the direction for that current room
    or returns an empty list if the current room in on a dead end
    '''
    unvisited_direction = []

    for d in map_dict[room_id]:
        if map_dict[room_id][d] == '?':
            unvisited_direction.append(d)
    return unvisited_direction

# function to traverse until it reaches a dead end
def travel(room_id):
    '''
    travels depth first all the way to the dead end
    '''
    while len(available_exit(room_id)) > 0:
        # randomly choose a direction from a list of available exits
        direction = random.choice(available_exit(room_id))
        # store the current room for a reference
        prev = player.current_room.id
        # travel to the next room
        player.travel(direction)
        # append that direction to the traversal path
        traversal_path.append(direction)
        # check if room exist in the map_dict (traversal graph)
        # if it does not exist add it to the traversal graph i.e map_dict
        if player.current_room.id not in map_dict:
            map_dict[player.current_room.id] = {d: '?' for d in player.current_room.get_exits()}
        # add the prev as the value of the opposite direction that was traversed
        map_dict[player.current_room.id][opposite_dir[direction]] = prev
        # add the current room id as the value for the room that was traversed from
        map_dict[prev][direction] = player.current_room.id
        # update the room to be the new room currently in after traversing
        room_id = player.current_room.id

# function that
def find_target(room_id):
    '''
    returns a room that will be the target
    '''
    # instantiate queue class
    q = Queue()
    # add the current room
    q.enqueue(room_id)

    visited = set()

    while q.size() > 0:
        room = q.dequeue()

        if room not in visited:
            visited.add(room)

            if len(available_exit(room)) > 0:
                return room
            
            for next_room in list(map_dict[room].values()):
                q.enqueue(next_room)

def travel_back(target_room, starting_room):
    '''
    this will return a list containing all the directions to travel in 
    order to get to target room
    '''
    q = Queue()

    q.enqueue([starting_room])

    visited = set()

    final_path = []

    while q.size() > 0:
        path = q.dequeue()

        # print(path)

        room = path[-1]
        # print(room)
        if room not in visited:
            visited.add(room)

            if room == target_room:
                # print(path, room)
                
                final_path = path
                break

            for next_room in list(map_dict[room].values()):
                new_path = path.copy() + [next_room]

                q.enqueue(new_path)
    # print(final_path)
    final_direction = []
    for i in range(len(final_path) - 1):
        for direction in map_dict[final_path[i]]:
            if map_dict[final_path[i]][direction] == final_path[i + 1]:
                final_direction.append(direction)

    return final_direction


while len(map_dict) < len(room_graph):
    travel(player.current_room.id)
    target = find_target(player.current_room.id)
    path = travel_back(target, player.current_room.id)
    for d in path:
        player.travel(d)
        traversal_path.append(d)

# print(player.current_room.id)
# travel(player.current_room.id)
# print(player.current_room.id)
# target = find_target(player.current_room.id)
# print(travel_back(target, player.current_room.id))
# print(find_target(player.current_room.id))
# print(available_exit(player.current_room.id))


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
