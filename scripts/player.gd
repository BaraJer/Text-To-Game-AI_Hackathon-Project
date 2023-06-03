extends CharacterBody2D

@export var speed = 100
var d_file : String = ""
var d_active = true


func _ready():
	$Dialogue.visible = true

func _physics_process(delta):
	if d_active:
		player_movement(delta)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func player_movement(delta):
	var anim = $AnimatedSprite2D
	if Input.is_action_pressed("ui_up"):
		velocity.x = 0
		velocity.y = -speed
		anim.play("walk_up")
	elif Input.is_action_pressed("ui_down"):
		velocity.x = 0
		velocity.y = speed
		anim.play("walk_down")
	elif Input.is_action_pressed("ui_right"):
		velocity.x = speed
		velocity.y = 0
		anim.play("walk_right")
	elif Input.is_action_pressed("ui_left"):
		velocity.x = -speed
		velocity.y = 0
		anim.play("walk_left")
	else:
		player_stop()
		
	move_and_slide()

func player_stop():
	velocity.x = 0
	velocity.y = 0
	$AnimatedSprite2D.stop()
		
func _input(event):
	if not d_active:
		return
	if event.is_action_pressed("ui_accept") and d_file != "":
		# Trigger dialogue
		player_stop()
		d_active = false
		$Dialogue.start(d_file) 
 

func _on_dialogue_ended():
	$AfterDialogueTimer.start()
	await $AfterDialogueTimer.timeout
	d_active = true
