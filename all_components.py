import os
import csv
import numpy as np
import statistics

components = [ "resistor", "cap", "inductor"]
currentDir = os.path.dirname(os.path.abspath(__file__))
csvFileName = "dataset.csv"

datasetFilePath = os.path.join(currentDir, csvFileName)
with open(datasetFilePath, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Aspect Ratio", "Fill %", "Horizontal Continuity", "Count", "Component"])

for component in components:
    subPath = os.path.join(currentDir, component)
    csvPath = os.path.join(subPath, "csv")
    
    for i in range(1, 200):
        csvFilePath = os.path.join(csvPath, str(i) + ".csv")
        leftX = 120
        rightX = 0
        topY = 0
        bottomY = 120
        coordinates = 0

        try:
            xValues = []
            yValues = []

            line = 0
            current = []
            gapCount = 0
            lowerBound = []
            upperBound = []
            gapOpen = False

            def vertBreak ():
                yBreak = 0
                for y in range(int(bottomY) + 1, int(topY)):
                    if y not in yValues:
                        yBreak += 1
                return yBreak >= 10
            def detectGap(gapOpen, gapCount, lowerBound, upperBound):
                gapBreak = False
                for k in range(1, len(current)):
                    if current[k] - current[k - 1] > 1:
                        val = current[k] - current[k - 1]
                        1
                    if current[k] - current[k - 1] > 1 and gapOpen == False and abs(line - current[k]) <= 5 and not vertBreak():
                        gapBreak = True
                        gapOpen = True
                        gapCount = gapCount + 1
                        lowerBound.append(current[0])
                        upperBound.append(current[len(current) - 1])
                        break
                    elif current[k] - current[k - 1] > 1 and gapCount > 0:
                        gapBreak = True
                        lowerBound.append(current[0])
                        upperBound.append(current[len(current) - 1])
                if gapBreak == False:
                    gapOpen = False
                return gapOpen, gapCount, lowerBound, upperBound
            with open(csvFilePath, newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    coordinates += 1
                    xValue = float(row[0])
                    yValue = float(row[1])
                    if xValue < leftX:
                        leftX = xValue
                    if xValue > rightX:
                        rightX = xValue
                    if yValue < bottomY:
                        bottomY = yValue
                    if yValue > topY:
                        topY = yValue
                    if xValue not in xValues:
                        xValues.append(xValue)
                        if len(current) > 0:
                            current = sorted(current)
                            gapOpen, gapCount, lowerBound, upperBound = detectGap(gapOpen, gapCount, lowerBound, upperBound)
                            line = statistics.mean(current)
                        current = []
                        current.append(yValue)
                    else:
                        current.append(yValue)
                    if yValue not in yValues:
                        yValues.append(yValue)

            aspectRatio = (topY - bottomY) / (rightX - leftX)
            fill = coordinates / 144


            # Analyzing horizontal continuity
            xCont = True
            xBreak = 0
            xBefore = 0
            xAfter = 0

            for x in range(int(leftX) + 1, int(rightX)):
                if x not in xValues:
                    xBreak += 1
                else:
                    xBefore += 1
                    if xBreak >= 5:
                        xAfter += 1
                if xBreak >= 5 and xBefore >= 5 and xAfter >= 5:
                    xCont = False
                    break
            with open(datasetFilePath, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([aspectRatio, fill, xCont, gapCount, component])
        except FileNotFoundError:
            continue
    print('checking component: ', component)