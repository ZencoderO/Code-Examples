# This makefile should build all the revelant @-graphs from a JSON file of tweets and store them in pkl files.
# It also creates some badly formatted statistics (in a file called graph_stats.txt)
# You will need to change the line below to point to the Label and Glove Path

Label=../data/ALLLabel.csv
GLOVE_PATH=../data/glove.twitter.27B.50d.txt

# Once you enter this line, the command to run (where the prompt is ">") is simply:

# > make

# To rerun, first type:

#> delete all the csv and output file.

all: train.csv output.txt

clean:
	rm train.csv output.txt
	
train.csv:
	python PreProcessing/SplitTheData.py ${Label}

output.txt: train.csv
	python 	Keras/Keras.py ${GLOVE_PATH} >> output.txt



