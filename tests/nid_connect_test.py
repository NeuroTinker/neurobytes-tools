from neurobytes import nid

dev = nid.nidHandler()
dev.start()
#dev.recv_quit([])
dev.wait_for_quit()
