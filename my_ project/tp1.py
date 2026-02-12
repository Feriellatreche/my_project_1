
import time
import numpy as np
import matplotlib.pyplot as plt

# خوارزميات البحث

def recherche_lineaire(tab, x):
    comparisons = 0  # عداد للمقارنات
    for i, val in enumerate(tab):  # المرور على كل عناصر المصفوفة
        comparisons += 1
        if val == x:  # إذا وجدنا العنصر المطلوب
            return i, comparisons
    return -1, comparisons  # إذا لم يتم العثور عليه

def recherche_lineaire_amelioree(tab, x):
    comparisons = 0
    for i, val in enumerate(tab):
        comparisons += 1
        if val == x:  # إذا وجد العنصر
            return i, comparisons
        elif val > x:  # إذا تجاوزنا العنصر المطلوب (المصفوفة مرتبة)
            break  # نوقف البحث
    return -1, comparisons

def recherche_binaire_iterative(tab, x):
    gauche, droite = 0, len(tab) - 1  # حدود البداية والنهاية
    comparisons = 0
    while gauche <= droite:  # طالما ما زال هناك عناصر
        milieu = (gauche + droite) // 2  # حساب موقع الوسط
        comparisons += 1
        if tab[milieu] == x:  # إذا وجد العنصر
            return milieu, comparisons
        elif tab[milieu] < x:  # إذا كان العنصر في النصف الأيمن
            gauche = milieu + 1
        else:  # إذا كان العنصر في النصف الأيسر
            droite = milieu - 1
    return -1, comparisons  # إذا لم يتم العثور عليه

def recherche_binaire_recursive(tab, x, gauche, droite, comparisons=0):
    if gauche > droite:  # شرط التوقف (لا يوجد نطاق صالح)
        return -1, comparisons
    milieu = (gauche + droite) // 2  # حساب الوسط
    comparisons += 1
    if tab[milieu] == x:  # إذا وجد العنصر
        return milieu, comparisons
    elif tab[milieu] < x:  # إذا كان العنصر في النصف الأيمن
        return recherche_binaire_recursive(tab, x, milieu + 1, droite, comparisons)
    else:  # إذا كان العنصر في النصف الأيسر
        return recherche_binaire_recursive(tab, x, gauche, milieu - 1, comparisons)


# اختبار الخوارزميات
def tester_algorithmes(taille, essais=100):
    # تخزين نتائج كل خوارزمية
    resultats = {"linéaire": [], "linéaire améliorée": [], "binaire itérative": [], "binaire récursive": []}

    for _ in range(essais):  # تكرار التجربة لعدة مرات
        tab = np.sort(np.random.randint(0, 10**6, size=taille))  # إنشاء مصفوفة مرتبة من أعداد عشوائية
        x = np.random.choice(tab)  # اختيار عنصر عشوائي للبحث عنه

        # --- البحث الخطي ---
        debut = time.time()
        _, comp = recherche_lineaire(tab, x)
        fin = time.time()
        resultats["linéaire"].append((fin - debut, comp))

        # --- البحث الخطي المحسن ---
        debut = time.time()
        _, comp = recherche_lineaire_amelioree(tab, x)
        fin = time.time()
        resultats["linéaire améliorée"].append((fin - debut, comp))

        # --- البحث الثنائي التكراري ---
        debut = time.time()
        _, comp = recherche_binaire_iterative(tab, x)
        fin = time.time()
        resultats["binaire itérative"].append((fin - debut, comp))

        # --- البحث الثنائي الاستدعائي ---
        debut = time.time()
        _, comp = recherche_binaire_recursive(tab, x, 0, len(tab) - 1)
        fin = time.time()
        resultats["binaire récursive"].append((fin - debut, comp))

    # حساب المتوسط والانحراف المعياري
    stats = {}
    for nom, valeurs in resultats.items():
        temps = [v[0] for v in valeurs]  # قائمة الأوقات
        comps = [v[1] for v in valeurs]  # قائمة المقارنات
        stats[nom] = {
            "temps_moyen": np.mean(temps),
            "ecart_temps": np.std(temps),
            "comparaisons_moy": np.mean(comps),
            "ecart_comp": np.std(comps)
        }
    return stats



# تنفيذ التجارب
tailles = [10**3, 10**4, 10**5, 10**6]  # أحجام المصفوفات
resultats_global = {nom: {"temps": [], "comparaisons": []} for nom in
                    ["linéaire", "linéaire améliorée", "binaire itérative", "binaire récursive"]}

# تنفيذ كل تجربة
for t in tailles:
    print(f"\n=== Taille du tableau : {t} ===")
    stats = tester_algorithmes(t)
    for nom, s in stats.items():
        print(f"{nom:22s} | Temps: {s['temps_moyen']:.8f}s ± {s['ecart_temps']:.8f} | "
              f"Comparaisons: {s['comparaisons_moy']:.1f} ± {s['ecart_comp']:.1f}")
        resultats_global[nom]["temps"].append(s["temps_moyen"])
        resultats_global[nom]["comparaisons"].append(s["comparaisons_moy"])

# الرسم البياني لعدد المقارنات
plt.figure(figsize=(10, 5))
for nom, data in resultats_global.items():
    plt.plot(tailles, data["comparaisons"], marker='o', label=nom)
plt.title("Comparaison du nombre de comparaisons entre les algorithmes de recherche")  
plt.xlabel("Taille du tableau (échelle logarithmique)")  
plt.ylabel("Nombre moyen de comparaisons")
plt.xscale("log")
plt.legend()
plt.grid(True)
plt.show()

# ===============================
# الرسم البياني لزمن التنفيذ
# ===============================
plt.figure(figsize=(10, 5))
for nom, data in resultats_global.items():
    plt.plot(tailles, data["temps"], marker='o', label=nom)
plt.title("Comparaison du temps d’exécution entre les algorithmes de recherche")  
plt.xlabel("Taille du tableau (échelle logarithmique)")  
plt.ylabel("Temps moyen (secondes)")  
plt.xscale("log")
plt.legend()
plt.grid(True)
plt.show()