from neurobytes import nid
import csv
import time

nid_handle = nid.nidHandler()

nid_handle.graph_controller = nid.potentialGraph()
nid_handle.graph_controller.add_channel(1)
nid_handle._data_ch = 1
nid_handle.data_val = 0

nid_handle.nid_thread.start()
nid_handle.serial_thread.start()

with open('data.csv', 'wb') as f:
    wr = csv.writer(f)
    while True:
        if nid_handle._data_ev.is_set():
            nid_handle.graph_controller.update(nid_handle._data_val, 1)
            wr.writerow([time.time(), nid_handle._data_val])
            nid_handle._data_ev.clear()
            time.sleep(0.01)
        