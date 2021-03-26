from PIL import Image
import numpy as np
import pymysql

numofdata = 5

img = Image.new("RGB", (1000, 400 + numofdata * 300 + 300), "#FFFFFF")

print(img.size)

img.show()

mydb = {
    
}
