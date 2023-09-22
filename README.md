# Job Shop Scheduling Problem (Constraint Programming vs. Tabu Search)

Autoren: Yann Chevelaz und Pascal Wagener

Business Analytics Projektseminar Wintersemester 2022

Universität Siegen

---

#### Inhalt:

* Generierung von JSP Instanzen
* Implementierung des Giffler-Thompson Algorithmus zur Erzeugung einer zulässigen Startlösung
* Implementierung einer Lokalen Suche mit Nachbarschaftsdefinition
* Implementierung einer Tabu Suche mit Nachbarschafsdefinition
* Nutzen des CP Solvers von Google ORtools für das JSP
* Vergleich der Performance der einzelnen Methoden

---

#### Doku:
* Main: Aufruf & Ausführung der Funktionen aus Gen_Instances (zur Instanzgenerierung) und der Solve-Datei (zum Lösen des GTA, LS, TS und CP)
* SolMethod: Aufruf & Ausführung der Funktionen aus GTA, LS, TS und CP
* Gen_Instances: Generierung der JSP-Instanzen
* Giffler_Thompson: GTA-Heuristik zur Erstellung einer Ausgangslösung
* Crit_Operations: Bestimmung der Release-, Tale Zeiten und der kritischen Operationen (für LS/TS)
* Approx: Approximierung des Makespan (für LS & TS)
* LocalSearch: Lokale Suche
* TabuSearch: Tabu-Suche mit verschiedenen Einstellungsmöglichkeiten
* CP_solver: CP-Solver mittels OR-Tools
* Plot_Gantt: Zum PLotten eines Gantt Charts
* Seminararbeit (PDF): Schriftliche Ausführungen zu JSP, Methoden etc.
