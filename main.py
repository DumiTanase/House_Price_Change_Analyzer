import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk


pd.options.mode.copy_on_write = True
df = pd.read_csv('houseprices.csv')
df['DurationFrom'] = pd.to_datetime(df['DurationFrom'])
df.loc[:, 'YearMonth'] = df['DurationFrom'].dt.strftime('%Y-%m')
place_name = list(set(df['GeoName'].to_list()))


def visualize():
    user = variable.get()
    region = df[(df['GeoName'] == user)]
    region = region.sort_values('YearMonth')

    region['DetachedPriceIncrease'] = region['AveragePriceDetached'].pct_change() * 100
    region['SemiDetachedPriceIncrease'] = region['AveragePriceSemiDetached'].pct_change() * 100
    region['TerracedPriceIncrease'] = region['AveragePriceTerraced'].pct_change() * 100
    region['FlatOrMaisonettePriceIncrease'] = region['AveragePriceFlatOrMaisonette'].pct_change() * 100

    x = np.arange(len(region['YearMonth']))
    bar_width = 0.2

    plt.bar(x - bar_width, region['DetachedPriceIncrease'], width=bar_width, color='#04e762',
            edgecolor='black', label='Detached')
    plt.bar(x, region['SemiDetachedPriceIncrease'], width=bar_width, color='#f5b700',
            edgecolor='black', label='Semi-Detached')
    plt.bar(x + bar_width, region['TerracedPriceIncrease'], width=bar_width, color='#dc0073',
            edgecolor='black', label='Terraced')
    plt.bar(x + 2 * bar_width, region['FlatOrMaisonettePriceIncrease'], width=bar_width, color='#008bf8',
            edgecolor='black', label='Flat/Maisonette')

    plt.xticks(x, region['YearMonth'], rotation=45)
    plt.xlabel('Month')
    plt.ylabel('Price Change %')
    plt.title(f'Price Change Over Months in {user}')
    plt.legend()
    plt.show()


window = tk.Tk()
window.title("Choose a Region")
window.minsize(width=140, height=130)

label = tk.Label(window, text="Choose a region", font='Forte', pady=10, padx=10)
label.config(bg='white')
label.pack()

variable = tk.StringVar(window)
variable.set(place_name[0])

dropdown = tk.OptionMenu(window, variable, *place_name)
dropdown.config(font='Italic', activebackground='lightblue', bg='white', pady=10)
dropdown.pack()

button = tk.Button(window, text="Visualize", command=visualize)
button.config(bg='white', activebackground='silver', pady=10)
button.pack()

window.mainloop()
