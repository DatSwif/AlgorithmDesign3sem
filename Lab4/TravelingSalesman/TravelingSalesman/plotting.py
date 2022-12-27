import matplotlib.pyplot as plot

def showResults(iterations, avgPathLengths, bestPathLengths, Lmin):
    """show results of all iterations"""
    X = list(range(iterations))
    LminConst = [Lmin for i in range(iterations)]

    plot.plot(X, avgPathLengths, color = 'r', label = 'Avg')
    plot.plot(X, bestPathLengths, color = 'b', label = 'Min')
    plot.plot(X, LminConst, color = 'g', label = 'Greedy')

    plot.xlabel('Iterations')
    plot.ylabel('Path length')

    plot.title(f'results of {iterations} iterations')
    plot.legend()
    plot.show()