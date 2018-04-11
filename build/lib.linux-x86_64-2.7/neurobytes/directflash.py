import usb.core
import usb.util
import array

dev = usb.core.find(idVendor=0x1d50, idProduct=0x6018)
dev.reset()
# dev.write(0x83, 'test', 1000)

if dev is None:
    raise ValueError('Device not found')

for i in xrange(10):
    if dev.is_kernel_driver_active(i):
        reattach= True
        dev.detach_kernel_driver(i)
dev.set_configuration()

cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = intf[1] # interface 0 is gdb??

assert ep is not None

# write the data

dev.ctrl_transfer(0x21, 0x22, 0x01 | 0x02, 0, None)
dev.ctrl_transfer(0x21, 0x20, 0, 0,
                  array.array('B', [0x80, 0x25, 0x00, 0x00, 0x00, 0x00, 0x08]))

while(True):
    # dev.write(0x02, 't', interface = 1)
    ep.write('test', 1000)
    try:
        print 'Received: "%s"' % dev.read(0x83, 64, interface = 1).tostring()
    except:
        print 'read failed'
# ep.write('test', 1000)
usb.util.dispose_resources(dev)