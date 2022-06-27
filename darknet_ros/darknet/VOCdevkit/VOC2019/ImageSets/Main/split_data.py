import random

all = 101
imageDir = "/home/xz/car/src/darknet_ros/darknet/VOCdevkit/VOC2019/JPEGImages/"
numList = list(range(1, all))
random.shuffle(numList)

print(numList)
trainfile = open('./train.txt', 'w')
testfile = open('./test.txt', 'w')
abstrainfile = open('./2019_train.txt', 'w')
abstestfile = open('./2019_test.txt', 'w')

for train in range(1,81):
    trainfile.write(str(numList[train-1])+'\n')
    abstrainfile.write(imageDir + str(numList[train-1]) + '.jpg' + '\n')
trainfile.close()

for test in range(81, all):
    testfile.write(str(numList[test-1])+'\n')
    abstestfile.write(imageDir + str(numList[test-1]) + '.jpg' + '\n')
testfile.close()

