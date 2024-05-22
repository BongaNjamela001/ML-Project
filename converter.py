from PIL import Image
import os
import csv

components = ["ac_src", "ammeter", "battery", "cap", "curr_src", "dc_volt_src_1", "dc_volt_src_2", "dep_curr_src", "diode", "gnd_1", "gnd_2", "inductor", "resistor", "voltmeter"]
currentDir = os.path.dirname(os.path.abspath(__file__))
for component in components:
    subPath = os.path.join(currentDir, component)
    for i in range(1, 201):
        imagePath = os.path.join(subPath, str(i) +".bmp")

        try:
            img = Image.open(imagePath)

            csvFolderPath = os.path.join(subPath, "csv")
            csvFilePath = os.path.join(csvFolderPath, str(i) + ".csv")

            width = 120
            height = 120

            with open(csvFilePath, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['X', 'Y'])

            whiterows = []
            for x in range(width):
                for y in range(height):
                    pixelColor = img.getpixel((x, y))
                    if pixelColor == 255:
                        whiterows.append([x,y])
            with open(csvFilePath, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(whiterows)
        except FileNotFoundError:
            1