from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0x27)
#Initialisiere LCD Modul
#'PFC8574' ->Chip des Treibers
#0x27 -> I2C Adresse
lcd.cursor_pos = (0,0)
#Setze Cursor auf Zeile 0 und Spalte 0
lcd.write_string(u'Selam Cesit')
#Schreibe den String von links nach rechts.
lcd.cursor_pos = (1,0)
lcd.write_string(u'ben raspi-cesit')