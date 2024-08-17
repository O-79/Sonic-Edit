import numpy as np
from scipy.signal import butter, lfilter

class Edit:
    def EQUALIZER(DAT, SPL_RTE, DB_ADD, HZ_LOW, HZ_UPP):
        print(f"ADD: {DB_ADD} / LOW: {HZ_LOW} / UPP: {HZ_UPP}")
        FCT_ADD = 10 ** (DB_ADD / 20.0)
        NYQ = 0.5 * SPL_RTE
        LOW = HZ_LOW / NYQ
        UPP = HZ_UPP / NYQ
        b, a = butter(1, [LOW, UPP], btype='band')
        y = lfilter(b, a, DAT)
        DAT_ADD = y * FCT_ADD
        return DAT + DAT_ADD