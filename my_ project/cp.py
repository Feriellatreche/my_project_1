from mpi4py import MPI
import numpy as np
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# حجم المصفوفة
N = 80

# عدد مرات التكرار
RUNS = 2   # يمكنك تغييره

def multiply_chunk(A, B, start_row, end_row):
    C_part = np.zeros((end_row - start_row, B.shape[1]))
    for i in range(start_row, end_row):
        for j in range(B.shape[1]):
            tmp = 0
            for k in range(B.shape[0]):
                tmp += A[i][k] * B[k][j]
            C_part[i - start_row][j] = tmp
    return C_part


# ================================
#           ROOT PROCESS
# ================================
if rank == 0:

    print(f"\n=== Running MPI with {size} processes ===")

    A = np.random.rand(N, N)
    B = np.random.rand(N, N)

    rows_per_proc = N // size

    times = []

    for r in range(RUNS):

        start = time.time()

        # تقسيم الصفوف بين العمليات
        offsets = []
        for i in range(size):
            s = i * rows_per_proc
            e = (i + 1) * rows_per_proc if i != size - 1 else N
            offsets.append((s, e))

        # إرسال الأجزاء
        for dest in range(1, size):
            s, e = offsets[dest]
            comm.send((A[s:e], B), dest=dest)

        # حساب جزء العملية 0
        s0, e0 = offsets[0]
        C0 = multiply_chunk(A, B, s0, e0)

        # استقبال باقي الأجزاء
        C_parts = [C0]
        for source in range(1, size):
            C_parts.append(comm.recv(source=source))

        # تجميع المصفوفة
        C = np.vstack(C_parts)

        end = time.time()
        times.append(end - start)

    print("\n=== FINAL RESULTS ===")
    print("Times:", times)
    print("Average:", np.mean(times))

# ================================
#         OTHER PROCESSES
# ================================
else:
    for r in range(RUNS):
        A_part, B = comm.recv(source=0)

        # حساب الجزء
        C_part = np.zeros((A_part.shape[0], B.shape[1]))
        for i in range(A_part.shape[0]):
            for j in range(B.shape[1]):
                tmp = 0
                for k in range(B.shape[0]):
                    tmp += A_part[i][k] * B[k][j]
                C_part[i][j] = tmp

        comm.send(C_part, dest=0)