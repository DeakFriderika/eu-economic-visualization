import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# EU-tagországok listája (27 ország)
eu_countries = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia",
    "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
    "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
    "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia",
    "Slovenia", "Spain", "Sweden"
]

# ---------------------------------------------
# 1️⃣ GDP per capita adatok beolvasása és tisztítása
# ---------------------------------------------
gdp = pd.read_csv("GDP.csv")

# Oszlopok átnevezése: geo = ország, TIME_PERIOD = év, OBS_VALUE = érték
gdp = gdp.rename(columns={
    "geo": "country",
    "TIME_PERIOD": "year",
    "OBS_VALUE": "gdp_per_capita"
})

# Csak EU-tagországokat és 2013–2023 közötti éveket megtartva
gdp = gdp[gdp["country"].isin(eu_countries)]
gdp = gdp[gdp["year"].between(2013, 2023)]

# ---------------------------------------------
# 2️⃣ Költségvetési hiány adatok beolvasása és tisztítása
# ---------------------------------------------
deficit = pd.read_csv("Koltsegvetesidef.csv")

deficit = deficit.rename(columns={
    "geo": "country",
    "TIME_PERIOD": "year",
    "OBS_VALUE": "budget_deficit"
})

deficit = deficit[deficit["country"].isin(eu_countries)]
deficit = deficit[deficit["year"].between(2013, 2023)]

# ---------------------------------------------
# 3️⃣ Államadósság adatok beolvasása és tisztítása
# ---------------------------------------------
debt = pd.read_csv("Allamadossag.csv")

debt = debt.rename(columns={
    "geo": "country",
    "TIME_PERIOD": "year",
    "OBS_VALUE": "debt"
})

debt = debt[debt["country"].isin(eu_countries)]
debt = debt[debt["year"].between(2013, 2023)]

# ---------------------------------------------
# 🔄 4️⃣ Adatok összefűzése ország + év alapján
# ---------------------------------------------
merged = gdp.merge(deficit, on=["country", "year"])
merged = merged.merge(debt, on=["country", "year"])

# ---------------------------------------------
# 💾 5️⃣ Mentés új CSV fájlba
# ---------------------------------------------
merged.to_csv("eu_economic_summary.csv", index=False)

# CSV fájl beolvasása
df = pd.read_csv("eu_economic_summary.csv")

# Adatok átalakítása heatmap formátumra
debt_pivot = df.pivot(index="country", columns="year", values="debt")

# Heatmap készítése
plt.figure(figsize=(15, 10))

# Heatmap rajzolása
sns.heatmap(
    debt_pivot,
    annot=True,  # Értékek megjelenítése
    fmt=".1f",   # Egy tizedesjegy
    cmap="RdYlGn_r",  # Piros-sárga-zöld színskála (fordítva)
    center=60,   # Középpont a 60%-nál (EU küszöb)
    cbar_kws={'label': 'Államadósság (% GDP)'}
)

# Címek és címkék
plt.title("Államadósság alakulása az EU-tagországokban (2013-2023)")
plt.xlabel("Év")
plt.ylabel("Ország")
plt.tight_layout()

# Mentés
plt.savefig("debt_heatmap.png", bbox_inches='tight', dpi=300)
plt.close()

print("✅ Az államadósság heatmap sikeresen elkészült!")
print("📁 Mentve: debt_heatmap.png")

# 2023-as adatok kinyerése
latest_data = df[df["year"] == 2023]

# Országok kiválasztása GDP alapján
highest_gdp_country = latest_data.loc[latest_data["gdp_per_capita"].idxmax(), "country"]
lowest_gdp_country = latest_data.loc[latest_data["gdp_per_capita"].idxmin(), "country"]

# Átlaghoz legközelebbi ország megtalálása
mean_gdp = latest_data["gdp_per_capita"].mean()
average_gdp_country = latest_data.loc[(latest_data["gdp_per_capita"] - mean_gdp).abs().idxmin(), "country"]

# Kiválasztott országok adatai
selected_countries = [highest_gdp_country, average_gdp_country, lowest_gdp_country]
selected_data = latest_data[latest_data["country"].isin(selected_countries)]

# Adatok normalizálása 0-1 skálára
metrics = ["gdp_per_capita", "debt", "budget_deficit"]
normalized_data = {}

for metric in metrics:
    min_val = latest_data[metric].min()
    max_val = latest_data[metric].max()
    normalized_data[metric] = (selected_data[metric] - min_val) / (max_val - min_val)

# Radar chart készítése
angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False)
angles = np.concatenate((angles, [angles[0]]))  # Kör bezárása

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

colors = ['#2ecc71', '#3498db', '#e74c3c']  # Zöld, kék, piros
labels = ['GDP per fő', 'Államadósság', 'Költségvetési hiány']

for idx, country in enumerate(selected_countries):
    values = [normalized_data[metric].iloc[idx] for metric in metrics]
    values = np.concatenate((values, [values[0]]))  # Kör bezárása
    
    ax.plot(angles, values, 'o-', linewidth=2, color=colors[idx], label=country)
    ax.fill(angles, values, alpha=0.25, color=colors[idx])

# Címkék és formázás
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
ax.set_ylim(0, 1)
plt.title("Gazdasági mutatók összehasonlítása (2023)", pad=20)
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

plt.tight_layout()
plt.savefig("economic_radar_chart.png", bbox_inches='tight', dpi=300)
plt.close()

print("✅ A radar chart sikeresen elkészült!")
print("📁 Mentve: economic_radar_chart.png")
print(f"\nÖsszehasonlított országok:")
print(f"🔼 Legmagasabb GDP: {highest_gdp_country}")
print(f"➡️ Átlagos GDP: {average_gdp_country}")
print(f"🔽 Legalacsonyabb GDP: {lowest_gdp_country}")
