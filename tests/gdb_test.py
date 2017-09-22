
gdb.execute("tar extended-remote /dev/ttyACM0")
gdb.execute("mon tpwr enable")
gdb.execute("mon swdp_scan")
gdb.execute("attach 1")
gdb.execute("run")
    
gdb.execute("quit")