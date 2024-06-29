from gs_usb.gs_usb import GsUsb
from gs_usb.gs_usb_frame import GsUsbFrame
from gs_usb.constants import (
    CAN_EFF_FLAG,
    CAN_ERR_FLAG,
    CAN_RTR_FLAG,
)
import struct

GS_USB_ECHO_ID = 0
GS_USB_NONE_ECHO_ID = 0xFFFFFFFF

GS_CAN_MODE_NORMAL = 0
GS_CAN_MODE_LISTEN_ONLY = (1 << 0)
GS_CAN_MODE_LOOP_BACK = (1 << 1)
#GS_CAN_MODE_TRIPLE_SAMPLE = (1 << 2)
GS_CAN_MODE_ONE_SHOT = (1 << 3)
GS_CAN_MODE_HW_TIMESTAMP = (1 << 4)


statusData = b"\x00\x00\x00\x00\x00\x00\x00\x00"
statusFrame = GsUsbFrame(can_id= 0x108040FE | CAN_EFF_FLAG, data=statusData) #GsUsbFrame(can_id= 0x108040FE, data=data)


current = 10
MAX_CURRENT = 50
value = int((current / MAX_CURRENT) * 1024.0)
print(value)
data7 = (value & 0xFF00) >> 8
data8 = value & 0xFF
print(data7, data8)

current1AData = b"\x01\x03\x00\x00\x00\x00\x00\x14"
current1AFrame = GsUsbFrame(can_id= 0x108180FE  | CAN_EFF_FLAG, data=current1AData)

current10AData = b"\x01\x03\x00\x00\x00\x00\x00\xCC"
current10AFrame = GsUsbFrame(can_id= 0x108180FE  | CAN_EFF_FLAG, data=current10AData)

current20AData = b"\x01\x03\x00\x00\x00\x00\x01\x99"
current20AFrame = GsUsbFrame(can_id= 0x108180FE  | CAN_EFF_FLAG, data=current10AData)

currentBumpData = b"\x01\x03\x00\x00\x00\x00\x03\x33"
currentBumpFrame = GsUsbFrame(can_id= 0x108180FE  | CAN_EFF_FLAG, data=currentBumpData)

voltageData = b"\x01\x00\x00\x00\x00\x00\xC8\x00"
voltageFrame = GsUsbFrame(can_id= 0x108180FE | CAN_EFF_FLAG, data=voltageData)



def main():
    devs = GsUsb.scan()
    if len(devs) == 0:
        print("Can not find gs_usb device")
        return

    dev1 = devs[0]
    dev2 = devs[1]

    print(dev1, dev2)

    dev1.stop()
    dev2.stop()

    if not dev1.set_bitrate(125000):
        print("Can not set bitrate for gs_usb")
        return

    if not dev2.set_bitrate(125000):
        print("Can not set bitrate for gs_usb")
        return
    
    dev1.start(GS_CAN_MODE_NORMAL)
    dev2.start(GS_CAN_MODE_NORMAL)

    count = 0
    count2 = 0
    while True:
        iframe = GsUsbFrame()

        if dev1.read(iframe, 1):
            print("RX1:  {}".format(iframe), count2, count)
            count +=1
            count2 +=1
        
        if dev2.read(iframe, 1):
            print("RX2:  {}".format(iframe), count2, count)
            count +=1
            count2 +=1
        
        if count >= 40 and count2 != 1000:
            dev1.send(statusFrame)
            dev2.send(statusFrame)
            print("send", count2, count)
            count = 0

        if count2 == 1000:
            dev1.send(current20AFrame)
            dev2.send(current20AFrame)
            print("current change to 20A")
        


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # When press keyboard to kill the codes. The usb2can will not auto-stop.It may risk error when you open it next time.
        #So added below code to stop it.
        devs = GsUsb.scan()
        dev1 = devs[0]
        dev1.stop()

        dev2 = devs[1]
        dev2.stop()
        pass