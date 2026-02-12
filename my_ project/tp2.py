import random
import time
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
#  خوارزميات البحث
#  -----------------------------

def recherche_seq_simple(tab, val):
    comp = 0
    for x in tab:
        comp += 1
        if x == val:
            return True, comp
    return False, comp

def recherche_seq_optimisee(tab, val):
    comp = 0
    for x in tab:
        comp += 1
        if x == val:
            return True, comp
        elif x > val:   # بما أن الجدول مرتب
            return False, comp
    return False, comp

def recherche_binaire_iterative(tab, val):
    comp = 0
    g, d = 0, len(tab) - 1
    while g <= d:
        m = (g + d) // 2
        comp += 1
        if tab[m] == val:
            return True, comp
        elif tab[m] < val:
            g = m + 1
        else:
            d = m - 1
    return False, comp

def recherche_binaire_recursive(tab, val, g, d, comp=0):
    if g > d:
        return False, comp
    m = (g + d) // 2
    comp += 1
    if tab[m] == val:
        return True, comp
    elif tab[m] < val:
        return recherche_binaire_recursive(tab, val, m + 1, d, comp)
    else:
        return recherche_binaire_recursive(tab, val, g, m - 1, comp)

# -----------------------------
# 2️ تجربة الخوارزميات
# -----------------------------

def tester_algorithmes(taille, nb_tests=30):
    algos = {
        "Séquentielle simple": recherche_seq_simple,
        "Séquentielle optimisée": recherche_seq_optimisee,
        "Binaire itérative": recherche_binaire_iterative,
        "Binaire récursive": lambda tab, val: recherche_binaire_recursive(tab, val, 0, len(tab)-1)
    }

    stats = {}

    for nom, algo in algos.items():
        temps_list = []
        comp_list = []

        for _ in range(nb_tests):
            tab = sorted(random.sample(range(0, taille*10), taille))  # توليد جدول مرتب
            val = random.randint(0, taille*10)

            t1 = time.time()
            _, comp = algo(tab, val)
            t2 = time.time()

            temps_list.append(t2 - t1)
            comp_list.append(comp)

        stats[nom] = {
            "temps_moyen": np.mean(temps_list),
            "ecart_temps": np.std(temps_list),
            "comp_moyen": np.mean(comp_list),
            "ecart_comp": np.std(comp_list)
        }

    return stats

# -----------------------------
# 3️ تنفيذ و عرض النتائج
# -----------------------------

tailles = [1000, 10000, 100000, 10000000]

for t in tailles:
    print(f"\n===== Taille du tableau : {t} =====")
    stats = tester_algorithmes(t)
    for nom, s in stats.items():
        print(f"{nom:25s} | Temps: {s['temps_moyen']:.8f}s ± {s['ecart_temps']:.8f} | "
              f"Comparaisons: {s['comp_moyen']:.2f} ± {s['ecart_comp']:.2f}")

# -----------------------------
# 4️ رسم النتائج بالـ Matplotlib
# -----------------------------

def tracer_graphique(stats_all, tailles):
    noms_algos = list(stats_all[0].keys())
    couleurs = ['r', 'g', 'b', 'm']

    # رسم الزمن
    plt.figure(figsize=(10,5))
    for i, nom in enumerate(noms_algos):
        plt.plot(tailles, [s[nom]['temps_moyen'] for s in stats_all], 
                 label=nom, marker='o', color=couleurs[i])
    plt.xlabel("Taille du tableau")
    plt.ylabel("Temps moyen (s)")
    plt.title("Comparaison des temps d’exécution")
    plt.legend()
    plt.grid()
    plt.show()

    # رسم المقارنات
    plt.figure(figsize=(10,5))
    for i, nom in enumerate(noms_algos):
        plt.plot(tailles, [s[nom]['comp_moyen'] for s in stats_all], 
                 label=nom, marker='o', color=couleurs[i])
    plt.xlabel("Taille du tableau")
    plt.ylabel("Nombre moyen de comparaisons")
    plt.title("Comparaison du nombre de comparaisons")
    plt.legend()
    plt.grid()
    plt.show()

# حفظ النتائج لرسمها
stats_all = [tester_algorithmes(t) for t in tailles]
tracer_graphique(stats_all, tailles)