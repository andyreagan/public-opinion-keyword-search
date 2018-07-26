# coding: utf-8
import datetime
import os
start = datetime.datetime(2008,9,13)
dt = datetime.timedelta(minutes=15)
# curr = datetime.datetime.now()
# curr=curr-datetime.timedelta(days=7)
# curr
# curr.strftime("keywords/%Y-%m-%d/%Y-%m-%d-%H-%M.pkl")
# f = curr.strftime("keywords/%Y-%m-%d/%Y-%m-%d-%H-%M.pkl")
# os.path.isfile(f)
# curr = start.copy()
curr = start
missing = []
while curr < datetime.datetime.now():
    f = curr.strftime("keywords/%Y-%m-%d/%Y-%m-%d-%H-%M.pkl")
    if not os.path.isfile(f):
        # print("missing", f)
        missing.append(f)
    curr+=dt
with open("missing.txt", "w") as f:
    f.write("\n".join(missing))

