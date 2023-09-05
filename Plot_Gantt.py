import plotly.figure_factory as ff
#Achtung: Anzahl Jobs muss <= 10 sein! Asonsten Fehlermeldung "zu wenig Farben" -> reicht aber zum Überprüfen der Methoden
def Plot (inst, SM, r):
    """
    Erstellt Gantt-Plot des Schedule
    :param inst: JSP-Instanz
    :param SM: Maschinennachfolger-Dictonary
    :param r: Dictonary der frühestmöglichen Start-Zeiten aller Operationen
    :return None
    """
    schedule_list = [] #Liste der einzelnen Operattions-Dictonarys (beinhaltet Start, Ende, Jobzugehörigkeit)
    for key in SM:
        schedule_dic = dict(Task = inst[key[0]][key[1]][0], Start = r[key], Finish = r[key] + inst[key[0]][key[1]][1], Resource = f"Job_{key[0]}")
        schedule_list.append(schedule_dic)
    schedule_list = sorted(schedule_list, key=lambda x: x["Task"])
    fig = ff.create_gantt(schedule_list, index_col = 'Resource', show_colorbar=True, group_tasks=True)
    fig.layout.xaxis.type = "linear"
    fig.show()