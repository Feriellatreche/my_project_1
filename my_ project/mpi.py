from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rang = comm.Get_rank()
taille = comm.Get_size()

N = 20
partie_taille = N // 4  
if rang == 0:
    # توليد جدول عشوائي من 20 عددًا بين 1 و 100
    tableau = np.random.randint(1, 101, size=N)
    print("Tableau aléatoire généré :")
    print(tableau)

    # تقسيم الجدول إلى 4 أجزاء متساوية
    parties = [tableau[i:i + partie_taille] for i in range(0, N, partie_taille)]

    # إرسال الأجزاء إلى المعالجات الأخرى
    for i in range(1, taille):
        comm.Send([parties[i], MPI.INT], dest=i, tag=77)

    # الجزء الخاص بالمعالج 0
    partie_locale = parties[0]
else:
    # كل معالج يستقبل جزءه
    partie_locale = np.empty(partie_taille, dtype='i')
    comm.Recv([partie_locale, MPI.INT], source=0, tag=77)

# كل معالج يحسب القيمة القصوى في الجزء الخاص به
max_local = np.max(partie_locale)
print(f"Processeur {rang} : partie = {partie_locale} -> maximum local = {max_local}")

# إرسال القيم القصوى إلى المعالج 0
if rang == 0:
    maxima = [max_local]
    for i in range(1, taille):
        max_recv = np.empty(1, dtype='i')
        comm.Recv([max_recv, MPI.INT], source=i, tag=99)
        maxima.append(max_recv[0])
    print("\nValeurs maximales reçues de chaque processeur :", maxima)
    print(f" La plus grande valeur du tableau est : {np.max(maxima)}")
else:
    comm.Send([np.array([max_local], dtype='i'), MPI.INT], dest=0, tag=99)