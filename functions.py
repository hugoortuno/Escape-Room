def setup_game():
  '''
  Sets up the game.
  Defines the rooms, doors, keys, furniture, staff, and object relations. 
  '''


  #rooms

  game_room = {
      "name": "game room",
      "type": "room",
  }

  bedroom1 = {
      "name": "bedroom1",
      "type": "room",
  }

  bedroom2 = {
      "name": "bedroom2",
      "type": "room",
  }

  living_room = {
      "name": "living room",
      "type": "room",
  }

  outside = {
    "name": "outside"
  }

  dungeon = {
      "name": "dungeon",
      "type": "room",
}
  #doors
  door_a = {
      "name": "door a",
      "type": "door",
  }

  door_b = {
      "name": "door b",
      "type": "door",
  }

  door_c = {
      "name": "door c",
      "type": "door",
  }

  door_d = {
      "name": "door d",
      "type": "door",
  }

  door_e = {
      "name": "door e",
      "type": "door",
  }

  #keys
  key_a = {
      "name": "key for door a",
      "type": "key",
      "target": door_a,
  }

  key_b = {
      "name": "key for door b",
      "type": "key",
      "target": door_b,
  }
  key_c = {
      "name": "key for door c",
      "type": "key",
      "target": door_c,
  }
  key_d = {
      "name": "key for door d",
      "type": "key",
      "target": door_d,
  }

  key_e = {
      "name": "key for door e",
      "type": "key",
      "target": door_e,
  }


  #furniture

  couch = {
      "name": "couch",
      "type": "furniture",
  }

  piano = {
      "name": "piano",
      "type": "furniture",
  }

  queen_bed = {
      "name": "queen bed",
      "type": "furniture",
  }

  double_bed = {
      "name": "double bed",
      "type": "furniture",
  }

  dresser = {
      "name": "dresser",
      "type": "furniture",
  }
  dining_table = {
      "name": "dining table",
      "type": "furniture",
  }

  coffin = {
      "name": "coffin",
      "type": "furniture",
  }


  all_rooms = [game_room, bedroom1, bedroom2, living_room, dungeon, outside]
  all_doors = [door_a,door_b,door_c,door_d, door_e]
  all_keys = [key_a, key_b, key_c, key_d, key_e]
  all_furniture = [couch, piano, queen_bed, double_bed, dresser, dining_table, coffin]

  # define which items/rooms are related
  object_relations = {
      "game room" : [couch, piano, door_a],
      "piano" : [key_a],
      "outside" : [door_e, dungeon],
      "door a" : [game_room, bedroom1, key_a],
      "bedroom1" :[queen_bed, door_a, door_b, door_c],
      "queen bed" : [key_b],
      "door b" : [bedroom2, bedroom1, key_b],
      "outside" : [living_room, door_c],
      "bedroom2" : [double_bed, dresser, door_b],
      "double bed" : [key_c],
      "dresser" :[key_d],
      "living room" : [dining_table, door_c, door_d],
      "door c": [bedroom1, living_room, key_c],
      "door d": [living_room, dungeon, key_d],
      "dungeon": [coffin, door_d, door_e],
      'coffin': [key_e],
      'door e': [dungeon, outside, key_e],
      "dining table": []

  }

  # define game state
  INIT_GAME_STAFF = {
      "current_room" : game_room,
      "keys_collected" : [],
      "target_room" : outside
  }
  return INIT_GAME_STAFF, object_relations



def linebreak():
    """
    Print a line break
    """
    print("\n\n")




def start_game(init_game_staff, object_relations):
    """
    Start the game
    """
    game_state = init_game_staff.copy()

    print("You wake up on a couch and find yourself in a strange house with no windows which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!")
    play_room(game_state, game_state["current_room"], object_relations)



def play_room(game_state, room, object_relations):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print("Congrats! You escaped the room!")
    else:
        print("You are now in " + room["name"])
        intended_action = input("What would you like to do? Type 'explore' or 'examine'?").strip()
        if intended_action == "explore":
            explore_room(room, object_relations)
            play_room(game_state, room, object_relations)
        elif intended_action == "examine":
            examine_item(game_state, input("What would you like to examine?").strip(), object_relations)
        else:
            print("Not sure what you mean. Type 'explore' or 'examine'.")
            play_room(game_state, room, object_relations)
        linebreak()



def explore_room(room, object_relations):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You explore the room. This is " + room["name"] + ". You find " + ", ".join(items))



def get_next_room_of_door(door, current_room, object_relations):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room



def examine_item(game_state, item_name, object_relations):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None

    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You unlock it with a key you have."
                    next_room = get_next_room_of_door(item, current_room, object_relations)
                else:
                    output += "It is locked but you don't have the key."
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.")

    if(next_room and input("Do you want to go to the next room? Ener 'yes' or 'no'").strip() == 'yes'):
        play_room(game_state, next_room, object_relations)
    else:
        play_room(game_state, current_room, object_relations)