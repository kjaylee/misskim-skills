# Godot 4.x Sprite Sheet Demo
# Attach to AnimatedSprite2D node

extends AnimatedSprite2D

enum State { IDLE, RUN, JUMP }

var current_state: State = State.IDLE

func _ready():
    # For this demo, assume you've created SpriteFrames in editor
    # with animations: "idle", "run", "jump"
    
    # Alternative: Create programmatically
    if sprite_frames == null:
        create_sprite_frames_from_sheet()
    
    play_state(State.IDLE)
    
    # UI Label
    var label = Label.new()
    label.text = "Godot Sprite Demo\nPress 1: Idle | 2: Run | 3: Jump"
    label.position = Vector2(20, 20)
    label.add_theme_font_size_override("font_size", 16)
    get_parent().add_child(label)

func _input(event):
    if event.is_action_pressed("ui_text_backspace"):  # Fallback keys
        return
    
    if event is InputEventKey and event.pressed:
        match event.keycode:
            KEY_1:
                play_state(State.IDLE)
            KEY_2:
                play_state(State.RUN)
            KEY_3:
                play_state(State.JUMP)

func play_state(state: State):
    if current_state == state and is_playing():
        return
    
    current_state = state
    
    match state:
        State.IDLE:
            play("idle")
        State.RUN:
            play("run")
        State.JUMP:
            play("jump")

# Programmatic sprite frame creation from atlas
func create_sprite_frames_from_sheet():
    var frames = SpriteFrames.new()
    
    # Load sprite sheet (replace with your asset path)
    var atlas_texture = load("res://assets/character_sheet.png")
    if atlas_texture == null:
        push_warning("character_sheet.png not found, using placeholder")
        return
    
    # Define animations
    var animations = {
        "idle": { "frames": [0, 1, 2, 3], "fps": 8.0 },
        "run": { "frames": [4, 5, 6, 7, 8, 9, 10, 11], "fps": 12.0 },
        "jump": { "frames": [12, 13, 14, 15], "fps": 10.0 },
    }
    
    var frame_width = 64
    var frame_height = 64
    var columns = 4
    
    for anim_name in animations.keys():
        frames.add_animation(anim_name)
        frames.set_animation_speed(anim_name, animations[anim_name].fps)
        frames.set_animation_loop(anim_name, anim_name != "jump")
        
        for frame_index in animations[anim_name].frames:
            var atlas = AtlasTexture.new()
            atlas.atlas = atlas_texture
            
            var col = frame_index % columns
            var row = frame_index / columns
            
            atlas.region = Rect2(
                col * frame_width,
                row * frame_height,
                frame_width,
                frame_height
            )
            
            frames.add_frame(anim_name, atlas)
    
    sprite_frames = frames
