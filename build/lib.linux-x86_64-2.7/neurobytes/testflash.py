
import usb.core
import usb.util
import usb.control

import array

# Look for a specific device and open it
#
dev = usb.core.find(idVendor=0x1d50, idProduct=0x6018) # Arduino Leonardo
if dev is None:
    raise ValueError('Device not found')

# Detach interfaces if Linux already attached a driver on it.
#
for itf_num in xrange(1):
    itf = usb.util.find_descriptor(dev.get_active_configuration(),
                                   bInterfaceNumber=1)
    if dev.is_kernel_driver_active(itf):
        dev.detach_kernel_driver(itf)
    usb.util.claim_interface(dev, itf)


# set control line state 0x2221
# set line encoding 0x2021 (9600, 8N1)
#
dev.ctrl_transfer(0x21, 0x22, 0x01 | 0x02, 0, None)
dev.ctrl_transfer(0x21, 0x20, 0, 0,
                  array.array('B', [0x80, 0x25, 0x00, 0x00, 0x00, 0x00, 0x08]))

while(True):
    dev.write(0x02, 't', interface = 1)
    try:
        print 'Received: "%s"' % dev.read(0x83, 64, interface = 1).tostring()
    except:
        print 'read failed'
pass