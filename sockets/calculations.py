import numpy as np


class calculations:

    # recive msg

    # do calculation
    def rcvRequest(calc, listOfNum):
        if (calc == "Summe"):
            return np.sum(listOfNum)
        elif (calc == "Produkt"):
            return np.prod(listOfNum)
        elif (calc == "Minimum"):
            return np.min(listOfNum)
        elif (calc == "Maximum"):
            return np.max(listOfNum)