MARY_CONV_NO_COND = """
Name: Mary
[
	{
		"index": 0,
		"text": "Hello How are you? are you Ok?",
		"answers": [{"option": "yes im good", "goto": 1}, {"option": "no so well", "goto": 2}]
	},
	{
		"index": 1,
		"text": "Nice to hear that you are well. Do you want to get a key?",
		"answers": [{"option": "yes id like to get a key", "goto": 3, "set_variable":"has_key"}, {"option": "no", "goto": 4}]

	},
	{
		"index": 2,
		"text": "Im sad you arent feeling well, what can I do to help you?",
		"answers": [{"option": "nothing", "goto": 4}, {"option": "Open the door", "goto": 5}]
	},
	{
		"index": 3,
		"text": "Ok here you go, You can have this key",
		"answers": [{"option": "Thank you!", "goto": 6}]
	},
	{
		"index": 4,
		"text": "Ok Bye!"
	},
	{
		"index": 5,
		"text": "To open the door you need to have a key, do you have the key?",
		"answers": [{"option": "no i dont have the key", "goto": 7}, {"option": "Yes i have the key!", "goto": 8, "condition": "has_key"}]
	},
	{
		"index": 6,
		"text": "You are welcome!"
	},
	{
		"index": 7,
		"text": "I cannot help you. Come back when you have a key!"
	},
	{
		"index": 8,
		"text": "Hooray! You have the key so now I can open the door. Do you want to get a prize?",
		"answers": [{"option": "no i dont need a prize", "goto": 4}, {"option": "Yes i want a prize!", "goto": 9, "set_variable": "has_prize"}]
	},
	{
		"index": 9,
		"text": "There you go, here is a prize! bye! it was nice doing business with you"
	}
]
"""
MIKE_CONV_INCLUDES_CONDITIONS = """This is the conversation with the NPC "Mike",
The conditions are ["has_key", "has_money"]
 [
	{
		"index": 0,
		"text": "Hello How are you? are you Ok?",
		"answers": [{"option": "yes im good", "goto": 1}, {"option": "no so well", "goto": 2}]
	},
	{
		"index": 1,
		"text": "Nice to hear that you are well. Do you want to get a mushroom?",
		"answers": [{"option": "yes id like to get a key", "goto": 3, "set_variable":"has_mushroom"}, {"option": "no", "goto": 4}]

	},
	{
		"index": 2,
		"text": "Im sad you arent feeling well, what can I do to help you?",
		"answers": [{"option": "nothing", "goto": 4}, {"option": "Open the door", "goto": 5}]
	},
	{
		"index": 3,
		"text": "Ok here you go, You can have this mushroom",
		"answers": [{"option": "Thank you!", "goto": 6}]
	},
	{
		"index": 4,
		"text": "Ok, do you have money?",
                "answers": [{"option": "no", "goto": 10}, {"condition": "has_money", "option": "yes", "goto": 11}, ]
	},
	{
		"index": 5,
		"text": "To open the door you need to have a key, do you have the key?",
		"answers": [{"option": "no i dont have the key", "goto": 7}, {"condition": "has_key", "option": "Yes i have the key!", "goto": 8}]
	},
	{
		"index": 6,
		"text": "You are welcome!"
	},
	{
		"index": 7,
		"text": "I cannot help you. Come back when you have a key!"
	},
	{
		"index": 8,
		"text": "Hooray! You have the key so now I can open the door. Do you want to get a prize?",
		"answers": [{"option": "no i dont need a prize", "goto": 4}, {"option": "Yes i want a prize!", "goto": 9, "set_variable": "has_prize"}]
	},
	{
		"index": 9,
		"text": "There you go, here is a prize! bye! it was nice doing business with you"
	},
        {
		"index": 10,
		"text": "Aw, thats too bad, I hope you find money. Bye!"
	},
        {
		"index": 11,
		"text": "Nice to hear you have money! Do you want to buy a sandwich?",
		"answers": [{"option": "No thanks!", "goto": 12}, {"option": "Oh yes please!", "goto": 13, "set_variable": "ate_sandwich"}]
	},
        {
		"index": 12,
		"text": "Ok, Bye!"
	},
        {
		"index": 11,
		"text": "Bless you! Have a good day!"
	},
]
"""
THEMES = ["beach", "castle", "dangerous_path", "garden", "garden_black", "kitchen", "library", "space", "street"]
LAYOUTS = []

OBJECTIVES= []
"""condition: """
def story(prompt, parts, characters):
    return f"""Given the following prompt, build a game that consists of {parts} parts, each part containing the following:

1) Non-playable character
2) Conversation idea between the player and the non-playable character. All the conversation ideas must revolve around the main story that was inspired by the given prompt. Each part must progress with the story until the last part of the game, which will be about the conclusion of the story. 

Do it in the following steps:

1) Write a story that is intended for adults. the stroy theme should be interesting and in the style of George R. R. Martin writings. The story must have an interesting twist. and it must be decently plotted.

2) Divide the story into {parts} parts. Each part should include an interaction with a non-playable character, and the interaction must revolve around the main story. The first part should serve as an introduction to the story/game, and the last part should wrap up the story/game.

The prompt: {prompt}


"""


def story_json(prompt):
    text = f"""{prompt}

JSON:

"""
    return text




def room_prompt(characters):
    # REMEMBER TO ADD Opening Brackets
    text = "\n\n".join([f"Non-Playable Character: {chr[0]}\nConversation: {chr[1]}" for chr in list(characters.items())])
    text += "\n\nOut of the following, in which it is most likely for the conversation with each NPC to take place?\n\n"
    text += "\n".join(THEMES)
    text+="\n\nwrite in python list\n\n[\""
    return text

def conversation_tree(charachter_name, full_story, conditions,
                      num_character, main_character):
    text_conditions=""
    if conditions:
        text_conditions += MIKE_CONV_INCLUDES_CONDITIONS
    else:
        text_conditions += MARY_CONV_NO_COND

    text_conditions+= "\n\nThis is a new game story:"
    text_conditions+= full_story+"\n\n"
    text_conditions+= f"the main character is: {main_character}\n"
    text_conditions+=f'This is the conversation with the NPC "{charachter_name}":\n'
    if conditions:
        text_conditions+= f"you may use conditions from the following: {conditions}\n"
    text_conditions+=f'the variable "finished_part_{num_character}" must be set (using "set_variable")' \
                     f' at some point during the conversation.'
    return text_conditions

def backgroud_prompt(story):
    text= f"generate a short ryming background for the story. the story is an RPG game story. " \
          f"the background will be displayed before starting the game.\n\n" \
          f"story: '''{story}'''"
    return text

def get_main_character(story):
    text = f"give a name and description for the main character of the RPG game." \
           f"the game is built by parts, the main character speaks in each part " \
           f"with a different NPC\n" \
           f"story:\n" \
           f"'''{story}'''\n" \
           f"the format is CHARACTER_NAME: FEW_WORDS_DESCRIPTION\n\n"
    return text