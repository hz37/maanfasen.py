# Grafiek van de maanfasen voor de komende dertig dagen.
# Hens Zimmerman <henszimmerman@gmail.com>, 5 februari 2021.
# Anaconda Python 3.8 met matplotlib en skyfield modules.

from datetime import timedelta

from skyfield import api
from skyfield import almanac

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches

efemeriden = api.load('de421.bsp')

# Hoeveel dagen willen we vooruit kijken?

dagen = 30

# Wat is het vandaag?

timescale = api.load.timescale()

nu = timescale.now()

# Voor het optellen van dagen gebruiken we een python object.

python_datum = nu.utc_datetime()

# Maanfasen voor de komende dagen.

data = []
verlichtingen = []

for x in range(dagen):
    skyfield_datum = timescale.from_datetime(python_datum)
    data.append(python_datum)
    maanfase = almanac.moon_phase(efemeriden, skyfield_datum)
    verlicht = (180 - abs(maanfase.degrees - 180)) / 180 * 100
    verlichtingen.append(verlicht)
    python_datum += timedelta(days=1)


# Print naar grafiek.

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('Verlichting van de maan vanaf ' + nu.utc_strftime(format='%d %B %Y'))
ax.set_facecolor('#eafff5')

vol = mpatches.Patch(color='yellow', label='100%: volle maan')
plt.legend(handles=[vol], loc='upper left')

ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %B'))

plt.plot(data, verlichtingen)
fig.autofmt_xdate()
ax.grid(True)
plt.show()

