import json
import os
import re
from json import JSONDecodeError
from random import *
import openai

import prompts

openai.api_key = #enter openai api key



def get_completion(temp, prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]

    # davinci
    response = openai.Completion.create(model="text-davinci-003", prompt=prompt,
                                        temperature=temp, max_tokens=1024)

    return response["choices"][0]["text"]


def turbo(prompt):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def json_to_dict(data):
    npc_list = data[list(data.keys())[0]]
    extracted_data = []

    for npc in npc_list:
        extracted_data.append({'name': npc['name'], 'conversation': npc['conversation']})

    return extracted_data


def parse_story(text):
    return [{"npc": conv[0], "description": conv[1]} for conv in
            re.findall("[Pp]art \d: *?\n+.*: (.*)\n+.*: (.*)", text)]


def check_dialogue(dialogue, conditions=[], sets=[]):
    """
    Check GOTOS make sense
    Check no given conditions are set

    """
    # Check GOTOS:
    gotos = {opt["goto"] for state in dialogue if "answers" in state for opt in
             state["answers"]}
    indexes = {state["index"] for state in dialogue}
    for goto in gotos:
        if goto not in indexes:
            print("ERROR: Gotos do not match indexes")
            return False

    # Check conditions are not set:
    diag_sets = {opt["set_variable"] for state in dialogue if "answers" in state
                         for opt in
                         state["answers"] if "set_variable" in opt}

    for cond in conditions:
        if cond in diag_sets:
            print("ERROR: Condition is set again!")
            return False

    # Check Sets are made:
    for s in sets:
        if s not in diag_sets:
            print(f"ERROR: Variable {s} not set!")
            return False

    # Check no new conditions
    diag_conds = {opt["condition"] for state in dialogue if "answers" in state
                         for opt in
                         state["answers"] if "condition" in opt}
    for cond in diag_conds:
        if cond not in conditions:
            print(f"ERROR: New undeclared condition {cond}!")
            return False

    return True


rule_directions = {"down": "up", "up": "down", "left": "right", "right": "left"}


def create_room(index, layout, theme, npc, transitions, num_of_room_in_dict):
    room = {"index": index,
            "layout": layout,
            "theme": theme,
            "npc": npc,
            "transitions": transitions,
            "num_of_room_in_dict": num_of_room_in_dict}
    return room


def choose_rooms(dict_of_rooms, num_of_rooms, themes, npcs):
    all_rooms = list()
    curr_num_room = choice(range(len(dict_of_rooms)))
    room = create_room(0, list(dict_of_rooms[curr_num_room].keys())[0],
                       themes[0], npcs[0], {}, curr_num_room)
    all_rooms.append(room)
    num_of_rooms -= 1
    while num_of_rooms > 0:
        did_changed = False
        for i in range(len(all_rooms)):
            if num_of_rooms == 0:
                break
            curr_room = all_rooms[i]
            room_in_dict = dict_of_rooms[curr_room["num_of_room_in_dict"]]
            direct_of_room = list(room_in_dict.values())[0]
            for d in direct_of_room:
                if num_of_rooms == 0:
                    break
                if d not in list(curr_room["transitions"].keys()):
                    rule = rule_directions[d]
                    all_optional_rooms = list()
                    for j, r in enumerate(dict_of_rooms):
                        if rule in list(r.values())[0] and j != curr_room[
                            "num_of_room_in_dict"]:
                            all_optional_rooms.append(j)
                    curr_num_room = choice(all_optional_rooms)
                    curr_room["transitions"][d] = len(all_rooms)
                    new_room = create_room(len(all_rooms),
                                           list(dict_of_rooms[curr_num_room].keys())[0],
                                           themes[len(all_rooms)], npcs[len(all_rooms)],
                                           {rule: curr_room["index"]}, curr_num_room)
                    all_rooms.append(new_room)
                    num_of_rooms -= 1
                    did_changed = True
                    break
        if not did_changed:
            break
    return all_rooms


def final_my_rooms(themes, npcs, background_story):
    dict_of_rooms = {}
    with open('../scenes/layouts.json', 'r') as openfile:
        dict_of_rooms = json.load(openfile)
    num_of_rooms = len(themes)
    all_r = choose_rooms(dict_of_rooms, num_of_rooms, themes, npcs)
    while len(all_r) < num_of_rooms:
        all_r = choose_rooms(dict_of_rooms, num_of_rooms, themes, npcs)
    for r in all_r:
        del r['num_of_room_in_dict']
    with open("./output/init.json", "w") as outfile:
        json.dump({"scenes": all_r, "opening_message": background_story}, outfile)

def add_chars_to_string(string, start_char, end_char):
    string=string.strip()
    if not string.startswith(start_char):
        string = start_char +"\n" + string
    if not string.endswith(end_char):
        string = string + "\n" + end_char
    return string

def append_dialogue(dial1, dial2):
    # Find last index in dial1
    index_offset = max([state["index"] for state in dial1]) + 1
    for state in dial2:
        state["index"] += index_offset
        if "answers" in state:
            for opt in state["answers"]:
                opt["goto"] += index_offset
    dial1 += dial2
    return dial1, index_offset
def recurring_charahcters(conv_tree_arr, story):
    uniques = {}
    for i, (part, conv_tree) in enumerate(zip(story, conv_tree_arr)) :
        if part["npc"] not in uniques:
            uniques[part["npc"]] = [i,conv_tree, [(0, "" if i==0 else f"finished_part_{i}")]]
        else:
            dial1, index_offset = append_dialogue(uniques[part["npc"]][0], conv_tree)
            uniques[part["npc"]][0]=dial1
            uniques[part["npc"]][1].append((index_offset,f"finished_part_{i}" ))







def main():
    parts = 5
    chars = 7
    # Story
    input_prompt = input("Enter an idea for a game: ")
    story_prompt = prompts.story(input_prompt, parts, chars)
    story_string = get_completion(0.5, story_prompt)
    print(story_string + "\n\n")

    story = parse_story(story_string)
    while not story:
        story_string = get_completion(0.5, story_prompt)
        print(story_string + "\n\n")
        story = parse_story(story_string)
    print("created story!")
    ###Bcakground story
    background_story_string = get_completion(1,prompts.backgroud_prompt(story_string))

    ##Main Character
    main_character= get_completion(1,prompts.get_main_character(story_string))
    print(main_character)
    with open(f"./output/background_story.txt", 'w') as outfile:
        json.dump(background_story_string, outfile)
    # Rooms
    # Get unique character:
    conv_tree = 0
    all_convs = {}
    uniques = {}
    for part in story:
        if part["npc"] not in uniques:
            uniques[part["npc"]] = part["description"]

    room_prompt = prompts.room_prompt(uniques)
    themes_str = '["' + get_completion(1, room_prompt)
    # print(f'{themes_str=}')
    themes_lst = themes_str.strip('"]["').split('", "')
    # print(f'{themes_lst=}')
    while len(themes_lst) != len(uniques):
        themes_str = '["' + get_completion(1, room_prompt)
        themes_lst = themes_str.strip('"]["').split('", "')
    final_my_rooms(themes=themes_lst, npcs=list(uniques.keys()),background_story=background_story_string)

    conditions = set()
    conv_tree_string = ""
    for i, part in enumerate(story):
        invalid_tree = True
        while invalid_tree:
            try:

                conv_tree_string = get_completion(0.3,
                                                  prompts.conversation_tree(part['npc'],
                                                                            full_story=story_string,
                                                                            conditions=list(
                                                                                conditions),
                                                                            num_character=i,
                                                                            main_character=main_character))
                conv_tree_string= add_chars_to_string(conv_tree_string, '[',']')

                conv_tree = json.loads(conv_tree_string)
            except JSONDecodeError:
                invalid_tree = True
                print(f"######\n{conv_tree_string}\n######\n\n")
                print("json error")
                continue
            except Exception:
                invalid_tree = True
                print("some error")
                continue

            print(conv_tree_string)
            invalid_tree = not check_dialogue(conv_tree, list(conditions), [f"finished_part_{i}"])
        conditions.update(
            [opt["set_variable"] for state in conv_tree if "answers" in state for opt in
             state if "set_variable" in state])
        if part["npc"] in all_convs:
            diag_full, index_offset = append_dialogue(all_convs[part["npc"]]["conv"], conv_tree)
            all_convs[part["npc"]]["conv"] = diag_full
            if "entrypoints" not in all_convs[part["npc"]]:
                all_convs[part["npc"]]["entrypoints"] = []
            all_convs[part["npc"]]["entrypoints"].insert(0, (f"finished_part_{i}",index_offset))
        else:
            formated_conv = {"name": part["npc"], "conv": conv_tree}
            all_convs[part["npc"]] = formated_conv

    for name, conv in all_convs.items():
        with open(f"./output/dialogue_{name}.json", 'w') as outfile:
            json.dump(conv, outfile)


if __name__ == '__main__':
    main()
    os.system("..\\build\\Hackathon.exe ./output/")
