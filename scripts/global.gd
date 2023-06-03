extends Node

const BLOCK_TYPES = ["blocker_main", "ground_main", "blocker_secondary", "ground_secondary"]
const TEXTURE_PATHS = "res://assets/sprites/tileset/%s/%s.png"
const SCENES_PATH = "res://scenes/layouts/%s.tscn"
const INIT_SUBPATH = "init.json"
const DIALOGUE_SUBPATH = "dialogue_%s.json"
const DEFAULT_BASEDIR = "res://data/"
var INIT_PATH = DEFAULT_BASEDIR + INIT_SUBPATH
var DIALOGUE_PATH = DEFAULT_BASEDIR + DIALOGUE_SUBPATH

enum ORIENTATION { NONE,LEFT,RIGHT,UP,DOWN }
var orientation_strings = ["", "left", "right", "up", "down"]

signal update_player_position;

var init_data = {}
var current_scene = 0

# Whether the player just moved between rooms
var did_just_transition = false

var constraints = []

func _ready():
	var args = Array(OS.get_cmdline_args())
	if args.size() != 0 and not OS.is_debug_build():
		
		var basedir = args[0]
		print("RUNNING WITH BASEDIR " % basedir)
		INIT_PATH = basedir.path_join(INIT_SUBPATH)
		DIALOGUE_PATH = basedir.path_join(DIALOGUE_SUBPATH)
		
	init_data = load_json(INIT_PATH)
	get_tree().get_first_node_in_group("message_box").start(init_data["opening_message"])

func _on_load_scene(scene_json):
	var prev_scene = current_scene
	current_scene = scene_json["index"]
	
	# Update transitions and player position	
	var player = get_tree().get_first_node_in_group("player")
	var trans_json = scene_json["transitions"]
	for trans in get_tree().get_nodes_in_group("transitions"):
		var orientation = orientation_strings[trans.orientation]
		if orientation in trans_json:
			var scene_ind = trans_json[orientation]
			trans.scene = scene_ind
			if scene_ind == prev_scene:
				player.position = trans.find_child("SpawnPoint").global_position
	
	# Update tiles
	var tilemap = get_tree().get_first_node_in_group("tilemap")	
	for ind in BLOCK_TYPES.size():
		var block_type = BLOCK_TYPES[ind]
		var newTexture = load(TEXTURE_PATHS % [scene_json["theme"], block_type])
		tilemap.tile_set.get_source(ind).texture = newTexture
	
	# Change NPC:
	var npc = get_tree().get_first_node_in_group("npc")
	var t = get_tree()
	if scene_json["npc"] == "":
		npc.queue_free()
	else:
		npc.dialogue = DIALOGUE_PATH % scene_json["npc"]

		
# Call this to change level - when player enters transition area
func change_level(scene_id):
	# Check that not on first scene
	if current_scene != scene_id:
		did_just_transition = true
	var scene_json = get_scene_json_by_id(scene_id)
	call_deferred("_deferred_change_level", scene_json)

func get_scene_json_by_id(scene_id):
	for scene_json in init_data["scenes"]:
		if scene_json["index"] == scene_id:
			return scene_json
	printerr("Could not find scene index %" % scene_id)

func _deferred_change_level(scene_json):
	var scene_path = SCENES_PATH % scene_json["layout"]
	_change_scene(scene_path)
	_on_load_scene(scene_json)

# Manual scene change (mostly technical)
# Will return new scene node
func _change_scene(scene_path):
	var root = get_tree().root
	var scene_node = root.get_child(root.get_child_count() - 1)
	scene_node.free()
	var scene_res = ResourceLoader.load(scene_path)
	scene_node = scene_res.instantiate()
	root.add_child(scene_node)
	get_tree().current_scene = scene_node
	return scene_node
	
	
func load_json(filepath):
	var json_as_text = FileAccess.get_file_as_string(filepath)
	var json_as_dict = JSON.parse_string(json_as_text)
	return json_as_dict

	
			
