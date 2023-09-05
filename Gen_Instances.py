import random

def Gen_Bench_Instances(blocks, nmbr_instances_each_block):
    '''
    Erzeugt Job-Shop Instanzen anhand der von Taillard (1993) dargestellten Struktur.
    :param blocks: Instanzklassen 
    :param nmbr_instances_each_block: Anzahl zu generierender Instanzen je Block
    :return: benchmark_instances (Benchmark-Instanzen in einer Liste abgespeichert)
    '''
    random.seed(1)
    benchmark_instances = {} #Instanz-Liste
    random_seed = "1"
    for block in blocks:
        n = block[0] #fixiere Anz. Maschinen und Aufträge
        m = block[1]
        random_seed_block = random_seed + str(n) + str(m)
        for instance in range(nmbr_instances_each_block):
            random_seed_block_iteration = random_seed_block + str(instance)
            random.seed(int(random_seed_block_iteration))
            jobs_data = [] #Liste einer Instanz
            shuflist = [machineId for machineId in range(m)] #erstelle MaschinenId-Liste
            for order in range(n):
                job = [] #erstelle Job-Liste
                random.shuffle(shuflist) #shuffle die MaschinenId-Liste, um zufällige Verteilung der Operationen zu den Maschinen sicherzustellen
                for machine in range(m):
                    processtime = random.randint(1, 99) #erzeuge zufällige Bearbeitungszeit einer Operation
                    machineId_processtime = (shuflist[machine], processtime) #erstelle Tupel
                    job.append(machineId_processtime) #füge Tupel der Job-Liste hinzu
                jobs_data.append(job) #füge Job zur Liste der erstellen Instanz hinzu
            benchmark_instances[random_seed_block_iteration] = jobs_data #füge Instanz zur Instanz-Liste hinzu
    return benchmark_instances