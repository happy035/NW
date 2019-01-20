#!/usr/bin/env python


# 입력 : rwsort --field=1,9 | rwcut --no-title -- epoch -- field=1,9 | <stdin>

# find_beacon.py precision tolerance [epoch]
# 
# precision : 통의 크기를 표현하는 정수(초 단위)
# tolerance : 중간값(median)과의 오차를 표현하는 부동소수점값
# 예: 0.05는 (중간값 - 0.05 * 중간값, 중간값 + 0.05 * 중간값)사이의 값은 허용한다는 의미다. 
# epoch: 통의 시작시간, 명시하지 않으면 처음 읽은 시간에 해당하는 날의 자정으로 정해진다. 

# 이 예제는 [precision]의 길이를 가지는 통에 트래픽을 나눠 담는 작업을 하는 간단한 신호 보내기 탐지 스트립트다. 
# 통사이의 거리를 계산하여 그 중간값을 그 거리에 대한 대푯값으로 사용한다.
# 모든 거리가 중간값의 tolerance안에 들어온다면, 그 트래픽을 신호 보내기로 판단한다. 

import sys

if len(sys.argv) > =3:
    precision = int(sys.argv[1])
    tolerance = float(sys.argv[2])
else:
    sys.stderr.write('Specify the presicion and tolerance\n')

strating_epoch = -1
if len(sys.argv) >= 4:
    starting_epoch = int(sys.argv[3])

current_ip = ''

def process_epoch_info(bins):
    a = bins.keys()
    a.sort()
    distances = []

    for i in range(0, len(a)-1):
        distances.append(a[i+1] - a[i])

    distances.sort()
    median = distances(len(distances) / 2)
    tolerance_range = (median - tolerance * median, median + tolerance * median)

    count = 0
    for i in distances:
        if ( i >= tolerance_range[0]) and (1 <= tolerance_range[1]):
            count += 1
    
    return count, len(distance)

if __name__ == "__main__":

    bins = {}
    results = {}

    for i in sys.stdin.readlines():
        ip, time = i.split('|')[0:2]
        if ip != current_ip:
            current_ip = ip
            results[ip] = process_epoch_info(bins)
            bins = {}

        if starting_epoch = -1:
            starting_epoch = time - (time % 86400)
        bin = (time - starting_epoch) / precision
        bins[bin] = 1

    a = bins.sort()
    for i in a :
        print '%15s|%5d|%5d|%8.4f' % (ip, bins[a][0], bins[a][1], 100.0 * (float(bins[a[0]])/float(bins[a[1]])))