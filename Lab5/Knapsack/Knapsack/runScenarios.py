import func
import plotting

def no_Range(PS, PC, MC, IC, instances):
    """if all specified parameters are constant"""
    results = func.run(PS, PC, MC, IC, instances)
    plotting.oneEvoResults(results, PS, PC, MC, IC, instances)

def PS_Range(PS1, PS2, PC, MC, IC, instances):
    """if populationSize is in a range"""
    results = []
    results400 = []
    results700 = []
    for i in range(PS1, PS2+1):
        print(f'PS = {i}:')
        runResults = func.run(i, PC, MC, IC, instances)
        results400.append(runResults[20])
        results700.append(runResults[35])
        results.append(max(runResults))
    plotting.rangeResults([results, results700, results400], PS1, PC, MC, IC, instances, 0, PS2)

def PC_Range(PS, PC1, PC2, MC, IC, instances):
    """if pointsCount is in a range"""
    results = []
    results400 = []
    results700 = []
    for i in range(PC1, PC2+1):
        print(f'PC = {i}:')
        runResults = func.run(PS, i, MC, IC, instances)
        results400.append(runResults[20])
        results700.append(runResults[35])
        results.append(max(runResults))
    plotting.rangeResults([results, results700, results400], PS, PC1, MC, IC, instances, 1, PC2)

def MC_Range(PS, PC, MC1, MC2, IC, instances):
    """if mutationsCount is in a range"""
    results = []
    results400 = []
    results700 = []
    for i in range(MC1, MC2+1):
        print(f'MC = {i}:')
        runResults = func.run(PS, PC, i, IC, instances)
        results400.append(runResults[20])
        results700.append(runResults[35])
        results.append(max(runResults))
    plotting.rangeResults([results, results700, results400], PS, PC, MC1, IC, instances, 2, MC2)

def IC_Range(PS, PC, MC, IC1, IC2, instances):
    """if improveCount is in a range"""
    results = []
    results400 = []
    results700 = []
    for i in range(IC1, IC2+1):
        print(f'IC = {i}:')
        runResults = func.run(PS, PC, MC, i, instances)
        results400.append(runResults[20])
        results700.append(runResults[35])
        results.append(max(runResults))
    plotting.rangeResults([results, results700, results400], PS, PC, MC, IC1, instances, 3, IC2)

def runSimulation(PS, PC, MC, IC, instances):
    """choose a function to run"""
    rangeInd = func.findRangeInd(PS, PC, MC, IC, instances)
    if rangeInd == -2:
        return 'Error: more than one range input'
    elif rangeInd == -3:
        return 'Error: the "Runs count" value cannot be a range'
    elif rangeInd == -1: # no range found
        if func.areNumeric(PS, PC, MC, IC, instances):
            PS, PC, MC, IC, instances = int(PS), int(PC), int(MC), int(IC), int(instances)
        else:
            return 'Error: not all inputs are numeric'
        if func.validNumbers(PS, PC, MC, IC, instances):
            no_Range(PS, PC, MC, IC, instances)
        else:
            return "Error: some numbers are too big or too small"
    else:
        if rangeInd == 0: # PS is a range
            PS, rangeEnd = PS.split(':')
        elif rangeInd == 1: # PC is a range
            PC, rangeEnd = PC.split(':')
        elif rangeInd == 2: # MC is a range
            MC, rangeEnd = MC.split(':')
        elif rangeInd == 3: # IC is a range
            IC, rangeEnd = IC.split(':')

        if func.areNumeric(PS, PC, MC, IC, instances, rangeEnd):
            PS, PC, MC, IC, instances, rangeEnd = int(PS), int(PC), int(MC), int(IC), int(instances), int(rangeEnd)
        else:
            return 'Error: not all inputs are numeric'
        if func.validNumbers(PS, PC, MC, IC, instances, rangeInd, rangeEnd) and [PS, PC, MC, IC][rangeInd] < rangeEnd:

            if rangeInd == 0: # PS is a range
                PS_Range(PS, rangeEnd, PC, MC, IC, instances)
            elif rangeInd == 1: # PC is a range
                PC_Range(PS, PC, rangeEnd, MC, IC, instances)
            elif rangeInd == 2: # MC is a range
                MC_Range(PS, PC, MC, rangeEnd, IC, instances)
            elif rangeInd == 3: # IC is a range
                IC_Range(PS, PC, MC, IC, rangeEnd, instances)
        else:
            return "Error: some numbers are too big or too small"
