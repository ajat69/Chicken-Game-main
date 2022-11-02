from game.casting.banner import Banner
from game.casting.river import River
from game.casting.road import Road
from game.casting.cast import Cast
from game.casting.lives import Lives
from game.casting.level import Level
from game.casting.chicken import Chicken
from game.casting.animation import  Animation
from game.casting.menu_screen import Menu
from game.casting.help_page import Help
from game.scripting.handle_restart_action import HandleRestartAction
from game.scripting.play_sound_action import PlaySoundAction
from game.casting.car import Car
from game.casting.log import Log
from game.scripting.script import Script
from game.shared.point import Point
from game.casting.image import Image
from game.scripting.control_chicken_action import ControlChickenAction
from game.scripting.move_actors_action import MoveActorsAction
from game.scripting.handle_collisions_action import HandleCollisionsAction
from game.scripting.handle_level_up import HandleLevelUp
from game.scripting.draw_actors_action import DrawActorsAction
from game.directing.director import Director
from game.services.keyboard_service import KeyboardService
from game.services.video_service import VideoService
from game.services.audio_service import RaylibAudioService
from game.scripting.move_car_action import MoveCarAction
from game.scripting.initialize_devices_action import InitializeDevicesAction
from game.scripting.release_devices_action import ReleaseDevicesAction
from game.scripting.load_asset_action import LoadAssetsAction
from game.scripting.unload_assets_action import UnloadAssetsAction
from constants import *

def main():
    
    # create the cast
    cast = Cast()
    size = Point(28, 28)
    animation = Animation(CHICKEN_IMAGES, CHICKEN_RATE)
    
    cast.add_actor("chicken", Chicken(animation, size))
    cast.add_actor("lives", Lives())
    cast.add_actor("level", Level())

    #car images
    car_images = [Image(BLACK_TRUCK), Image(BLACK_CAR), Image(GREEN_CAR), Image(BLUE_CAR), Image(YELLOW_CAR), Image(RED_TRUCK)]
    
    #car lane 1
    cast.add_actor("car", Car(2, CAR_LANE_ONE, car_images, size))
    
    #car lane 2
    cast.add_actor("car", Car(1, CAR_LANE_TWO, car_images, size))
    
    #car lane 3
    cast.add_actor("car", Car(3, CAR_LANE_THREE, car_images, size))
    
    
    
    #Logs
    log_size = Point(35, 28)
    
    #Log images
    log_images = [Image(LONG_PLANK), Image(PLANK), Image(BRANCH)]
    
    #Water Log
    cast.add_actor("log", Log(2, LOG_LANE_THREE, log_images, log_size))
    cast.add_actor("log", Log(1, LOG_LANE_TWO, log_images, log_size))
    cast.add_actor("log", Log(3, LOG_LANE_ONE, log_images, log_size))
    
    
     
    #Banner
    cast.add_actor("banner", Banner())
    
    #Road
    cast.add_actor("road", Road())
 
    #River
    cast.add_actor("river", River())
    

    #Menu
    cast.add_actor("menu", Menu())

    #Menu
    cast.add_actor("help", Help())
    
   
    # start the game
    keyboard_service = KeyboardService() 
    video_service =  VideoService()
    AUDIO_SERVICE = RaylibAudioService()

    script = Script()
    
    script.add_action("input", ControlChickenAction(keyboard_service))
    script.add_action("input", HandleRestartAction(AUDIO_SERVICE, keyboard_service))
    
    script.add_action("load", LoadAssetsAction(AUDIO_SERVICE, video_service))
    script.add_action("initialize", InitializeDevicesAction(AUDIO_SERVICE, video_service))
    
    
    script.add_action("update", MoveActorsAction())
    script.add_action("update", MoveCarAction(AUDIO_SERVICE))
    script.add_action("update", HandleCollisionsAction(AUDIO_SERVICE))
    script.add_action("update", HandleLevelUp(AUDIO_SERVICE))
    
    script.add_action("output", PlaySoundAction(AUDIO_SERVICE, GAME_PLAY_SOUND))
    script.add_action("release", ReleaseDevicesAction(AUDIO_SERVICE, video_service))
    script.add_action("output", DrawActorsAction(video_service))
    script.add_action("unload", UnloadAssetsAction(AUDIO_SERVICE, video_service))
    
    
    director = Director(video_service)
    director.start_game(cast, script)


if __name__ == "__main__":
    main()