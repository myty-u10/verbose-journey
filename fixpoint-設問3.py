import pandas as pd


class Time(object):
    def __init__(self, time='00000000000000'):
        self.time = int(time)
        self.year = self.time // (10 ** 10)
        self.month = self.time % (10 ** 10) // (10 ** 8)
        self.date = self.time % (10 ** 8) // (10 ** 6)
        self.hour = self.time % (10 ** 6) // (10 ** 4)
        self.min = self.time % (10 ** 4) // (10 ** 2)
        self.sec = self.time % (10 ** 2)

    def __sub__(self, other):
        ans =Time()
        month31 = [1, 2, 4, 6, 8, 9, 11]
        month30 = [5, 7, 10, 12]

        ans.year = self.year - other.year
        ans.month = self.month - other.month
        ans.date = self.date - other.date
        ans.hour = self.hour - other.hour
        ans.min = self.min - other.min
        ans.sec = self.sec - other.sec

        while ans.sec < 0:
            ans.sec += 60
            ans.min -= 1

        while ans.min < 0:
            ans.min += 60
            ans.hour -= 1

        while ans.hour < 0:
            ans.hour += 24
            ans.date -= 1

        while ans.date < 0:
            if other.month in month31:
                date = 31
            elif other.month in month30:
                date = 30
            else:
                date = 28
            ans.date += date
            ans.month -= 1

        while ans.month < 0:
            ans.month += 12
            ans.year -= 1

        return ans
    
    def print_time(self):
        if self.year != 0:
            print(self.year,'年', end='')
        
        if self.month != 0:
            print(self.month,'カ月', end='')
        
        if self.date != 0:
            print(self.date,'日', end='')
        
        if self.hour != 0:
            print(self.hour,'時間', end='')
        
        if self.min != 0:
            print(self.min,'分', end='')
        
        if self.sec != 0:
            print(self.sec,'秒')

N = int(input('許容するタイムアウトの回数を入力してください ： '))  
num = int(input('平均をとる個数を入力してください : '))
T = int(input('閾値の時間を入力してください : '))       
print('###################################')

file = 'log_file.xlsx'
f = pd.read_excel(file)


info =[[],[],[]]

for i in range(f.shape[1]):
    for j in range(f.shape[0]):
        info[i].append(f.iat[j, i])

server_name = []
for k in info[1]:
    if k not in server_name:
        server_name.append(k)
        

server = []
for l in range(len(server_name)):
    server.append([])
    for m in range(f.shape[0]):
        if server_name[l] == f.iat[m, 1]:
            server[l].append([f.iat[m, 0], f.iat[m, 2]])

n = 0
time1 = []
time2 = []

t_sum = []
t_ave = []

for p in range(len(server)):
    time1.append(0)
    time2.append(0)
    for q in range (len(server[p])):
        if server[p][q][1] == '-':
            if n == 0:
                time1[p] = server[p][q][0]
            time2[p] = server[p][q][0]
            n += 1
            
        else:
            n = 0
    
    if n > N:
        c = Time(time2[p]) - Time(time1[p])
        print('エラーが起きているサーバー：', server_name[p], end='   ')
        print('故障期間：', end='' )
        c.print_time()
        print()

print('###################################')

for r in range(len(server)):
    t_sum.append([])
    t_ave.append([])
    for s in range (len(server[r])):
        t_ave[r].append(0)
        t_sum[r].append(0)
        
        if server[r][s][1] == '-':
            o = 0
        
        else:            
            o += 1
             
        if o >= num:
            for t in range(q, q-num, -1):
                t_sum[r][s] += server[r][t][0]
                t_ave[r][s] = t_sum[r][s] / num

for u in range(len(server)):
    for v in range(len(server[u])-1):            
        if (t_ave[u][v] > T) & (t_ave[u][v+1] < T):
            w = v
            
            time_a = server[u][v][0]
            while t_ave[u][w] > T:
                time_b = server[u][w- num+1][0]
                w -= 1
                
                
            d = Time(time_a) - Time(time_b)
            print('過負荷が起きているサーバー：', server_name[u], end='   ')
            print('故障期間：', end='' )
            d.print_time()
            print()
            
    v = len(server[u]) - 1            
    if t_ave[u][v] > T:
        w = v
            
        time_a = server[u][v][0]
        while t_ave[u][w] > T:
            w -= 1
            time_b = server[u][w][0]
            
                
                
        e = Time(time_a) - Time(time_b)
        print('過負荷が起きているサーバー：', server_name[u], end='   ')
        print('故障期間：', end='' )
        e.print_time()
        print()


