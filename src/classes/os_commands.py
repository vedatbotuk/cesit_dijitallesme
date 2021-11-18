from os import system
from .lcd_module import LcdModule
from time import sleep
from .json_funcs import get_setup
from .log_info import LogInfo
import subprocess

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


def reboot_system():
    """101"""
    logging.log_info('system rebooting...')
    LCD.refresh_lcd('code_reboot')
    sleep(2)
    LCD.lcd_close()
    system("sudo reboot")


def restart_program():
    """102"""
    logging.log_info('program restarting...')
    LCD.refresh_lcd('code_restart_program')
    sleep(2)
    LCD.lcd_close()
    system("sudo systemctl restart cesit_dijitallesme.service")


def update_code():
    """103"""
    logging.log_info('code updating...')
    if subprocess.call(['ping', '-c', '1', 'google.com']) == 0:
        LCD.refresh_lcd('code_update')
        if subprocess.call("cd /home/pi/cesit_dijitallesme && git pull", shell=True) == 0:
            sleep(1)
            LCD.refresh_lcd('update_successfully')
            system("sudo systemctl restart cesit_dijitallesme.service")
        else:
            logging.log_info('Update not successfully, git fails: ')
            LCD.refresh_lcd('not_successfully')
            sleep(2)

    else:
        logging.log_info('No internet')
        LCD.refresh_lcd('no_internet')
        sleep(2)
