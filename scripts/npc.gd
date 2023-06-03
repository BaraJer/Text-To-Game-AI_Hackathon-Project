extends CharacterBody2D

@export_file("*.json") var dialogue = "";


func _on_area_2d_body_entered(body):
	if body.is_in_group("player"):
		body.d_file = dialogue


func _on_area_2d_body_exited(body):
	if body.is_in_group("player") and body.d_file == dialogue:
		body.d_file = ""
