import csv
# this program was used to fill our movieList for autocomplete
with open('movies.csv', 'r') as csv_file: # movies.csv not included in our github
    csv_reader = csv.DictReader(csv_file)
    for line in csv_reader:
        if (line['domgross_2013$'] != '#N/A'):
            if (int(line['domgross_2013$']) > 100000000): #only want movies that were popular to save search time
                print("\""+line['title']+" ("+line['year']+")\",")
