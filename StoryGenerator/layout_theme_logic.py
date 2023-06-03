import json


def write_scenes_json(npc_list, themes_list):
    shorter_list = npc_list if len(npc_list) <= len(themes_list) else themes_list
    data = {
        "scenes" : [
        {
            "index": 0,
            "layout": "house_second_room",
            "theme": "None",
            "npc": "None",
            "transitions": {"left": 1}
        },
        {
            "index": 1,
            "layout": "house_first_room",
            "theme": "library",
            "npc": "Moo the Mooer",
            "transitions": {"right": 0, "down": 2}
        },
        {
            "index": 2,
            "layout": "house_entrance",
            "theme": "library",
            "npc": "Moo the Mooer",
            "transitions": {"left": 3, "up": 1}
        },
        {
            "index": 3,
            "layout": "road_to_house_entrance",
            "theme": "library",
            "npc": "Moo the Mooer",
            "transitions": {"left": 0, "down": 4, "right": 2}
        },
        {
            "index": 4,
            "layout": "bridges_up_down",
            "theme": "library",
            "npc": "Moo the Mooer",
            "transitions": {"up": 3, "down": 0}
        }
    ]}

    for i in range(len(shorter_list)):
        data["scenes"][i]["npc"] = npc_list[i]
        data["scenes"][i]["theme"] = themes_list[i]

    json_object = json.dumps(data, indent=2)
    print(json_object)
    # Writing to sample.json
    with open("./output/scenes.json", "w") as outfile:
        outfile.write(json_object)
