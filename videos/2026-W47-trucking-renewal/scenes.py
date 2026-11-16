"""Scene boundaries shared by build.py and mix.py, derived from the voiceover timing."""
import json
L = json.load(open("timing.json"))["lines"]
S2, S3, S4, S5 = 2.45, 4.35, 6.02, 9.26
S5B = round(L[5]["speech"][0] - 0.06, 3)
S6 = round(L[6]["speech"][0] - 0.16, 3)
S7 = round(L[7]["speech"][0] - 0.13, 3)
DUR = round(L[7]["speech"][1] + 2.36, 1)
