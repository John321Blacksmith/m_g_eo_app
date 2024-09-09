import math
 
# in order to calculate
# distance between two cities,
# I used the Euclidean distance formula
distance = lambda p, s_p: math.sqrt(
    (p._values_impl()[0].latitude - s_p._values_impl()[0].latitude)**2 + \
    (p._values_impl()[0].longitude - s_p._values_impl()[0].longitude)**2
    ) if p and s_p else 0


def sort_dists(dists: list[tuple]):
        """
        Quick sorting of the distances.
        """
        if len(dists) < 2:
            return dists
        else:
            pivot = dists[0]
            smaller_dists = [dists[i] for i in range(len(dists)) if dists[i][1] < pivot[1]]
            greater_dists = [dists[i] for i in range(len(dists)) if dists[i][1] > pivot[1]]

            return sort_dists(smaller_dists) + [pivot] + sort_dists(greater_dists)