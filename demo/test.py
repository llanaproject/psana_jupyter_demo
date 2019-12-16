import os
from psana import DataSource
from dask.distributed import Client
from dask.distributed import Queue

client = Client(scheduler_file="scheduler.json")

queue = Queue("psana")


def filter_fn(evt):
    return True


xtc_dir = os.path.join(os.environ.get("TEST_XTC_DIR", os.getcwd()), ".tmp")

ds = DataSource(exp="xpptut13", run=1, dir=xtc_dir, filter=filter_fn)

for run in ds.runs():
    det = run.Detector("xppcspad")
    edet = run.Detector("HX2:DVD:GCC:01:PMON")
    for evt in run.events():
        print("In run.events loop")
        # 4 segments, two per file

        raw = det.raw.calib(evt)
        queue.put(raw.tolist())
