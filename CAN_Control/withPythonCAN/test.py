import can


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


devs = GsUsb.scan()
dev = devs[0]
dev.stop()



def send_one():

    """Sends a single message."""


    # this uses the default configuration (for example from the config file)

    # see https://python-can.readthedocs.io/en/stable/configuration.html

    with can.Bus(interface='usb2can', bitrate=125000) as bus:

        # Using specific buses works similar:

        # bus = can.Bus(interface='socketcan', channel='vcan0', bitrate=250000)

        # bus = can.Bus(interface='pcan', channel='PCAN_USBBUS1', bitrate=250000)

        # bus = can.Bus(interface='ixxat', channel=0, bitrate=250000)

        # bus = can.Bus(interface='vector', app_name='CANalyzer', channel=0, bitrate=250000)

        # ...


        msg = can.Message(

            arbitration_id=0xC0FFEE, data=[0, 25, 0, 1, 3, 1, 4, 1], is_extended_id=True

        )


        try:

            bus.send(msg)

            print(f"Message sent on {bus.channel_info}")

        except can.CanError:

            print("Message NOT sent")



if __name__ == "__main__":

    send_one()