from RPLCD import i2c
from time import sleep 

class LCD:
    def __init__(self) -> None:
        self.__lcdmode = 'i2c'
        self.__cols = 16
        self.__rows = 2
        self.__charmap = 'A00'
        self.__i2c_expander = 'PCF8574'
        self.__address = 0x27
        self.__port = 1
        self.__lcd = i2c.CharLCD(self.__i2c_expander, self.__address, port=self.__port, charmap=self.__charmap, cols=self.__cols, rows=self.__rows)

    def tampil(self, jumlah_value=0, harga_satuan=0):
        self.__lcd.write_string("Jumlah: {}\r\nHarga: Rp{}".format(jumlah_value, harga_satuan*jumlah_value))
        sleep(20)
        self.__lcd.close(clear=True)

    def jumlah(self, Maxjumlah=0):
        self.__lcd.write_string("Jumlah: {}".format(Maxjumlah))
        sleep(15)
        self.__lcd.close(clear=True)      

if __name__ == "__main__":
    lcd = LCD()
    lcd.tampil(40,1000)