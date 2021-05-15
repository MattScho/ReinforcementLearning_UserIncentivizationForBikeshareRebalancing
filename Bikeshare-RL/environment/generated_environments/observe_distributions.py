import matplotlib.pyplot as plt
import pickle as pkl

'''
Script to allow for observing distributions inside of the environment

:author: Matthew Schofield
:version: 4.10.2021
'''
arrivals = pkl.load(open("DC_base.pkl", "rb")).get_arrivals()
for h in range(8,10):
    matrix = arrivals[h].reshape((10,10))
    print(matrix)
    plt.title("Arrival Distribution for Hour " + str(h))
    plt.imshow(matrix, cmap='Greens')
    plt.show()