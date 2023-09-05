from Gen_Instances import Gen_Bench_Instances
from SolMethod import solve_GTA
from SolMethod import solve_CP
from SolMethod import solve_LS
from SolMethod import solve_TS


structure_instances = [(15,15), (20,15), (20,20), (30,15), (30,20), (50,15), (50,20), (100,20)] #anhand Taillard
benchmark_instances = Gen_Bench_Instances(structure_instances, nmbr_instances_each_block = 1)

#Parametereinstellungen der einzelnen Lösungsverfahren definieren:
'''
Doku:
Verschiedene Parameter können für die einzelnen Methoden eingestellt (übergeben) werden.
Für genau Erklärungen siehe Hausarbeit.
Giffler & Thompson - Algorithmus -> Prioritätsregeln: priorityrule = ("SPT", "Random", "SPT_operation", "MWKR"))
CP-Solver: Zeitlimit (in Sekunden): TimeLimit = irgendeine Zahl größer Null
Lokale Suche: -> Prioritätsregeln: priorityrule = ("SPT", "Random", "SPT_operation", "MWKR") für GTA
Tabu-Suche:
-> Prioritätsregeln: priorityrule = ("SPT", "Random", "SPT_operation", "MWKR") für GTA
-> Tabu-Länge: Tabu_len = ("static", "dynamic", "adaptive", "adaptive2", "combi_adaptive")
-> Tabu-Kriterium (was setzt ich Tabu): TK = ("TK1", "TK2")
-> Zeitlimit (in Sekunden): TimeLimit = irgendeine Zahl größer Null 
'''

solve_GTA(benchmark_instances, priorityrule = "MWKR")
solve_CP(benchmark_instances, TimeLimit = 5)
solve_LS(benchmark_instances, priorityrule = "MWKR")
solve_TS(benchmark_instances, priorityrule = "MWKR", Tabu_len = "combi_adaptive", TK = "TK2", TimeLimit = 5)