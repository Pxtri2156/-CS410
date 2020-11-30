import numpy as np 
import json

def main():
    prop_sizes = [128, 256, 512, 1024, 2048]
    topologys = ['ring', 'star']
    problems = ['Rastrigin', 'Rosenbrock']
    result = {
        "Rastrigin": {
            "ring": {
                "128": {},
                "256": {},
                "512": {},
                "1024": {},
                "2048": {}
            },
            "star": {
                "128": {},
                "256": {},
                "512": {},
                "1024": {},
                "2048": {}
            }
        },
        "Rosenbrock":{
            'ring':{
                "128": {},
                "256": {},
                "512": {},
                "1024": {},
                "2048": {}            },
            'star':{
                "128": {},
                "256": {},
                "512": {},
                "1024": {},
                "2048": {}            }
        }
    }
    for problem in problems:
        for topology in topologys:
            for size in prop_sizes:
                path_file = "./Experimental_result/" + problem + '_' + topology + '_' + str(size) + "_10.json"
                data = json.load(open(path_file,"r"))
                result[problem][topology][str(size)]['best_solution_mean'] \
                    = np.mean(np.array([data[i]["best_solution"]  for i in range(10)]), 0 ).tolist()
                
                result[problem][topology][str(size)]['best_solution_std'] \
                    = np.std(np.array([data[i]["best_solution"]  for i in range(10)]), 0 ).tolist()

                result[problem][topology][str(size)]['val_best_solution_mean'] \
                    = np.mean(np.array([data[i]["val_best_solution"]  for i in range(10)]), 0).tolist()

                result[problem][topology][str(size)]['val_best_solution_std'] \
                    = np.std(np.array([data[i]["val_best_solution"]  for i in range(10)]), 0).tolist()

                result[problem][topology][str(size)]['dis_true_global_mean'] \
                    = np.mean(np.array([data[i]["dis_true_global"]  for i in range(10)]), 0).tolist()
                
                result[problem][topology][str(size)]['dis_true_global_std'] \
                    = np.std(np.array([data[i]["dis_true_global"]  for i in range(10)]), 0).tolist()

    mean_file = open("./Experimental_result/mean.json", 'w')
    
    data = json.dumps(result, indent=4)
    json.dump(data,mean_file)
    for size in prop_sizes:
        print(' {} & {} \pm {} & {} \pm {} & {} \pm {} & {} \pm {} \\'.format(size, \
        round(result['Rastrigin']['ring'][str(size)]["val_best_solution_mean"], 4), \
        round(result['Rastrigin']['ring'][str(size)]["val_best_solution_std"], 4),  \
        round(result['Rastrigin']['star'][str(size)]["val_best_solution_mean"], 4), \
        round(result['Rastrigin']['star'][str(size)]["val_best_solution_std"], 4),  \
        round(result['Rosenbrock']['ring'][str(size)]["val_best_solution_mean"], 4), \
        round(result['Rosenbrock']['ring'][str(size)]["val_best_solution_std"], 4),  \
        round(result['Rosenbrock']['star'][str(size)]["val_best_solution_mean"], 4), \
        round(result['Rosenbrock']['star'][str(size)]["val_best_solution_std"], 4),  \
            ))
    
    
if __name__ == "__main__":
    main()