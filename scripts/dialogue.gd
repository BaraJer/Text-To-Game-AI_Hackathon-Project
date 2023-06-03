extends CanvasLayer

@export var text_speed : float = 0.001
signal dialogue_ended

var char_name = ""
var conv = {}
var state = {}
var state_ind = 0
var d_active = false

enum {PLAYING, DISPLAY, OPTIONS}
var d_stage = DISPLAY

var options_dict = []

func _ready():
	$DialogueBox.visible = false
	$Timer.wait_time = text_speed;

func start(d_file):
	$DialogueBox.visible = true
	$DialogueBox/Text.visible = true
	$DialogueBox/OptionsList.visible = false
	d_active = true	
	
	var data = Global.load_json(d_file)
	char_name = data["name"]
	conv = data["conv"]
	state_ind = 0	
	if "entrypoints" in data:
		for ep in data["entrypoints"]:
			if ep[0] in Global.constraints:
				state_ind = ep[1]
				break
	state = get_state(0)
	$DialogueBox/Title.text = char_name	
	show_state()
	

func show_state():
	$DialogueBox/OptionsList.visible = false
	$DialogueBox/Text.visible = true
	$DialogueBox/Text.text = state["text"]
	$DialogueBox/Text.visible_characters = 0
	d_stage = PLAYING
	while $DialogueBox/Text.visible_characters < len(state["text"]):
		$DialogueBox/Text.visible_characters += 1
		
		$Timer.start()
		await $Timer.timeout
		if d_stage != PLAYING:
			break
	
	$DialogueBox/Text.visible_characters = len(state["text"])
	d_stage = DISPLAY
	
func show_options():
	$DialogueBox/OptionsList.visible = true
	$DialogueBox/OptionsList.clear()
	options_dict = []
	if !state.has("answers") or state["answers"].is_empty():
		end()
		return
	for opt_ind in state["answers"].size():
		var opt = state["answers"][opt_ind]
		if opt.has("condition") and opt["condition"] not in Global.constraints:
			continue
		options_dict.append(opt_ind) 
		$DialogueBox/OptionsList.add_item(opt["option"])
	
	$DialogueBox/Text.visible = false
	$DialogueBox/OptionsList.grab_focus()
	
func end():
	d_active = false
	$DialogueBox.visible = false
	dialogue_ended.emit()
	
func get_ind_from_answer():
	var selected = $DialogueBox/OptionsList.get_selected_items()
	if selected.is_empty():
		return null
	selected = state["answers"][options_dict[selected[0]]]
	if selected.has("set_variable") and "set_variable" not in Global.constraints:
		Global.constraints.append(selected["set_variable"])
	return selected["goto"]

func get_state(index):
	for state in conv:
		if state["index"] == index:
			return state
	printerr("Error: could not find index %d in conversation of %s" % [index, char_name])
	
	
func _input(event):
	if not d_active:
		return
	if event.is_action_pressed("ui_accept"):
		if d_stage == PLAYING:
			d_stage = DISPLAY
			return
		if d_stage == DISPLAY:
			d_stage = OPTIONS
			show_options()
			return
		if d_stage == OPTIONS:
			var selected = get_ind_from_answer()
			if selected == null:
				return
			state_ind = selected
			d_stage = PLAYING
			state = get_state(state_ind)
			show_state()
			
