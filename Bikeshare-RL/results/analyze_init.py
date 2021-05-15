'''
Analyze an initialization file
'''

import pickle as pkl
import matplotlib.pyplot as plt
import numpy as np

# Read in file
bss_init = pkl.load(open("../environment/generated_environments/DC_base.pkl", 'rb'))

plt.imshow(bss_init.get_init_supply().reshape((10,10)), cmap="Greens")
plt.show()

for h in range(24):
    regions = np.zeros((100))
    a_distrib = bss_init.get_arrivals()[h]
    users = int(5000 * bss_init.get_user_per_hour()[h])
    pick_from = np.arange(100)
    for _ in range(users):
        regions[np.random.choice(pick_from, p=a_distrib)] += 1
    print(regions)
    regions = np.divide(regions, np.sum(regions))
    regions = regions.reshape((10,10))
    plt.title(h)
    plt.imshow(regions, cmap="Greens")
    plt.show()
