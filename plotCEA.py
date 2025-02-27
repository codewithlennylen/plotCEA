#!/usr/bin/env python
# -*-coding:utf-8-*-

import matplotlib.pyplot as plt
import pandas as pd
import sys
import pdb

gravity_acceleration = 9.80665

if len(sys.argv) != 2:
    print("Usage: python plotCEA.py <Your CEA output text file>")
    sys.exit()

filename = sys.argv[1]

file = open(filename).read()
outputs = file.split('THEORETICAL')
outputs = outputs[1:]
df = pd.DataFrame()
for output in outputs:
    dic = {}
    # pdb.set_trace()
    Pin = output.split('Pin =')[1].split('PSIA')[0].strip()
    O_F = output.split('O/F=')[1].split('%FUEL')[0].strip()
    Isp = output.split('Isp, M/SEC')[1].split('MASS')[0].strip().split(' ')[-1]
    dic['Pin'] = float(Pin)
    dic['O_F'] = float(O_F)
    dic['Isp'] = float(Isp)
    df1 = pd.DataFrame(dic, index=[0])
    df = pd.concat([df, df1], ignore_index=True)


Pins = list(df['Pin'].unique())

for Pin in Pins:
    # color = colors[cnt]
    val = df[df['Pin'] == Pin]
    O_Fs = sorted(list(set(val['O_F'])))
    df_tmp = pd.DataFrame()
    for O_F in O_Fs:
        tmp = val[val['O_F'] == O_F]
        tmp = tmp[tmp['Isp'] == max(tmp['Isp'])]
        df_tmp = pd.concat([df_tmp, tmp], ignore_index=True)

    plt.plot(df_tmp['O_F'], df_tmp['Isp']/gravity_acceleration)

plt.legend([str(Pin)+'(psia)' for Pin in Pins])
plt.xlabel('O/F ratio')
plt.ylabel('Isp [s]')
plt.title('Isp vs. O/F ratio')
plt.show()
