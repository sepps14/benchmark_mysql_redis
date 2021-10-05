import os
os.environ['QT_MAC_WAnTS_LAYER'] = '1'

import matplotlib.pyplot as plt
import numpy as np

m_insert_f = 'mysql_insert_times.txt'
r_insert_f = 'redis_insert_times.txt'
m_increment_f = 'mysql_increment_times.txt'
r_increment_f = 'redis_increment_times.txt'


mysql_insert_times = []
mysql_increment_times = []
redis_insert_times = []
redis_increment_times = []

with open(m_insert_f, 'r') as m_f, open(r_insert_f, 'r') as r_f:
    for m_line, r_line in zip(m_f, r_f):
        mysql_insert_times.append(float(m_line))
        redis_insert_times.append(float(r_line))

with open(m_increment_f, 'r') as m_f, open(r_increment_f, 'r') as r_f:
    for m_line, r_line in zip(m_f, r_f):
        mysql_increment_times.append(float(m_line))
        redis_increment_times.append(float(r_line))

mysql_insert_times = np.array(mysql_insert_times)
redis_insert_times = np.array(redis_insert_times)

mysql_increment_times = np.array(mysql_increment_times)
redis_increment_times = np.array(redis_increment_times)

print(f'mysql insert 50th percentile    = {np.percentile(mysql_insert_times, 50)}')
print(f'redis insert 50th percentile    = {np.percentile(redis_insert_times, 50)}')
print(f'mysql increment 50th percentile = {np.percentile(mysql_increment_times, 50)}')
print(f'redis increment 50th percentile = {np.percentile(redis_increment_times, 50)}')

def plot(series_pair, labels, fig_name):
    (s1, s2) = series_pair
    (l1, l2) = labels
    s1_p_99 = np.percentile(s1, 99)
    s1_p_1 = np.percentile(s1, 1)
    s1_bins = np.linspace(s1_p_1, s1_p_99, 100)

    s2_p_99 = np.percentile(s2, 99)
    s2_p_1 = np.percentile(s2, 1)
    s2_bins = np.linspace(s2_p_1, s2_p_99, 100)

    plt.hist(s1, s1_bins, edgecolor='blue', fill=False, label=l1)
    plt.axvline(s1_p_1, color='blue', linestyle='dashed')
    plt.axvline(s1_p_99, color='blue', linestyle='dashed')
    plt.hist(s2, s2_bins, edgecolor='red', fill=False, label=l2)
    plt.axvline(s2_p_99, color='red', linestyle='dashed')
    plt.axvline(s2_p_1, color='red', linestyle='dashed')
    plt.legend(loc="upper right")
    plt.xlabel('time (s)')
    plt.savefig(fig_name)
    plt.cla()

plot([mysql_insert_times, redis_insert_times], ['mysql', 'redis'], 'redis_v_mysql_insert_time.png')
plot([mysql_increment_times, redis_increment_times], ['mysql', 'redis'], 'redis_v_mysql_increment_time.png')