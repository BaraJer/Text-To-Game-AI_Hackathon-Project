extends Area2D

@export var orientation : Global.ORIENTATION = Global.ORIENTATION.NONE
var scene : int = -1

var just_used = false

func _on_body_entered(body):
	if body.is_in_group("player"):
		if scene == -1:
			return
		if not Global.did_just_transition:
			just_used = true
			Global.change_level(scene)


func _on_body_exited(body):
	if body.is_in_group("player") && not just_used:
		Global.did_just_transition = false
