def calculate_release(inst, PM, SM, PJ, SJ, end_dummy_note):
    """
    Berechnet frühestmögliche Start-Zeiten der einzelnen Operationen
    :param inst: JSP-Instanz
    :param PM: Maschinenvorgänger-Dictonary
    :param SM: Maschinennachfolger-Dictonary
    :param PJ: Jobvorgänger-Dictonary
    :param SJ: Jobnachfolger-Dictonary
    :param end_dummy_note: fiktiver Endknoten des Schedules
    :return: r (Dictonary der frühestmöglichen Start-Zeiten aller Operationen)
    :return: makespan (Makespan des Schedule)
    """
    r = {(job,operation): -1 for job in range(len(inst)) for operation in range(len(inst[job]))} #frühestmöglichen Start-Zeiten aller Operationen
    Q = [] #Liste bestehend aus Operationen i für die r_i berechenbar ist
    makespan = 0 #auf Null setzen und im späteren Verlauf aktualisieren
    first_operation_of_job = [(job, 0) for job in range(len(inst))] #Liste aller ersten Operationen eines Jobs
    for operation in first_operation_of_job: #füge alle Operationen hinzu die sowohl 1. ihres Jobs sind als auch 1. auf einer Maschine
        if PM[operation][0] == -1:
            Q.append(operation) 

    while len(Q) != 0: #für alle Operationen
        i = Q[0]
        Q.remove(i)
        pm = PM[i]
        pj = PJ[i] 

        #Berechnung r:
        if pm[0] > -1: #falls Maschinen-Vorgänger kein fiktiver Knoten ist
            fp = r[pm] + inst[pm[0]][pm[1]][1]
        else:
            fp = 0
        if pj[0] > -1: #falls Job-Vorgänger kein fiktiver Knoten ist
            sp = r[pj] + inst[pj[0]][pj[1]][1]
        else:
            sp = 0
        r[i] = max(fp, sp) #berechne r

        #füge die nächsten Operationen die berechenbar sind zu Q hinzu:
        if SJ[i][0] != end_dummy_note: #falls Job-Nachfolger kein fiktiver Knoten ist
            sj = SJ[i]
            if sj not in Q:
                if PM[sj][0] == -1: #falls Maschinenvorgänger vom Jobnachfolger ein fiktiver Knoten ist
                    Q.append(sj)
                elif r[PM[sj]] > -1: #oder r vom Maschinenvorgänger vom Jobnachfolger bereits berechnet wurde
                    Q.append(sj)
        if SM[i][0] != end_dummy_note: #siehe oben nur für Jobvorgänger vom Maschinennachfolger
            sm = SM[i]
            if sm not in Q:
                if PJ[sm][0] == -1:
                    Q.append(sm)
                elif r[PJ[sm]] > -1:
                    Q.append(sm)

        #berechne und ggf. aktualisiere Makespan:
        if SM[i][0] == end_dummy_note:
            if r[i] + inst[i[0]][i[1]][1] > makespan:
                makespan = r[i] + inst[i[0]][i[1]][1]

    return r, makespan

def calculate_tale(inst, PM, SM, PJ, SJ, end_dummy_note):
    """
    Berechnet Tail-Zeiten der einzelnen Operationen
    :param inst: JSP-Instanz
    :param PM: Maschinenvorgänger-Dictonary
    :param SM: Maschinennachfolger-Dictonary
    :param PJ: Jobvorgänger-Dictonary
    :param SJ: Jobnachfolger-Dictonary
    :param end_dummy_note: fiktiver Endknoten des Schedules
    :return: q (Dictonary der Tale-Zeiten aller Operationen)
    """
    q = {(job,operation): -1 for job in range(len(inst)) for operation in range(len(inst[job]))} #Tail-Zeiten aller Operationen
    T = [] #Liste bestehend aus Operationen i für die q_i berechenbar ist
    last_operation_of_job = [(job,len(inst[job])-1) for job in range(len(inst))] #Liste aller letzten Operationen eines Jobs
    for operation in last_operation_of_job: #füge alle Operationen hinzu die sowohl letzter ihres Jobs sind als auch letzter auf einer Maschine
        if SM[operation][0] == end_dummy_note:
            T.append(operation)

    while len(T) != 0: #für alle Operationen
        i = T[0]
        T.remove(i)
        sj = SJ[i]
        sm = SM[i]

        #Berechnung q:
        if sm[0] != end_dummy_note: #falls Maschinennachfolger kein fiktiver Knoten ist
            fp = q[sm]
        else:
            fp = 0
        if sj[0] != end_dummy_note: #falls Jobnnachfolger kein fiktiver Knoten ist
            sp = q[sj]
        else:
            sp = 0
        q[i] = max(fp, sp) + inst[i[0]][i[1]][1] #berechne q

        #füge die nächsten Operationen die berechenbar sind zu T hinzu:
        if PJ[i][0] > -1: #falls Jobvorgänger kein fiktiver Knoten ist
            pj = PJ[i]
            if pj not in T:
                if SM[pj][0] == end_dummy_note: #falls Maschinennachfolger vom Jobvorgänger ein fiktiver Knoten ist
                    T.append(pj)
                elif q[SM[pj]] > -1: #oder q vom Maschinennachfolger vom Jobnvorgänger bereits berechnet wurde
                    T.append(pj)
        if PM[i][0] > -1: #siehe oben nur für Jobnachfolger vom Maschinenvorgänger
            pm = PM[i]
            if pm not in T:
                if SJ[pm][0] == end_dummy_note:
                    T.append(pm)
                elif q[SJ[pm]] > -1:
                    T.append(pm)

    return q

def calculate_critical (r, q, makespan):
    """
    Bestimmt kritische Operationen und listet diese auf
    :param r: Dictonary der frühestmöglichen Start-Zeiten aller Operationen
    :param q: Dictonary der Tale-Zeiten aller Operationen
    :param makespan: Makespan des Schedule
    :return: crit_operations (Liste kritischer Operationen)
    """
    crit_operations = [] #Liste kritischer Operationen
    for key in r: #gehe alle Operationen durch und schaue ob sie kritisch sind
        if r[key] + q[key] == makespan:
            crit_operations.append(key)

    return crit_operations