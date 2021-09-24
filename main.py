import random
import time
import arcade
global savehi
savehi=0
WIDTH=800
HEITH=600
UPDATES_PER_FRAME = 1

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

class Game(arcade.View):
    save=0
    def __init__(self,savehi=0):
        super().__init__()
        self.player=Dino()
        self.gravity=0.5
        self.center_x=800
        self.ground_list=arcade.SpriteList()
        self.ground_list.append(Ground(400,50))
        self.physics_engine=arcade.PhysicsEnginePlatformer(self.player,self.ground_list,gravity_constant=self.gravity)
        self.time_start=time.time()
        self.time_start2=time.time()
        self.player_list=arcade.SpriteList()
        self.cactos_list = arcade.SpriteList()
        self.birds_list=arcade.SpriteList()
        self.append_player()
        self.x=0
        self.rand = random.randint(1, 5)
        self.cactos_speed=4
        self.color=arcade.color.WHITE
        self.background_color_time=0
        self.savehi=savehi
    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(self.color)
        self.player.draw()
        self.ground_list.draw()
        for i in range(len(self.cactos_list)):
            self.cactos_list[i].draw()
        for i in range(len(self.birds_list)):
            self.birds_list[i].draw()
        arcade.draw_text(f'HI: {self.savehi} , {self.x}',350,500,arcade.color.GRAY,25,bold=True)
    def append_player(self):
        self.player_list.append(self.player)
    def on_update(self, delta_time: float):
        self.physics_engine.update()
        self.player_list.update_animation()
        self.birds_list.update_animation()
        self.time_end=time.time()
        self.time_end2=time.time()
        self.x+=1
        if self.x<1000:
            if self.x>42 and self.time_end-self.time_start>self.rand:
                self.rand=random.randint(1,5)
                self.cactos_list.append(Cactos(80,self.cactos_speed))
                self.time_start=time.time()
            for i in range(len(self.cactos_list)):
                self.cactos_list[i].move()
            for cactos in self.cactos_list:
                if cactos.center_x < 0:
                    cactos.remove_from_sprite_lists()
                elif arcade.check_for_collision(cactos, self.player):
                    self.window.show_view(Gameover(WIDTH, HEITH, self,self.x))

        else:
            for cactos in self.cactos_list:
                if cactos.center_x>=0 and cactos.center_x<800:
                    cactos.remove_from_sprite_lists()
            if len(self.birds_list)==0:
                self.birds_list.append(Birds())
            self.birds_list[0].move()
            if self.birds_list[0].center_x < 0:
                 self.birds_list.pop(0)
            for bird in self.birds_list:
                if arcade.check_for_collision(bird,self.player):
                    self.window.show_view(Gameover(WIDTH, HEITH, self,self.x))

        if self.time_end2-self.time_start2>8:
            self.cactos_speed += 1
            self.time_start2 = time.time()
            if self.background_color_time == 0:
                self.color = arcade.color.BLACK
                self.background_color_time=1
            elif self.background_color_time == 1:
                self.color = arcade.color.WHITE
                self.background_color_time=0

    def on_key_press(self, key, modifiers: int):
        if key==arcade.key.UP and self.physics_engine.can_jump():
            self.player.change_y=1*self.player.jump
            arcade.play_sound(arcade.load_sound(':resources:sounds/jump3.wav'))
        elif key==arcade.key.DOWN:
            self.player.walk_textures=[load_texture_pair('images/dino-bend.png'),load_texture_pair('images/dino-bend.png'),load_texture_pair('images/dino-bend.png'),load_texture_pair('images/dino-bend2.png'),load_texture_pair('images/dino-bend2.png'),load_texture_pair('images/dino-bend2.png')]
    def on_key_release(self, key, _modifiers: int):
        if key==arcade.key.UP:
            self.player.change_y = 0
        elif key == arcade.key.DOWN:
            self.player.walk_textures = [load_texture_pair('images/dino.png'), load_texture_pair('images/dino.png'),
                                  load_texture_pair('images/dino.png')
                , load_texture_pair('images/dino-walk.png'), load_texture_pair('images/dino-walk.png'),
                                  load_texture_pair('images/dino-walk.png')]


class Dino(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture=arcade.load_texture('images/dino.png')
        self.center_x=80
        self.center_y=200
        self.jump=12
        self.cur_texture=0
        self.walk_textures = [load_texture_pair('images/dino.png'),load_texture_pair('images/dino.png'),load_texture_pair('images/dino.png')
            ,load_texture_pair('images/dino-walk.png'),load_texture_pair('images/dino-walk.png'),load_texture_pair('images/dino-walk.png')]
        self.frame=0

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_y>0:
            self.texture = arcade.load_texture('images/dino.png')
            return
        if self.frame>=5:
            self.frame=0
        else:
            self.frame+=1
        self.texture = self.walk_textures[self.frame][0]


class Cactos(arcade.Sprite):
    def __init__(self,y,speed):
        super().__init__()
        self.texture=arcade.load_texture('images/cactos.png')
        self.center_x=800
        self.center_y=y
        self.speed=speed
    def move(self):
        self.center_x-=self.speed
class Birds(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture=arcade.load_texture('images/bird.png')
        self.walk_textures=[load_texture_pair('images/bird.png'),load_texture_pair('images/bird2.png'),load_texture_pair('images/bird3.png')]
        self.frame=0
        self.speed=4
        self.center_x=800
        self.center_y=random.randint(60,200)

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_y>0:
            self.texture = arcade.load_texture('images/bird.png')
            return
        self.frame += 1
        if self.frame>2 :
            self.frame=0

        self.texture = self.walk_textures[self.frame][0]
    def move(self):
        self.center_x-=self.speed
class Ground(arcade.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.texture=arcade.load_texture('images/background.png')
        self.center_x=x
        self.center_y=y
        self.width=800
        self.height=15
        self.speed=4
    def walk_ground(self):
        self.center_x-=self.speed

class Gameover (arcade.View):
    def __init__(self,w,h,gameview,x):
        super().__init__()
        self.center_x=w//2
        self.center_y=h//2
        self.color=arcade.color.BLACK
        self.game_view=gameview
        self.score=x
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE)
        arcade.play_sound(arcade.load_sound(':resources:sounds/gameover4.wav'))
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text('GAME OVER',self.center_x-100,self.center_y,self.color,30,15,bold=True)
        arcade.draw_text('Press the T button to play again',self.center_x-150,self.center_y-50,self.color,20,15)
    def on_key_press(self, key, modifiers: int):
        if key==arcade.key.T:
            self.window.show_view(Game(self.score))
window=arcade.Window(WIDTH,HEITH,'dino game')
game=Game()
window.show_view(game)
arcade.run()