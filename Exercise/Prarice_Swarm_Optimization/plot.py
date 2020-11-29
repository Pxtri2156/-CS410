import json
import argparse
import os
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
from matplotlib import animation
from config import PROBLEM
from Prarice_Swarm_Optimization import Pso

from config import PROBLEM

# animation function.  This is called sequentially
def animate(i, ln, ax, data_file):
    file = open(data_file,'r')
    data = json.load(file)
    population = data[0]['log_population'][i]
    ax.set_title("Gen {} {} ".format(i,data_file.split('/')[-1].split('.')[0]))
    population = np.array(population)
    ln.set_data(population[:,0],population[:,1])
    return ln,

def main(args):
    # np.random.seed(18521530)
    npts = 200
    problem = PROBLEM[args["problem"]]
    
    # Name file

    file_name = './Experimental_visualization/'+ args['problem'] + '_' \
        + args['topology']+  '_' + str(args['popsize']) + '_' + str(args['probsize']) + '.gif'
    # if os.path.exists(file_name) == False:
    #     open(file_name,'w').close()

    data_file = './Experimental_result/'+ args['problem'] + '_' \
        + args['topology']+  '_' + str(args['popsize']) + '_' + str(args['probsize']) + '.json'

    x = np.linspace(problem['lower'], problem['upper'], npts)
    y = np.linspace(problem['lower'], problem['upper'], npts)
    X, Y = np.meshgrid(x,y)
    
    if args["problem"] == "Rastrigin":
        Z = 20 + (X**2 - 10 * np.cos(2 * 3.14 * X)) + \
                (Y**2 - 10 * np.cos(2 * 3.14 * Y))
    elif args["problem"] == "Rosenbrock":
        Z = 100*(Y - X**2)**2 + (1-X)**2
    elif args["problem"] == "Eggholder":
        Z = -(Y + 47)*np.sin(np.sqrt(np.abs(X/2 + X[1] + 47 ))) \
        - (X*np.sin(np.sqrt(np.abs(X[0]- (Y + 47)))))
    elif args["problem"] == "Ackley":
       Z = -20*np.exp(-0.2*np.sqrt(0.5*(X**2 + Y**2))) \
        - np.exp(0.5*(np.cos(2*np.pi*X) + np.cos(2*np.pi*Y))) + np.e + 20

    
    fig, ax = plt.subplots(figsize=(6,6))
    cp = ax.contourf(X,Y,Z)
    ln, = plt.plot([],[],'*r')

    anim = animation.FuncAnimation(fig, animate, fargs = (ln, ax, data_file),
                                frames=50, interval=20, blit=True)

    anim.save(file_name, fps=5 )

    plt.show()

if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description='Config to plot result ')
    parser.add_argument('--topology', '-t', required=True, 
                        type=str, help='ring or star')
    parser.add_argument('--problem', '-p', required=True, 
                        type=str, help='Name of problem')
    parser.add_argument('--popsize', '-s1', default = 32, 
                        type=int, help='Size of population ')
    parser.add_argument('--probsize', '-s2', default = 2, 
                        type=int, help='Size of population ')
    
    args = vars(parser.parse_args())
    main(args)

