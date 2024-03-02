# TODO:
# Enable Multithreading for parallel collection and processing

import serial

def serialInit():
    print("Initializing serial connection")

    ser = serial.Serial('COM3', 9600, timeout=1, bytesize=8, parity='N', stopbits=1)

    print(ser.name)

    return ser

# Not currently used in single threaded version
def serialLoop(ser):
    count = 0

    while count < 100:

        data = ser.read(9)
        dataHex = data.hex()
        print("Read {}: str: {}, hex: {}".format(count, data, dataHex))
        count += 1


def serialRead(ser):
    bytesList = []
    data = ser.read(9)

    for byte in data:
        bytesList.append(byte)
        # print(byte)

    return bytesList


def bytesDecode(bytesList):
    # mapping to variables (probably a more elegant way to do this)
    dataLength = bytesList[0] # should always be 7
    pageNumber = bytesList[1] # should always be 5
    status = bytesList[2] # 00 = emission off, 01 = emission 25uA, 10 = emission 5mA, 11 = degas
    errorByte = bytesList[3]
    measurementHi = bytesList[4]
    measurementLo = bytesList[5]
    softwareVer = bytesList[6]
    sensorType = bytesList[7]
    checkSum = bytesList[8]

    # put error checking here


    return status, measurementHi, measurementLo


def calculatePressure(measurementHi, measurementLo):
    pMbarr = pow(10, (((measurementHi * 256) + measurementLo)/(4000))-12.5)

    return pMbarr


def main():
    ser = serialInit()

    bytesList = serialRead(ser)

    status, measurementHi, measurementLo = bytesDecode(bytesList)

    print(calculatePressure(measurementHi, measurementLo))






if __name__ == "__main__":
    main()