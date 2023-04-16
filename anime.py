from ursina import *
app = Ursina()

player = Entity(model='cube', color=(123, 123, 112, 0.20), scale_x=.70)
player_graphics = SpriteSheetAnimation('space-marine-run', tileset_size=(11, 1), fps=6, animations={
    'run' : ((0,0), (10,0)),
}, position=player.position)
def update():
    global player
    player_graphics.position = player.position
    player_graphics.x = player.x + .10
    print(player_graphics.position.x)
    if held_keys['d']:
        print('d')
        player.x += .10
    if held_keys['a']:
        print('a')
        player.x -= .10
    if held_keys['w']:
        print('w')
        player.y += .10
    if held_keys['s']:
        print('s')
        player.y -= .10
def input(key):
    
    if key == 'd':
        print('runing...')
        print(player_graphics.play_animation('run'))
        player_graphics.play_animation('run')





EditorCamera()
app.run()