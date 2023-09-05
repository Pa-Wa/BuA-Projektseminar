import random
import copy

def GTA(inst, priorityrule):
    """
    Wendet den Giffler und Thompson-Alg. an um eine erste zulässige Lösung zu finden
    :param inst: Job-Shop-Instanz
    :param priorityrule: Gewählte Prioritätsregel ("SPT", "Random", "SPT_operation", "MWKR")
    :return PM: Maschinenvorgänger-Dictonary
    :return SM: Maschinennachfolger-Dictonary
    :return PJ: Jobvorgänger-Dictonary
    :return PJ: Jobnachfolger-Dictonary
    :return: Makespan (Makespan des Schedule)
    :return: end_dummy_note (fiktiver letzter Knoten im Schedule)
    """
    #Vorarbeit:
    instance_del = copy.deepcopy(inst) #Instanz-Liste die im folgenden um bereits zugewiesene Operationen verkürzt wird
    machines_count = 1 + max(task[0] for job in inst for task in job) #Anzahl Maschinen
    Z = {job: 0 for job in range(machines_count)} #frühester Maschinen-Start-Zeitpunkt
    machine_assignment = [[]for machine in range(machines_count)] #Maschinenbelegung
    R = {job: 0 for job in range(len(inst))} #frühester Auftrags-Start-Zeitpunkt
    if priorityrule == "SPT": #Shortes Process Time vom gesamten Auftrag
        PT = {job: sum(inst[job][operation][1] for operation in range(len(inst[job]))) for job in range(len(inst))}
    if priorityrule == "MWKR": #Most Work Remaining
        WKR = {job: sum(inst[job][operation][1] for operation in range(len(inst[job]))) for job in range(len(inst))}
    avail_ops = {job: (inst[job][0][0], inst[job][0][1], 0) for job in range(len(inst))} #Operationen die eingeplant werden können (mId,PT,r)
    C_star = {job: 0 for job in range(len(inst))} #frühester Zeitpunkt zu dem ein einzuplanender Auftrag fertiggestellt werden kann 
    PM = {(job,operation): 0 for job in range(len(inst)) for operation in range(len(inst[job]))} #MaschinenvorgängerDict
    SM = {(job,operation): 0 for job in range(len(inst)) for operation in range(len(inst[job]))} #MaschinennachfolgerDict

    #Hauptschleife:
    while bool (avail_ops) == True: #solange bis alle Operationen eingeplant sind

        #Berechnung C* und einzuplanende Maschine:
        for key in avail_ops:
            C = avail_ops[key][1] + max(R[key], Z[avail_ops[key][0]])
            C_star[key] = C
        planned_job = min(C_star, key = C_star.get) #aktuell einzuplanender Job   
        machine = avail_ops[planned_job][0] #einzuplanende Maschine

        #prüfe, ob weitere Aufträge auf Maschine eingeplant werden können und entscheide nach Prioritätsregel:
        possible_jobs = []
        for key in avail_ops:
            if avail_ops[key][0] == machine:
                if avail_ops[key][2] < C_star[planned_job]:
                    possible_jobs.append(key)
        if len(possible_jobs) != 1: #sollten mehrere Jobs einplanbar sein, dann wähle Job nach Prioritätsregel
            if priorityrule == "SPT": #kürzeste Auftagszeit
                SPT = float("inf")
                for job in possible_jobs:
                    if PT[job] < SPT:
                        SPT = PT[job]
                        planned_job = job
            if priorityrule == "MWKR": #meiste verbleibende Bearbeitungszeit
                MWKR = 0
                for job in possible_jobs:
                    if WKR[job] > MWKR:
                           MWKR = WKR[job]
                           planned_job = job
            if priorityrule == "SPT_operation": #kürzeste Bearbeitungszeit der verfügbaren Operationen
                SPT_op = float("inf")
                for job in possible_jobs:
                    if avail_ops[job][1] < SPT_op:
                        SPT_op = avail_ops[job][1]
                        planned_job = job
            if priorityrule == "Random": #zufällige Auswahl
                planned_job = random.choice(possible_jobs)
        planned_operation = inst[planned_job].index((machine, avail_ops[planned_job][1]))
        
        #speichere & update:
        machine_assignment[machine].append((planned_job,inst[planned_job].index((machine, 
                                            avail_ops[planned_job][1])), avail_ops[planned_job][1]))
        Z[machine] = avail_ops[planned_job][1] + max(Z[machine], R[planned_job])
        R[planned_job] = Z[machine]
        if len(machine_assignment[machine]) == 1: #falls dies der erste Auftrag auf der Maschine ist
            PM[(planned_job,planned_operation)] = (-1, machine) #dann ist der Vorgänger ein fiktiver Knoten
        else:
            PM[(planned_job,planned_operation)] = (machine_assignment[machine][-2][0], 
                                                   machine_assignment[machine][-2][1]) #ansonsten weise den Vorgänger zu
        predecessor = PM[(planned_job, planned_operation)]
        if predecessor[0] > -1: #wenn der Vorgänger kein fiktiver Knote ist
            SM[(predecessor[0], predecessor[1])] = (planned_job, planned_operation) #dann weise ihm den momentanen Job als Nachfolger zu
        if priorityrule == "MWKR": 
            WKR[planned_job] = WKR[planned_job] - avail_ops[planned_job][1]
        instance_del[planned_job].remove((machine, avail_ops[planned_job][1]))
        if len(instance_del[planned_job]) == 0: #falls ein Auftrag komplett eingeplant ist, dannn entferne ihn
            avail_ops.pop(planned_job)
            C_star.pop(planned_job)
        else: #wenn nicht, dann füge nächste Operation in avail_ops zu
            operation = instance_del[planned_job][0]
            avail_ops[planned_job] = (operation[0], operation[1], R[planned_job])

    #passe SM weiter an und erstelle PJ,SJ:
    end_dummy_note = len(inst) #fiktiver Endknoten des Schedule
    for key in SM: #weise den letzten Operationen einer Maschine als Nachfolger den fiktiven Knoten zu
        if SM[key] == 0:
            SM[key] = (end_dummy_note, inst[key[0]][key[1]][0])
    makespan = Z[max(Z, key = Z.get)] #Makespan des erstellten Schedule
    PJ = {(job, operation): 0 for job in range(len(inst)) for operation in range(len(inst[job]))} #erstelle Job-Vorgänger_operation
    for key in PJ:
        if key[1]-1 >= 0:
            PJ[key] = (key[0], key[1]-1)
        else:
            PJ[key] = (-1, -1)
    SJ = {(job, operation): 0 for job in range(len(inst)) for operation in range(len(inst[job]))} #erstelle Job-Nachfolger-Operation
    for key in SJ:
        if key[1] + 1 <= len(inst[key[0]]) - 1: 
            SJ[key] = (key[0], key[1]+1)
        else:
            SJ[key] = (end_dummy_note, end_dummy_note)

    return PM, SM, PJ, SJ, makespan, end_dummy_note