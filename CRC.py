import random


# Creates the data to be transmitted
def random_generator(a, b, k):
    data = []

    for i in range(0, k):
        rand = random.random()+0.1

        if rand < 0.6:
            data.append(a)
        else:
            data.append(b)

    return data


# Singe bit error generator
def error_generator(bit, bit_error_rate):
    rand = random.randrange(0, 1000)

    if rand == bit_error_rate*1000:
        if bit == 1:
            return 0
        else:
            return 1
    else:
        return bit


def xor(b1, b2):
    result = []

    for i in range(len(b1)):
        result.append(int(b1[i]) ^ int(b2[i]))  # xor bit by bit

    return result


def division(data, fcs, f, p):
    # appending L-1 0 to the original message
    for bit in data:
        f.append(bit)

    for i in range(0, (len(p)-1)):
        f.append(0)

    # creating array which stores the starting division data
    for i in range(0, len(p)):
        fcs.append(data[i])

    # performing binary division
    for i in range(len(p), len(f)):
        if fcs[0] != 0:
            fcs = xor(fcs, p)

        fcs.remove(0)
        fcs.append(f[i])

    if fcs[0] != 0:
        fcs = xor(fcs, p)

    fcs.remove(0)

    return fcs


BER = 0.001  # bit error rate
should_be_received = []  # stores the receiver binary division which should result in 0
fcs = []  # is used to find the transmitted FCS
f = []  # is used to store the data + CRC(FCS)
p = input("\nType the P value: ")  # polynomial used is given by the user
k = 20  # how many bits will be transmitted
cought_errors_count = 0  # errors cought from CRC
uncought_errors_count = 0  # uncought errors from CRC
num_of_messages = 1000000  # number of messages

for i in range(0, len(p)-1):
    should_be_received.append(0)

for i in range(0, num_of_messages):
    data = random_generator(1, 0, k)
    should_be_transmitted = []  # original message
    transmitted = []  # message over channel with BER 0.001

    for binary in data:
        transmitted.append(error_generator(binary, BER))
        should_be_transmitted.append(binary)

    fcs = division(data, fcs, f, p)

    for binary in fcs:
        transmitted.append(binary)
        should_be_transmitted.append(binary)

    # reseting the arrays
    fcs = []
    f = []

    to_be_received = division(transmitted, fcs, f, p)

    while(1):
        if transmitted != should_be_transmitted and to_be_received != should_be_received:
            cought_errors_count += 1
            transmitted.clear()

            for binary in should_be_transmitted:
                transmitted.append(error_generator(binary, BER))
        elif transmitted != should_be_transmitted and to_be_received == should_be_received:
            uncought_errors_count += 1
            break
        else:
            break
        # reseting the arrays
        fcs = []
        f = []

        to_be_received = division(transmitted, fcs, f, p)

    # reseting the arrays
    fcs = []
    f = []

print("Total messages: ", num_of_messages)

print("Messages checked by CRC: ", cought_errors_count+uncought_errors_count)

print("Errors found by CRC: ", cought_errors_count)

print("Errors not found by CRC: ", uncought_errors_count)

print("Messages checked by CRC over total messages: ",
      ((cought_errors_count+uncought_errors_count)/num_of_messages)*100, "%")

print("Errors found by CRC over messages checked by CRC: ",
      (cought_errors_count/(cought_errors_count+uncought_errors_count))*100, "%")

print("Errors not found by CRC over messages checked by CRC: ",
      (uncought_errors_count/(cought_errors_count+uncought_errors_count))*100, "%")
