extends CanvasLayer

@export var text_speed : float = 0.001
signal dialogue_ended


enum {PLAYING, DISPLAY, OPTIONS}
var d_stage = DISPLAY

func _ready():
	$Timer.wait_time = text_speed;

func start(text):
	$DialogueBox.visible = true
	$DialogueBox/Text.visible = true
	$DialogueBox/Text.text = text
	$DialogueBox/Text.visible_characters = 0
	d_stage = PLAYING
	while $DialogueBox/Text.visible_characters < len(text):
		$DialogueBox/Text.visible_characters += 1
		
		$Timer.start()
		await $Timer.timeout
		if d_stage != PLAYING:
			break
	
	$DialogueBox/Text.visible_characters = len(text)
	d_stage = DISPLAY

	
func _input(event):
	if event.is_action_pressed("ui_accept"):
		if d_stage == PLAYING:
			d_stage = DISPLAY
			return
		if d_stage == DISPLAY:
			Global.change_level(0)
			
