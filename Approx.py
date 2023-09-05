def approx_makespan(inst, PM, SM, PJ, SJ, r, q, swap_job, end_dummy_note):
    """
    Approximiert den neuen Makspan, falls Operationen getauscht werden
    :param inst: JSP-Instanz
    :param PM: Maschinenvorgänger-Dictonary
    :param SM: Maschinennachfolger-Dictonary
    :param PJ: Jobvorgänger-Dictonary
    :param SJ: Jobnachfolger-Dictonary
    :param r: Dictonary der frühestmöglichen Start-Zeiten aller Operationen
    :param q: Dictonary der Tale-Zeiten aller Operationen
    :param swap_job: Zu Tauschende Operationen
    :param end_dummy_note: fiktiver Endknoten des Schedules
    :return: m_approx (approximierter Makespan)
    """
    crit = swap_job[0] #erste Operation (a) der zu tauschenden Operationen
    snd_op = swap_job[1] #zweite Operation (b) der zu tauschenden Operationen

    #Approximationsrechnung nach Taillard: Parallel Taboo Search Techniques for the JSP (1993)
    #dafür werden die Bearbeitungszeiten und Startzeitpunkte der Job-/Maschinen-Nachfolger/Vorgänger Operationen benötigt
    #diese berechnen sich wie folgt:
    PM_a = PM[crit]
    if PM_a[0] == -1: #falls Maschinenvorgänger von a ein fiktiver Knoten ist
        d_PM_a = 0
        r_PM_a = 0
    else:
        d_PM_a = inst[PM_a[0]][PM_a[1]][1]
        r_PM_a = r[PM_a]
    PJ_b = PJ[snd_op]
    if PJ_b[0] == -1: #falls Jobvorgänger von b ein fiktiver Knoten ist
        d_PJ_b = 0
        r_PJ_b = 0
    else:
        d_PJ_b = inst[PJ_b[0]][PJ_b[1]][1]
        r_PJ_b = r[PJ_b]
    d_b = inst[snd_op[0]][snd_op[1]][1]
    PJ_a = PJ[crit]
    if PJ_a[0] == -1: #falls Jobvorgänger von a ein fiktiver Knoten ist
        d_PJ_a = 0
        r_PJ_a = 0
    else:
        d_PJ_a = inst[PJ_a[0]][PJ_a[1]][1]
        r_PJ_a = r[PJ_a]
    d_a = inst[crit[0]][crit[1]][1]
    SM_b = SM[snd_op]
    if SM_b[0] == end_dummy_note: #falls Maschinennachfolger von b ein fiktiver Knoten ist
        q_SM_b = 0
    else:
        q_SM_b = q[SM_b]
    SJ_a = SJ[crit]
    if SJ_a[0] == end_dummy_note: #falls Jobnachfolger von a ein fiktiver Knoten ist
        q_SJ_a = 0
    else: 
        q_SJ_a = q[SJ_a]
    SJ_b = SJ[snd_op]
    if SJ_b[0] == end_dummy_note: #falls Jobnachfolger von b ein fiktiver Knoten ist
        q_SJ_b = 0
    else:
        q_SJ_b = q[SJ_b]
    
    #Endrechnung:
    r_b_line = max(r_PM_a + d_PM_a, r_PJ_b + d_PJ_b)
    r_a_line = max(r_b_line + d_b, r_PJ_a + d_PJ_a)
    q_a_line = max(q_SM_b, q_SJ_a) + d_a
    q_b_line = max(q_a_line, q_SJ_b) + d_b
    m_approx = max(r_b_line + q_b_line, r_a_line + q_a_line)

    return m_approx