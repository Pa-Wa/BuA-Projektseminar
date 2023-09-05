import time
import plotly.figure_factory as ff
import pandas as pd

from Giffler_Thompson import GTA
from CP_solver import OR_Solver
from LocalSearch import Local_Search
from TabuSearch import Tabu_Search

def solve_GTA (bench_instances, priorityrule):
    """
    Löst mit Hilfe des Giffler und Thompson Algorithmus alle generierten Instanzen und speichert Lösungsdaten in einer CSV-Datei ab
    :param bench_instances: generierte JSP-Benchmark-Instanzen
    :param priorityrule: gewählte Prioritätsregel
    :return: None
    """
    solution_list = []
    for key in bench_instances:  #gehe alle Instanzen durch
        instance = bench_instances[key]
        start_time = time.time() #definiere Startzeitpunkt
        PM_GTA, SM_GTA, PJ, SJ, makespan_GTA, end_note = GTA(instance, priorityrule)
        time_GTA = time.time() - start_time #berechne GTA Rechenzeit
        solution = {"ID": key, "Time_GTA": round(time_GTA, 10), "Makespan_GTA": makespan_GTA, "PrioRule": priorityrule}
        solution_list.append(solution)
    df_solution = pd.DataFrame(solution_list)
    print(df_solution)
    #df_solution.to_csv('solution_gta.csv', sep=';') #erstelle CSV-Datei mit Lösungsdaten

def solve_CP (bench_instances, TimeLimit):
    """
    Löst mit Hilfe des CP-Solvers alle generierten Instanzen und speichert Lösungsdaten in einer CSV-Datei ab
    :param bench_instances: generierte JSP-Benchmark-Instanzen
    :param TimeLimit: Zeit-Limit zum Lösen einer Instanz
    :return: None
    """
    solution_list = []
    for key in bench_instances: #gehe alle Instanzen durch
        instance = bench_instances[key]
        solution_time, makespan_CP, opt_sol = OR_Solver(instance, TimeLimit)
        solution = {"ID": key, "Time": solution_time, "Makespan": makespan_CP, "Optimal?": opt_sol}
        solution_list.append(solution)
    df_solution = pd.DataFrame(solution_list)
    print(df_solution)
    #df_solution.to_csv('solution_cp.csv', sep=';') #erstelle CSV-Datei mit Lösungsdaten

def solve_LS (bench_instances, priorityrule):
    """
    Löst mit Hilfe der Lokalen Suche alle generierten Instanzen und speichert Lösungsdaten in einer CSV-Datei ab
    :param bench_instances: generierte JSP-Benchmark-Instanzen
    :param priorityrule: gewählte Prioritätsregel
    :return: None
    """
    solution_list = []
    for key in bench_instances: #gehe alle Instanzen durch
        instance = bench_instances[key]
        start_time = time.time() #definiere Startzeit
        PM_GTA, SM_GTA, PJ, SJ, makespan_GTA, end_note = GTA(instance, priorityrule)
        time_GTA = time.time() - start_time #berechne GTA Rechenzeit
        makespan_star, it_count_ls = Local_Search(instance, makespan_GTA, PM_GTA, SM_GTA, PJ, SJ, end_note)
        ls_time = time.time() - start_time #berechne LS Rechenzeit
        solution = {"ID": key, "Time_GTA": round(time_GTA, 10), "Makespan_GTA": makespan_GTA,
                    "Time_LS": round(ls_time, 3), "Makespan_LS": makespan_star, "It_count": it_count_ls - 1}
        solution_list.append(solution)
    df_solution = pd.DataFrame(solution_list)
    print(df_solution)
    #df_solution.to_csv('solution_ls.csv', sep=';') #erstelle CSV-Datei mit Lösungsdaten

def solve_TS(bench_instances, priorityrule, Tabu_len, TK, TimeLimit):
    """
    Löst mit Hilfe der Tabu-Suche alle generierten Instanzen und speichert Lösungsdaten in einer CSV-Datei ab
    :param bench_instances: generierte JSP-Benchmark-Instanzen
    :param priorityrule: gewählte Prioritätsregel
    :param Tabu_len: Tabu-Länge ("static", "dynamic", "adaptive", "adaptive2", "combi_adaptive")
    :param TK: Tabu-Kriterium (was setzt ich Tabu -> "TK1", "TK2")
    :param TimeLimit: Zeitlimit
    :return: None
    """
    solution_list = []
    for key in bench_instances: #gehe alle Instanzen durch
        instance = bench_instances[key]
        start_time = time.time() #definiere Startzeitpunkt
        PM_GTA, SM_GTA, PJ, SJ, makespan_GTA, end_note = GTA(instance, priorityrule)
        time_GTA = time.time() - start_time #berechne GTA Rechenzeit
        makespan_star, it_count_ts, TL_full, break_no_nb = Tabu_Search(instance, makespan_GTA, PM_GTA, SM_GTA,
                                                                    PJ, SJ, Tabu_len, TK,
                                                                    TimeLimit, end_dummy_note = end_note)
        ts_time = time.time() - start_time #berechne TS Rechenzeit
        solution = {"ID": key, "Time_GTA": round(time_GTA, 10), "Makespan_GTA": makespan_GTA,
                    "Time_TS": round(ts_time, 3), "Makespan_TS": makespan_star, "It_count": it_count_ts - 1,
                    "TL full?": TL_full, "No Neighbor?": break_no_nb}
        solution_list.append(solution)
    df_solution = pd.DataFrame(solution_list)
    print(df_solution)
    #df_solution.to_csv('solution_ts.csv', sep=';') #erstelle CSV-Datei mit Lösungsdaten