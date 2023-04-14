from ursina import *
app = Ursina()

from ursina.prefabs.platformer_controller_2d import PlatformerController2d
player = PlatformerController2d(y=1, z=.01, scale_y=1, max_jumps=4)

ground = Entity(model='quad', scale_x=10, collider='box', color=color.black)


quad = load_model('quad', use_deepcopy=True)


level_parent = Entity(model=Mesh(vertices=[], uvs=[]), texture='white_cube')
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
            if col == color.green:
                player.start_position = (x, y)
                player.position = player.start_position
    print('cordinates are:\n', pos)
    level_parent.model.generate()

make_level(load_texture('level_01'))   # generate the level

camera.orthographic = True
camera.position = (30/2,8)
camera.fov = 500


player.position = (1676, 50)
player.traverse_target = level_parent
enemy = Entity(model='cube', collider='box', color=color.red, position=(16,5,-.1))
def update():
    if player.intersects(enemy).hit:
        print('die')
        player.position = player.start_position


app.run()