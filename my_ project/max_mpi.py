from mpi4py import MPI
import random
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size != 4:
    if rank == 0:
        print("Program must be run with 4 processors!")
    exit()

table_length = 20
chunk_size = 5

if rank == 0:
    data = [random.randint(1, 100) for _ in range(table_length)]
    print(f"Full table: {data}")
    
    chunks = [data[i*chunk_size:(i+1)*chunk_size] for i in range(4)]
else:
    chunks = None

local_data = comm.scatter(chunks, root=0)
local_max = max(local_data)

print(f"Processor {rank}: {local_data} -> Local max: {local_max}")

all_max = comm.gather(local_max, root=0)

if rank == 0:
    global_max = max(all_max)
    print(f"Received max values: {all_max}")
    print(f"Global maximum: {global_max}")