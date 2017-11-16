from neurobytes import nid

dev = nid.nidHandler()
dev.start()
dev.recv_quit([])
dev._quit_ev.wait()