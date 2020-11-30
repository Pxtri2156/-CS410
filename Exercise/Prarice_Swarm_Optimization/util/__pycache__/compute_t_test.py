from scipy import stats
import json
def main():
    t_test = {
        'Rastrigin':[],
        "Rosenbrock": []
    }

    prop_sizes = [128, 256, 512, 1024, 2048]
    for problem in ['Rastrigin', 'Rosenbrock']:
        for size in prop_sizes:
            path_file = "./Experimental_result/" + problem + '_' + "ring" + '_' + str(size) + "_10.json"
            data_1 = json.load(open(path_file,"r"))

            path_file = "./Experimental_result/" + problem + '_' + "star" + '_' + str(size) + "_10.json"
            data_2 = json.load(open(path_file,"r"))

            best_val_ring = [data_1[i]["val_best_solution"]  for i in range(10)]
            best_val_star = [data_2[i]["val_best_solution"]  for i in range(10)]

            stats.ttest_ind(best_val_ring,best_val_star))
            t_test[problem].append(stats.ttest_ind(best_val_ring,best_val_star))

    t_test_file = open("./Experimental_result/t_test.json", 'w')
    
    # data = json.dumps(t_test_file, indent=4)
    # json.dump(data,data)


if __name__ == "__main__":
    main()