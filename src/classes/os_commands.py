from os import system
from .lcd_module import LcdModule
from time import sleep
from .json_funcs import get_setup
from .log_info import LogInfo

LCD = LcdModule()

config_json = get_setup()

logging = LogInfo(config_json['main']['log'],
                       config_json['main']['log_level'],
                       config_json['main']['log_path'])


def shutdown_system():
    """100"""
    logging.log_info('system shutting down...')
    LCD.refresh_lcd('code_shutdown')
    sleep(2)
    LCD.lcd_close()
    system("sudo shutdown now")
    exit()


def reboot_system():
    """101"""
    logging.log_info('system rebooting...')
    LCD.refresh_lcd('code_reboot')
    sleep(2)
    LCD.lcd_close()
    system("sudo reboot")
    exit()


def restart_program():
    """102"""
    logging.log_info('program restarting...')
    LCD.refresh_lcd('code_restart_program')
    sleep(2)
    LCD.lcd_close()
    system("sudo systemctl restart cesit_dijitallesme.service")
    exit()


def update_code():
    """103"""
    logging.log_info('code updating...')
    LCD.refresh_lcd('code_update')
    system("cd /home/pi/cesit_dijitallesme/ && git pull")
    LCD.lcd_close()
    system("sudo systemctl restart cesit_dijitallesme.service")
    exit()
