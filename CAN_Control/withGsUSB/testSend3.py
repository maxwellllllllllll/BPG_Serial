import time

from gs_usb.gs_usb import GsUsb
from gs_usb.gs_usb_frame import GsUsbFrame
from gs_usb.constants import (
    CAN_EFF_FLAG,
    CAN_ERR_FLAG,
    CAN_RTR_FLAG,
)


# gs_usb general also can import from gs_usb_structures.py
GS_USB_ECHO_ID = 0
GS_USB_NONE_ECHO_ID = 0xFFFFFFFF


#innomaker usb2can device do not support the NO_ECHO_BACK mode
#below macro is for gs_usb 0.2.9
#from gs_usb.gs_usb import (
#    GS_USB_MODE_NORMAL ,
#    GS_USB_MODE_LISTEN_ONLY ,
#    GS_USB_MODE_LOOP_BACK ,
#    GS_USB_MODE_ONE_SHOT ,
#    GS_USB_MODE_NO_ECHO_BACK,
#)

#below macro is for gs_usb 0.3.0 and above

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

    #set can device handle from 0 to 1,2,3...  choosing the right device serial number accroding to the print
    #I found defualt usb2can device is devs[0] with gs_usb 0.2.9 ,and devs[1] with gs_usb 0.3.0
    dev = devs[0]
    print(dev)
    # Close before Start device in case the device was not properly stop last time
    # If do not stop the device, bitrate setting will be fail.
    #dev.stop()

    # Configuration Modify the Baudrate you want here
    if not dev.set_bitrate(125000):
        print("Can not set bitrate for gs_usb")
        return

    # Start device, If you have only one device for test, pls use the loop-back mode, otherwise you will get a lot of error frame
    # If you have already connect to a aviailable CAN-BUS, you could set as NORMAL mode
    #dev.start(GS_CAN_MODE_LOOP_BACK)
    dev.start(GS_CAN_MODE_NORMAL)
    # Prepare frames
    # list all kinds of frame for test. Select you want.

    # data = b"\x12\x34\x56\x78\x9A\xBC\xDE\xF0"
    data = b"\x00\x00\x00\x00\x00\x00\x00\x00"
    sff_frame = GsUsbFrame(can_id= 0x108040FE, data=data)
    sff_none_data_frame = GsUsbFrame(can_id=0x108040FE)
    err_frame = GsUsbFrame(can_id=0x108040FE | CAN_ERR_FLAG, data=data)
    eff_frame = GsUsbFrame(can_id=0x12345678 | CAN_EFF_FLAG, data=data)
    eff_none_data_frame = GsUsbFrame(can_id=0x12345678 | CAN_EFF_FLAG)
    rtr_frame = GsUsbFrame(can_id=0x108040FE | CAN_RTR_FLAG)
    rtr_with_eid_frame = GsUsbFrame(can_id=0x12345678 | CAN_RTR_FLAG | CAN_EFF_FLAG)
    rtr_with_data_frame = GsUsbFrame(can_id=0x108040FE | CAN_RTR_FLAG, data=data)
    frames = [
        sff_frame,
        sff_none_data_frame,
        err_frame,
        eff_frame,
        eff_none_data_frame,
        rtr_frame,
        rtr_with_eid_frame,
        rtr_with_data_frame,
    ]

    # Read all the time and send message in each second
    while True:
        #dev.send(frames[0])
        iframe = GsUsbFrame()
        if dev.read(iframe, 1):
            # if you don't want to receive the error frame. filter out it.
            # otherwise you will receive a lot of error frame when your device do not connet to CAN-BUS
            #if iframe.can_id & CAN_ERR_FLAG != CAN_ERR_FLAG:

            # filter out the echo frame. Otherwise It will read back the frame has been sent successfully
            if iframe.echo_id == GS_USB_NONE_ECHO_ID:
                print("RX  {}".format(iframe))

                if dev.send(frames[0]):
                        print("TX  {}".format(frames[0]))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # When press keyboard to kill the codes. The usb2can will not auto-stop.It may risk error when you open it next time.
        #So added below code to stop it.
        devs = GsUsb.scan()
        dev = devs[0]
        dev.stop()
        pass