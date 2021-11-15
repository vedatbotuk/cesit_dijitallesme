from os import system
from .lcd_module import LcdModule
from time import sleep

LCD = LcdModule()


def shutdown_system():
    """100"""
    LCD.refresh_lcd('code_shutdown')
    sleep(2)
    LCD.lcd_close()
    system("sudo shutdown now")


def reboot_system():
    """101"""
    LCD.refresh_lcd('code_reboot')
    sleep(2)
    LCD.lcd_close()
    system("sudo reboot")


def restart_program():
    """102"""
    LCD.refresh_lcd('code_restart_program')
    sleep(2)
    LCD.lcd_close()
    system("sudo systemctl restart cesit_dijitallesme.service")


def update_code():
    LCD.refresh_lcd('code_update')
    system("cd /home/pi/cesit_dijitallesme/ && git pull")
    LCD.lcd_close()
    system("sudo systemctl restart cesit_dijitallesme.service")
