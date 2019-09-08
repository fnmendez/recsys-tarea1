fo = open("training_set.csv", "r+")
fw = open("new_training_set.csv", "w+")

fo.readline()
for line in fo.readlines():
    line = line.strip().split(",")
    line[1] = line[1][:-2]
    line[2] = line[2][:-2]
    line[3] = line[3][:-2]
    new_line = line[1] + "," +line[2] + "," +line[3] + "\n"
    fw.writelines(new_line)

fo.close()
fw.close()
