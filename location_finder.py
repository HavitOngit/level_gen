from ursina import *
app = Ursina()

from ursina.prefabs.platformer_controller_2d import PlatformerController2d
quad = load_model('quad', use_deepcopy=True)

level_parent = Entity(model=Mesh(vertices=[], uvs=[]), texture='white_cube')
bg = Entity(model='quad', position=(962, 545, 1), scale=(1950, 1080), texture='Level_1_final.png')
assat_layer = Entity( model='quad', position=(962, 545, -1), scale=(1950, 1080), texture='level_1_assate_fnl.png')
def make_level(texture):
    # destroy every child of the level parent.
    # This doesn't do anything the first time the level is generated, but if we want to update it several times
    # this will ensure it doesn't just create a bunch of overlapping entities.
    [destroy(c) for c in level_parent.children]
    pos = []
    for y in range(texture.height):
        collider = None
        for x in range(texture.width):
            col = texture.get_pixel(x,y)

            # If it's black, it's solid, so we'll place a tile there.
            if col == color.black:
                level_parent.model.vertices += [Vec3(*e) + Vec3(x+.5,y+.5,0) for e in quad.generated_vertices] # copy the quad model, but offset it with Vec3(x+.5,y+.5,0)
                level_parent.model.uvs += quad.uvs
                # Entity(parent=level_parent, position=(x,y), model='cube', origin=(-.5,-.5), color=color.gray, texture='white_cube', visible=True)
                if not collider:
                    collider = Entity(parent=level_parent, position=(x,y), model='quad', origin=(-.5,-.5), collider='box', visible=False)
                else:
                    # instead of creating a new collider per tile, stretch the previous collider right.
                    collider.scale_x += 1
                    pos.append(collider.position)
            else:
                collider = None

            # If it's green, we'll place the player there. Store this in player.start_position so we can reset the plater position later.
            #if col == color.green:
                #player.start_position = (x, y)
                #player.position = player.start_position
    print('cordinates are:\n', pos)
    level_parent.model.generate()

make_level(load_texture('level_1_collider_f'))   # generate the level

camera.orthographic = True
camera.position = (0, 0)
camera.fov = 800

loc_finder = Entity(model='cube', scale_x=10, scale_y=10, x=1000, y=1000,z=-2, color=color.red)
camera.add_script(SmoothFollow(target=loc_finder, offset=[0, 5, -30],speed=4))
#player.traverse_target = level_parent
move_spd = 1
def Pointer_Control():
    global move_spd
    if held_keys['w']:
        loc_finder.y +=move_spd
    if held_keys['s']:
        loc_finder.y -=move_spd
    if held_keys['a']:
        loc_finder.x -=move_spd
    if held_keys['d']:
        loc_finder.x +=move_spd
    if held_keys['g']:
        print(loc_finder.position)
    if held_keys['shift']:
        move_spd = 10
    else:
        move_spd = 1



def update():
    Pointer_Control()

EditorCamera()
app.run()