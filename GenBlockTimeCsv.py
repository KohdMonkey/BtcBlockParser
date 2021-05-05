#! /bin/python3

import BtcHeaderDB

blkTimes = []
blkTimeDict = {}

with BtcHeaderDB.BtcHeaderDB('blockchain_headers') as db:
	with open('Blocktime.csv', 'w') as csvFile:
		csvFile.write('"block num","block time","block diff"\n')

		prevTime = 0
		idx = 0

		for header in db:
			if prevTime > 0:
				if header.timestamp < prevTime:
					# print(header.timestamp - prevTime)
					# print(idx)
					# print(header)
					# exit()
					blkTime = 0
				else:
					blkTime = header.timestamp - prevTime
				blkTimes.append(blkTime)
				csvFile.write('{},{},{}\n'.format(idx, blkTime, header.difficulty))

			prevTime = header.timestamp
			idx += 1

# with BtcHeaderDB.BtcHeaderDB('blockchain_headers') as db:
# 	prevTime = 0

# 	for header in db:
# 		if prevTime > 0:
# 			if header.timestamp < prevTime:
# 				print(idx)
# 			blkTime = header.timestamp - prevTime
# 			blkTimes.append(blkTime)

# 		prevTime = header.timestamp

for t in blkTimes:
	if t not in blkTimeDict:
		blkTimeDict[t] = 1
	else:
		blkTimeDict[t] += 1

with open('BlocktimeDist.csv', 'w') as csvFile:
	csvFile.write('"block time","count"\n')
	for t, count in sorted(blkTimeDict.items()):
		#print(t, count)
		csvFile.write('{},{}\n'.format(t, count))
