# capacity P=500, 100 items, value 2-30, weight 1-20
# crossover parameter 25 >= C >= 3, mutation 100 >= M >= 2, local improvement 100 >= L >= 2
# one solution is array of 1's and 0's (added to knapsack or not)
# additional parameters: runs count, population size

import runScenarios

def main():
    while True:
        print('Enter the 5 parameters to a simulation')
        print('All have to be natural numbers')
        print('a - one number; a:b - range of numbers')
        print('only one range per simulation')
        print('--------------------------------------')

        while True:
            PS = input('Population size [10:30]: ')                     # populationSize
            PC = input('Crossover cutting points [3:25]: ')             # pointsCount
            MC = input('Mutations per iteration [2:100]: ')             # mutationsCount
            IC = input('Local improvements per iteration [2:100]: ')    # improveCount
            instances = input('Runs count [1:20]: ')
            print('--------------------------------------')
            Exception = runScenarios.runSimulation(PS, PC, MC, IC, instances)
            if Exception is None:
                break
            else:
                print(Exception)
                print('Try to enter the parameters again')
                print('--------------------------------------')

        proceed = input('input "0" to stop the program or "1" to do another run: ')
        if proceed == '0':
            break

if __name__ == "__main__":
    main()