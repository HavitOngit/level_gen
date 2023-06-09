from ursina import *
app = Ursina()

from ursina.prefabs.platformer_controller_2d import PlatformerController2d
player = PlatformerController2d(walk_speed=100, x=1000, y=1000, z=.01, scale_x=10, scale_y=10, max_jumps=10, jump_height=50, jump_duretion=1, color=(0, 0, 0, .10))
anime_run = SpriteSheetAnimation('space-marine-run', tileset_size=(11, 1), fps=6, position=player.position, animations={
    'run': ((0, 0), (10, 0)),})


def input(key):
    if key == 'd':
        print('runing...')
        anime_run.play_animation('run')

ground = Entity(model='quad', scale_x=10, collider='box', color=color.black)


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

loc_finder = Entity(model='cube', scale_x=10, scale_y=10, position=player.position, color=color.red)
camera.add_script(SmoothFollow(target=player, offset=[0, 5, -30],speed=4))
player.traverse_target = level_parent
enemy = Entity(model='cube', collider='box', color=color.red, position=(16,5,-.1))

def Pointer_Control():
    if held_keys['w']:
        loc_finder.y +=1
    if held_keys['s']:
        loc_finder.y -=1
    if held_keys['a']:
        loc_finder.x -=1
    if held_keys['d']:
        loc_finder.x +=1
    if held_keys['g']:
        print(loc_finder.position)
def update():

    if player.intersects(enemy).hit:
        print('die')
        player.position = player.start_position
    if held_keys['8']:
        bg.y +=1
    if held_keys['2']:
        bg.y -=1
    if held_keys['4']:
        bg.x -=1
    if held_keys['6']:
        bg.x +=1
    if held_keys['x']:
        bg.scale_x +=10
    if held_keys['z']:
        bg.scale_x -=10
     

    
    print(f'scale:{bg.scale}\nposition{bg.position}')

EditorCamera()
app.run()