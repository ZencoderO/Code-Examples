import pickle
import numpy as np
import argparse
import pdb

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--Means", help="input file data")
    parser.add_argument("--Tests", help="output file data", default='const_transformed.json')
    args = parser.parse_args()
    return args

def graphize(columns, rows, array, factor=1.0,level=1.0):
    print "& \\textbf{" + ("} & \\textbf{".join(columns)) + "} \\\\"
    if level < .8:
	levels = []
        for r in rows:
	    for c in columns:
		levels.append(array[c][r])
        levels= sorted(levels)
	i = 0
	#pdb.set_trace()
	while levels[i] <= level/(factor-i):
	    #pdb.set_trace()
            i+=1

    for r in rows :
	row = []
	for c in columns:
        	entry = "%0.8f" %  array[c][r]
		if level < .8 and array[c][r] < levels[i]:
			entry = "\\textbf{" + entry + "}"
		row.append(entry)
        print r + " & " + (" & ".join(row)) + " \\\\"
	
    print ""

def main():

    args = parse_args()
    f = open(args.Means)
    means = pickle.load(f)
    f.close()
    f = open(args.Tests)
    tests = pickle.load(f)
    f.close()

    rows = ['POSEMO', 'NEGEMO', 'Openness', 'Agreeableness', 'Conscientiousness',  'Neuroticism',  'Extraversion']
    columns = ['R@-CH vs CH', 'H-CH vs CH', 'T-CH vs CH', 'RT-CH vs CH', 'R@ vs R@-H', "R@, RT, H, and CH ANOVA"]
    columns = ["R@-RT vs RT", "R@-H vs H", 'R@-CH vs CH', "NCH vs @-NCH-NH", "CH vs @-NCH-NH"]
    columns2 = ["R@, NCH, CH ANOVA", "R@, RT, H, and CH ANOVA"]
    #columns = ["R@, RT, H, and CH ANOVA"]
    graphize(columns, rows, means, 70.0, 0.05)
   
    graphize(columns2, rows, means, 70.0, 0.05) 
    # fix tests to pull out means
    tests = {x:{y:z[0] for y,z in w.items()} for x,w in tests.items()}

    graphize(['R@', 'RT', 'H',  'CH', 'NCH'], rows, tests)

if __name__ == '__main__':
    main()
