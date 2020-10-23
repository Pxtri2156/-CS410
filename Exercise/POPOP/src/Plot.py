import json
import matplotlib.pyplot as plt
import numpy as np
import argparse



def Load_data(file_1X,file_UX,type):
    
    file_1X = open(file_1X,"r")
    data_1X = file_1X.read()
    file_UX = open(file_UX, "r")
    data_UX = file_UX.read()

    data_1X = json.loads(data_1X)
    data_UX = json.loads(data_UX)

    data_1 = {}
    data_2 = {}
    for key in data_1X.keys() :
        if (None not in data_1X[key][type]) and ( -1 not in data_1X[key][type] ): # Check value  nulll
            data_1[key] = data_1X[key][type]
        if (None not in data_UX[key][type]) and ( -1 not in data_UX[key][type] ): # Check value null
            data_2[key] = data_UX[key][type]

    print("{} data 1X: \n {} \n data UX: \n {}".format(type,data_1, data_2))
    return data_1, data_2

def Cacul_Standard_Deviation(data):
    SD = {}
    for key in data.keys():
        SD[key] = np.std(data[key])
    return SD

def Cacul_Avg(data):
    Avg = {}
    for key in data.keys():
        Avg[key] = np.average(data[key])
    return Avg

def Plot(data_1X, data_UX, SD_1X, SD_UX,type,fitness):

    # Convert type of Problem size string to int
    Problem_size_1X = [int(key) for key in data_1X.keys()]
    Problem_size_UX = [int(key) for key in data_UX.keys()]


    fig, ax = plt.subplots()
    ax.errorbar(Problem_size_1X, data_1X.values(), yerr=SD_1X.values() , fmt='-o', color='limegreen', label = 'Single Point Cross-over')
    ax.errorbar(Problem_size_UX, data_UX.values(), yerr=SD_UX.values() , fmt='-o', color='crimson', label = 'Uniform Cross-over')
    ax.set_title(fitness +"_" + type)
    ax.set_xlabel('Problem Size')
    ax.set_ylabel('No.')
    plt.xscale('log')
    plt.yscale('log')
    plt.xticks([10, 20, 40, 80, 160])
    ax.set_xticklabels(['10', '20', '40', '80', '160'])
    plt.legend()

    # save
    file_fig = "../Experimental_Visualization/Experience_" + fitness + "_" + type +".png"
    plt.savefig(file_fig)

def main(args):
    # Step 1: Load data 
    file_data_1X = "../Experimental_Result/Experience_1X_" + args["Fitness"] + ".json"
    file_data_UX = "../Experimental_Result/Experience_UX_" + args["Fitness"] + ".json"
    print(file_data_1X)
    print(file_data_UX)
    data_1X, data_UX = Load_data(file_data_1X, file_data_UX,args['Type'])

    # Step 2: Calculating average 
    Avg_1X = Cacul_Avg(data_1X)
    Avg_UX = Cacul_Avg(data_UX)
    print("Average {} of {} 1X : {} ".format(args['Type'],args['Fitness'],Avg_1X))
    print("Average {} of {} UX : {} ".format(args['Type'],args['Fitness'],Avg_UX))

    # Step 3: Calculating Standard Deviation

    SD_1X = Cacul_Standard_Deviation(data_1X)
    SD_UX  = Cacul_Standard_Deviation(data_UX)
    print("Standard {} of {} 1X: {}".format(args['Type'],args['Fitness'],SD_1X))
    print("Standard {} of {} UX: {}".format(args['Type'],args['Fitness'],SD_UX))


    # Step 4: Plot data 
    print("Problem size: ", data_1X.keys())
    Plot(Avg_1X, Avg_UX, SD_1X, SD_UX,args['Type'],args['Fitness'])

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Plot data')
    parser.add_argument('-f','--Fitness', type=str, required=True, help='Function Fitness: One_Max or Trap')
    parser.add_argument('-t','--Type', type=str, required=True, help='Type is MRPS or Avg_eval')
    main(vars(parser.parse_args()))