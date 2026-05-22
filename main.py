import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# šautriņu dēļa riņķu rādiusi
radiuses = [6.35, 16, 99, 107, 162, 170, 225.5]


# saraksts ar sektoru leņķiem radiānos
deg = 9
rad_list = []

while deg < 360:

    rad = np.deg2rad(deg)
    rad_list.append(rad)

    deg += 18


# funkcija šautriņu dēļa uzzīmēšanai (debugošanai)
def draw_board():
     
    plt.figure(figsize=(6, 6))
    ax = plt.gca()

    # uzzīmē koncentriskos riņķus
    for r in radiuses:
        circle = plt.Circle((0, 0), r, color="red", fill=False)
        ax.add_patch(circle)

    # uzzīmē sektoru līnijas
    for rad in rad_list:

        sin_val = np.sin(rad)
        cos_val = np.cos(rad)

        x0 = radiuses[1] * cos_val
        y0 = radiuses[1] * sin_val

        x = radiuses[-1] * cos_val
        y = radiuses[-1] * sin_val

        plt.plot([x0, x], [y0, y], color="red")

    # uzzīmē metienu punktus
    plt.scatter(x_points, y_points)

    plt.axis("equal")
    plt.show()


contestants = ["Jānis", "Ilze"]

# punktu secība pa sektoriem
aim_points = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17,
              3, 19, 7, 16, 8, 11, 14, 9, 12, 5]

# uzvaru skaitītāji
Janis_wins = 0
Ilzes_wins = 0
ties = 0

# katras spēles rezultātu saraksti
Janis_points = []
Ilzes_points = []


# cikls katrai spēlei
for num in range(10000):

    current_game_points = []

    # cikls katram dalībniekam
    for contestant in contestants:

        points = 0

        # mērķēšanas vieta katram spēlētājam
        if contestant == "Jānis":
            loc_x = 0
            loc_y = 0

        elif contestant == "Ilze":
            loc_x = 0
            loc_y = 103

        # ģenerē 3 nejaušus metienus
        x_points = np.random.normal(loc=loc_x, scale=70, size=3)
        y_points = np.random.normal(loc=loc_y, scale=70, size=3)

        # pārvērš Dekarta koordinātas polārajās koordinātās
        polar_len = (x_points**2 + y_points**2)**0.5
        polar_rad = np.arctan2(x_points, y_points)

        # pārveido negatīvās radiānu vērtības par pozitīvām
        polar_rad[polar_rad < 0] += 2 * np.pi

        polar_deg = np.rad2deg(polar_rad)

        # cikls katra metiena punktu noteikšanai
        for i in range(len(polar_len)):

            # pārbauda vai metiens ir dēļa robežās
            if polar_len[i] <= 170:

                # pārbauda centrālos mērķus
                if polar_len[i] <= radiuses[1]:

                    if polar_len[i] <= radiuses[0]:
                        points += 50

                    else:
                        points += 25

                    continue

                # sektora indeksa noteikšana
                idx = np.searchsorted(rad_list, polar_rad[i])

                # pilna apļa gadījums
                if idx == len(aim_points):
                    idx = 0

                # triple sektors
                if 98 <= polar_len[i] <= 107:
                    points += 3 * aim_points[idx]

                # double sektors
                elif 162 <= polar_len[i] <= 170:
                    points += 2 * aim_points[idx]

                # parastais sektors
                else:
                    points += aim_points[idx]

        current_game_points.append(points)

        # saglabā spēles rezultātus
        if contestant == "Jānis":
            Janis_points.append(points)

        elif contestant == "Ilze":
            Ilzes_points.append(points)

    # nosaka uzvarētāju konkrētajā spēlē
    if current_game_points[0] > current_game_points[1]:
        Janis_wins += 1

    elif current_game_points[0] < current_game_points[1]:
        Ilzes_wins += 1

    else:
        ties += 1


# izvada kopējo statistiku
print("Jāņa uzvaras:", Janis_wins)
print("Ilzes uzvaras:", Ilzes_wins)
print("Neizšķirts:", ties)


# histogrammu dati
points = [Janis_points, Ilzes_points]

plt.figure(figsize=(10, 6))

# histogrammu krāsas
hist_colors = ["royalblue", "orange"]

# vidējo vērtību līniju krāsas
mean_colors = ["red", "darkred"]

# mediānu līniju krāsas
median_colors = ["green", "darkgreen"]

labels = ["Jāņa punkti", "Ilzes punkti"]


# cikls histogrammu zīmēšanai
for person_points, hist_color, mean_color, median_color, label in zip(
    points,
    hist_colors,
    mean_colors,
    median_colors,
    labels
):

    # histogramma un KDE līkne
    sns.histplot(
        person_points,
        bins=20,
        kde=True,
        color=hist_color,
        edgecolor="black",
        alpha=0.5,
        label=label,
    )

    # statistikas aprēķini
    mean_val = np.mean(person_points)
    median_val = np.median(person_points)

    # vidējās vērtības līnija
    plt.axvline(
        mean_val,
        color=mean_color,
        linestyle="--",
        linewidth=2,
        label=f"Vidējais ({label}): {mean_val:.2f}",
    )

    # mediānas līnija
    plt.axvline(
        median_val,
        color=median_color,
        linestyle="-.",
        linewidth=2,
        label=f"Mediāna ({label}): {median_val:.2f}",
    )


# grafika noformējums
plt.xlabel("Punkti", fontsize=13)
plt.ylabel("Biežums", fontsize=13)

plt.legend()
plt.tight_layout()

plt.savefig("uzd_7.png", dpi=300)
plt.show()
