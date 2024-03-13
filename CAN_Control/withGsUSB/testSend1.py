import time

from gs_usb.gs_usb import GsUsb
from gs_usb.gs_usb_frame import GsUsbFrame
from gs_usb.constants import (
    CAN_EFF_FLAG,
    CAN_ERR_FLAG,
    CAN_RTR_FLAG,
)

GS_USB_ECHO_ID = 0
GS_USB_NONE_ECHO_ID = 0xFFFFFFFF

#from gs_usb.gs_usb import (
#    GS_USB_MODE_NORMAL ,
#    GS_USB_MODE_LISTEN_ONLY ,
#    GS_USB_MODE_LOOP_BACK ,
#    GS_USB_MODE_ONE_SHOT ,
#    GS_USB_MODE_NO_ECHO_BACK,
#)

GS_CAN_MODE_NORMAL = 0
GS_CAN_MODE_LISTEN_ONLY = (1 << 0)
GS_CAN_MODE_LOOP_BACK = (1 << 1)
#GS_CAN_MODE_TRIPLE_SAMPLE = (1 << 2)
GS_CAN_MODE_ONE_SHOT = (1 << 3)
GS_CAN_MODE_HW_TIMESTAMP = (1 << 4)

def main():
    devs = GsUsb.scan()
    if len(devs) == 0:
        print("Can not find gs_usb device")
        return
    
    dev = devs[0]
    print(dev)

    if not dev.set_bitrate(125000):
        print("Can not set bitrate for gs_usb")
        return
    
    dev.start(GS_CAN_MODE_NORMAL)
    #dev.start(GS_USB_MODE_NORMAL)

    data = b"\x12\x34\x56\x78\x9A\xBC\xDE\xF0"
    sff_frame = GsUsbFrame(can_id=0x7FF, data=data)
    frames = [
        sff_frame
    ]
    
    while True:
        iframe = GsUsbFrame()
        if dev.read(iframe, 1):
            if iframe.echo_id == GS_USB_NONE_ECHO_ID:
                print("RX  {}".format(iframe))

        if input() == 'b':

            if dev.send(frames[0]):
                print("TX  {}".format(frames[0]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        devs = GsUsb.scan()
        dev = devs[1]
        dev.stop()
        pass