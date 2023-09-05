import copy
from Crit_Operations import calculate_release
from Crit_Operations import calculate_tale
from Crit_Operations import calculate_critical
from Approx import approx_makespan
from Plot_Gantt import Plot #falls Bedarf nach Gantt Plot besteht (Vorsicht: Anz. Jobs muss kleiner 11 sein!)

def Local_Search(inst, makespan, PM, SM, PJ, SJ, end_dummy_note):
    """
    Verbessert Startlösung mit Hilfe des Lokale Suche-Verfahrens
    :param inst: JSP-Instanz
    :param makespan: Makespan des Schedule
    :param PM: Maschinenvorgänger-Dictonary
    :param SM: Maschinennachfolger-Dictonary
    :param PJ: Jobvorgänger-Dictonary
    :param SJ: Jobnachfolger-Dictonary
    :param end_dummy_note: fiktiver Endknoten des Schedules
    :return: makespan_current (bester gefundener Makespan)
    :return:  it_count (Anz. absolvierter Iterationen)
    """
    #Setze Startlösung als aktuelle Lösung
    makespan_current = makespan
    SM_current = copy.deepcopy(SM)
    PM_current = copy.deepcopy(PM)
    it_count = 1
    break_criterium = True
    while break_criterium == True:
        r_current, makespan_current = calculate_release(inst, PM_current, SM_current, PJ, SJ, end_dummy_note)
        q_current = calculate_tale(inst, PM_current, SM_current, PJ, SJ, end_dummy_note)
        crit_operations = calculate_critical(r_current, q_current, makespan_current)
        makespan_best_neighbor = makespan_current 
        swap_list = []
        for crit in crit_operations: #erstelle Kandidatenliste nach N1
                snd_op = SM_current[crit] #Maschinennachfolger als zweite Operation im Tausch
                swap = [crit, snd_op]
                if snd_op in crit_operations:
                    if r_current[crit] + inst[crit[0]][crit[1]][1] == r_current[snd_op]: #falls direkt aufeinanderfolgend
                        swap_list.append(swap)
        if len(swap_list) > 0: #falls Kandidatenliste gefüllt
            for swap in swap_list: #iteriere über Kandidatenliste
                crit = swap[0]
                snd_op = swap[1]
                makespan_approx = approx_makespan(inst, PM_current, SM_current, PJ, SJ, r_current,
                                                   q_current, swap, end_dummy_note)

                if makespan_approx < makespan_best_neighbor: #führe Tausch durch, falls approximierter Wert besser als bester Nachbar
                    SM_neighbor = copy.deepcopy(SM_current)
                    PM_neighbor = copy.deepcopy(PM_current)
                    #aktualisiere Maschinenvorgänger und Nachfolger
                    PM_neighbor[crit] = snd_op
                    SM_neighbor[crit] = SM_current[snd_op]
                    PM_neighbor[snd_op] = PM_current[crit]
                    SM_neighbor[snd_op] = crit
                    if PM_current[crit][0] > -1: #falls Vorgänger ein fiktiver Knoten
                        SM_neighbor[PM_current[crit]] = snd_op               
                    if SM_current[snd_op][0] < end_dummy_note: #falls Nachfolger ein fiktiver Knoten
                        PM_neighbor[SM_current[snd_op]] = crit 
                    r_neighbor, makespan_neighbor = calculate_release(inst, PM_neighbor, SM_neighbor,
                                                                       PJ, SJ, end_dummy_note)
            
                    if makespan_neighbor < makespan_best_neighbor: #falls besser -> aktualisiere bester Nachbar
                        makespan_best_neighbor = makespan_neighbor
                        SM_best_neighbor = copy.deepcopy(SM_neighbor)
                        PM_best_neighbor = copy.deepcopy(PM_neighbor)
                        
            if makespan_best_neighbor < makespan_current: #falls besser -> aktualisiere momentane Lösung
                makespan_current = makespan_best_neighbor
                SM_current = copy.deepcopy(SM_best_neighbor)
                PM_current = copy.deepcopy(PM_best_neighbor)
            else:
                break_criterium = False #falls keine bessere Lösung als momentane gefunden wurde, beende Lokale Suche
        else:
            break_criterium = False #falls Kandidatenliste leer, beende Lokale Suche (theoretisch nicht möglich!)
        it_count = it_count + 1
    return makespan_current, it_count