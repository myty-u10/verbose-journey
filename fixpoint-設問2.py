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
