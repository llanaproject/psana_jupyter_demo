from psana import DataSource
import numpy as np
import sys
from dask.distributed import Client, Queue

# The code below fail with MPI rank errors. 
# import os
# os.environ['PS_SRV_NODES'] = "2"

# Connect to the Dask scheduler
client = Client(scheduler_file="scheduler.json")

# Create a Queue object
queue = Queue("psana")

# called back on each SRV node, for every smd.event() call below
def test_callback(data_dict):
    print(data_dict)

ds = DataSource(exp='xpptut13', run=1, dir='.tmp')

# batch_size here specifies how often the dictionary of information
# is sent to the SRV nodes
smd = ds.smalldata(filename='my.h5', batch_size=5, callbacks=[test_callback])
run = next(ds.runs())

# necessary (instead of "None") since some ranks may not receive events
# and the smd.sum() below could fail

arrsum = np.zeros((2), dtype=np.int)

for i,evt in enumerate(run.events()):
    myones = np.ones_like(arrsum)
    smd.event(evt, myfloat=2.0, arrint=myones)
    arrsum += myones
    queue.put(arrsum.tolist())


# This fails as reported in https://github.com/slac-lcls/lcls2/issues/11

# if smd.summary:
#     smd.sum(arrsum)
#     smd.save_summary({'summary_array' : arrsum}, summary_int=1)
# smd.done()

sys.exit()
