import copy
import time
from Crit_Operations import calculate_release
from Crit_Operations import calculate_tale
from Crit_Operations import calculate_critical
from Approx import approx_makespan
from Plot_Gantt import Plot #falls Bedarf nach Gantt Plot besteht (Vorsicht: Anz. Jobs muss kleiner 11 sein!)

def Tabu_Search(inst, makespan, PM, SM, PJ, SJ, Tabu_len, TK, TimeLimit, end_dummy_note):
    """
    Verbessert Startlösung mit Hilfe des Tabu-Suche-Verfahrens
    :param inst: JSP-Instanz
    :param makespan: Makespan des Schedule
    :param PM: Maschinenvorgänger-Dictonary
    :param SM: Maschinennachfolger-Dictonary
    :param PJ: Jobvorgänger-Dictonary
    :param SJ: Jobnachfolger-Dictonary
    :param Tabu_len: Tabu-Länge ("static", "dynamic", "adaptive", "adaptive2", "combi_adaptive")
    :param TK: Tabu-Kriterium (was setzt ich Tabu -> "TK1", "TK2")
    :param TimeLimit: Zeitlimit
    :param end_dummy_note: fiktiver Endknoten des Schedules
    :return: makespan_star (bester gefundener Makespan)
    :return:  it_count (Anz. absolvierter Iterationen)
    :return: TL_full (Tabu-Liste voll?) 
    :return: break_no_neighbor (Kein Nachbar gefunden?)
    """
    tabu_time_start = time.time() #starte Zeitnahme
    makespan_star = makespan #weise Startlösung als momentane Lösung zu
    makespan_current = makespan
    SM_current = copy.deepcopy(SM)
    PM_current = copy.deepcopy(PM)
    it_count = 1 #Iterationszähler
    it_count_nbs = 0 #Iterationszähler Abbruchkriterium (max. Anzahl Iterationen ohne neue beste Lösung)
    TL = [] #Tabu-Liste
    TL_full = False #für Ausgabe
    break_no_neighbor = False #für Ausgabe
    break_criterium = True #Abbruchkriterium, falls kein Nachbar gefunden oder Zeitlimit überschritten

    #definiere Tabu-Länge nach eingestelltem Parameter:
    m = len(inst[0])
    n = len(inst)
    if Tabu_len == "combi_adaptive":
        if n >= 50:
            Tabu_len = "adaptive"
        else:
            Tabu_len = "adaptive2"
    if Tabu_len == "static":
        TL_len = 25
    if Tabu_len == "dynamic" or Tabu_len == "adaptive" or Tabu_len == "adaptive2":
        TL_len = round((n+m)/2)
        TH_min = round((n+m)/2) - round((n+m)/4)
        TH_max = round((n+m)/2) + round((n+m)/4)
    
    while it_count_nbs <= 49 and break_criterium == True: #Solane nicht eins der Abbruchkriterien erfüllt sind
        r_current, makespan_current = calculate_release(inst, PM_current, SM_current, PJ, SJ, end_dummy_note)
        q_current = calculate_tale(inst, PM_current, SM_current, PJ, SJ, end_dummy_note)
        crit_operations = calculate_critical(r_current, q_current, makespan_current)
        makespan_best_neighbor = float("inf")
        swap_list = []
        for crit in crit_operations: #erstelle Kandidatenliste nach N1
            snd_op = SM_current[crit] #Maschinennachfolger als zweite Operation im Tausch
            swap = [crit, snd_op]
            if snd_op in crit_operations:
                if r_current[crit] + inst[crit[0]][crit[1]][1] == r_current[snd_op]: #falls direkt aufeinanderfolgend
                    if TK == "TK1": 
                        if swap not in TL: #falls nicht tabu
                            swap_list.append(swap)                  
                    if TK == "TK2": 
                        if crit not in TL: #falls nicht tabu
                            if snd_op not in TL:
                                swap_list.append(swap)
                    
        if len(swap_list) > 0: #falls Kandidatenliste gefüllt
            for swap in swap_list: #iteriere über Kandidatenliste
                crit = swap[0]
                snd_op = swap[1]
                
                makespan_approx = approx_makespan(inst, PM_current, SM_current, PJ, SJ, r_current, q_current, 
                                                  swap, end_dummy_note)
                if makespan_approx < makespan_best_neighbor: #führe Tausch durch, falls approximierter Wert besser als bester Nachbar
                    #aktualisiere Maschinenvorgänger und Nachfolger:
                    SM_neighbor = copy.deepcopy(SM_current)
                    PM_neighbor = copy.deepcopy(PM_current)
                    PM_neighbor[crit] = snd_op
                    SM_neighbor[crit] = SM_current[snd_op]
                    PM_neighbor[snd_op] = PM_current[crit]
                    SM_neighbor[snd_op] = crit
                    if PM_current[crit][0] > -1: #falls Vorgänger ein fiktiver Knoten
                        SM_neighbor[PM_current[crit]] = snd_op   
                    if SM_current[snd_op][0] < end_dummy_note: #falls Nachfolger ein fiktiver Knoten
                        PM_neighbor[SM_current[snd_op]] = crit

                    r_neighbor, makespan_neighbor = calculate_release(inst, PM_neighbor, SM_neighbor, PJ, SJ, 
                                                                      end_dummy_note)
       
                    if makespan_neighbor < makespan_best_neighbor: #falls besser -> aktualisiere bester Nachbar
                        makespan_best_neighbor = makespan_neighbor
                        SM_best_neighbor = copy.deepcopy(SM_neighbor)
                        PM_best_neighbor = copy.deepcopy(PM_neighbor)
                        trans_swap_best_neighbor = [snd_op, crit] #Elemente in Swap getauscht
                        
            #update Tabu-Liste/Länge:
            if len(TL) == TL_len: #falls TL voll, dann entferne 1. Element
                TL_full = True #für Ausgabe
                TL.remove(TL[0])
            if TK == "TK1":
                TL.append(trans_swap_best_neighbor)
            if TK == "TK2":
                TL.append(trans_swap_best_neighbor[0])
            if Tabu_len == "adaptive":
                if makespan_best_neighbor < makespan_current and TL_len > TH_min:
                    if len(TL) == TL_len:
                        TL.remove(TL[0])
                    TL_len = TL_len - 1
                if makespan_best_neighbor >= makespan_current and TL_len < TH_max:
                    TL_len = TL_len + 1

            #aktualisiere momentane Lösung:
            makespan_current = makespan_best_neighbor 
            SM_current = copy.deepcopy(SM_best_neighbor)
            PM_current = copy.deepcopy(PM_best_neighbor)

            if makespan_current < makespan_star: #falls momentane Lösung besser als beste gefundene, aktualisiere beste
                makespan_star = makespan_current
                it_count_nbs = 0 #setzte max. Iterationen-Count (ohne neue beste Lösung) zurück
                if Tabu_len == "adaptive": #update Tabu-Liste/Länge
                    TL = []
                    if TK == "TK1":
                        TL.append(trans_swap_best_neighbor)
                    if TK == "TK2":
                        TL.append(trans_swap_best_neighbor[0])
                    TL_len = 1
            else:
                it_count_nbs = it_count_nbs + 1 #setzte max. Iterationen-Count (ohne neue beste Lösung) + 1
                  
        else: #falls kein Tausch möglich, aktualisiere Abbruchkriterium zu "Beenden"
            break_criterium = False
            break_no_neighbor = True
        it_count = it_count + 1

        if Tabu_len == "adaptive2": #update Tabu-Liste/Länge
            if it_count_nbs == 20:
                TL_len = round(round((n+m)/2)*0.5)
                del_elements = len(TL) - TL_len
                for element in range(del_elements):
                    TL.remove(TL[0])
            if it_count_nbs == 0:
                TL_len = round((n+m)/2)

        tabu_time = time.time() - tabu_time_start #messe vergangene Zeit
        if tabu_time >= TimeLimit: #falls Zeitlimit überschritten, aktualisiere Abbruchkriterium zu "Beenden"
            break_criterium = False
    return makespan_star, it_count, TL_full, break_no_neighbor