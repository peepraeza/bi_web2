import pandas as pd
import datetime
import csv
import os
from os.path import basename

class Create:
    def __init__(self):
        self.head = []  # keep header
        self.time = []  # keep time dimension
        self.dimension = []  # keep dimension
        self.measure = []  # keep measurement
        self.len_key = 1000  # first key

    ############################ import file ###################################
    def import_file(self, file_name):
        print(file_name)
        xl = pd.ExcelFile(file_name)
        basename = os.path.splitext(file_name)
        basename = basename[0].strip().split('/')

        if len(basename) > 1:
            self.basename = basename[len(basename) - 1]
        self.path = './data/' + self.basename + '/'

        if not os.path.exists(self.path):
            os.makedirs(self.path)
        df = xl.parse(xl.sheet_names[0])
        self.data = pd.read_excel(file_name, xl.sheet_names[0])

        for i in df.columns:
            self.head.append(i)
    
    ################## convert data and clasify data ###########################
    def convert_data(self):
        for i in self.head:
            self.convert_data_dimension(i)
            self.convert_data_time(i)
            self.convert_data_measure(i)

    # convert dimension
    def convert_data_dimension(self, i):
        zipcode = ["zip", "code", "postal"]
        data = self.data[i].values.tolist()
        if("id" in i.lower()): # Dimension ID 
            self.dimension.append(i) 
        elif(type(data[0]) == int):
            if(any(x in i.lower() for x in zipcode)): # Dimension zipcode
                self.dimension.append(i)
        elif(type(data[0]) == str):
            self.dimension.append(i) # Dimension others
        #return self.dimension

    # convert dimension time
    def convert_data_time(self, i):
        data = self.data[i].values.tolist()
        if(type(data[0]) == int):
            if(len(str(data[0])) > 13): # Dimension time
                self.time.append(i)
        #return self.time

    # convert measure
    def convert_data_measure(self, i):
        zipcode = ["zip", "code", "postal"]
        data = self.data[i].values.tolist()
        if(type(data[0]) == int and not("id" in i.lower())):
            if(not(len(str(data[0])) > 13) and
               not(any(x in i.lower() for x in zipcode))):
                self.measure.append(i) # Measure quantity
        if(type(data[0]) == float):
            self.measure.append(i) # Measure other
        #return self.measure
    
    ################# create dimension file ####################################            
    def manage_file(self):
        for t in range(len(self.time)):
            key = (t + 1) * self.len_key
            time = pd.to_datetime(self.data[self.time[t]].values.tolist())
            dim_time = []
            df = pd.DataFrame({'Year': time.year,
                               'Quarter': time.quarter,
                               'Month': time.month})
            group = df.groupby(['Year', 'Quarter', 'Month'])

            for k, val in group:
                dim_time.append([key, k[0], k[1], k[2]])
                key = key + 1

            with open(self.path + self.time[t] + '.csv', 'w') as outcsv:
                names = ['Key','Year','Quarter','Month']
                writer = csv.DictWriter(outcsv, fieldnames = names)
                writer.writeheader()
                a = csv.writer(outcsv, delimiter = ',')
                a.writerows(dim_time)
        
        for i in range(len(self.dimension)):
            key = (i + len(self.time) + 1) * self.len_key
            data = self.data[self.dimension[i]].values.tolist()
            dim = []
            df = pd.DataFrame({self.dimension[i]: data})
            group = df.groupby([self.dimension[i]])
            for k, val in group:
                dim.append([key, k])
                key = key + 1
            with open(self.path + self.dimension[i] + '.csv', 'w') as outcsv:
                writer = csv.DictWriter(outcsv, fieldnames = ['Key', self.dimension[i]])
                writer.writeheader()
                a = csv.writer(outcsv, delimiter = ',')
                a.writerows(dim)
        self.create_fact()

    #################### create fact file ######################################
    def create_fact(self):
        key = []
        measure = []

        # fact of time dimension
        for i in range(len(self.time)):
            key.append([])
            data = pd.read_csv(self.path + self.time[i] + '.csv').values.tolist()
            time = pd.to_datetime(self.data[self.time[i]].values.tolist())
            for j in range(len(time)):
                for k in range(len(data)):
                    if(time[j].year == int(data[k][1]) and
                       time[j].quarter == int(data[k][2]) and
                       time[j].month == int(data[k][3])):
                        key[i].append(data[k][0])
                        break

        # fact of dimension
        for i in range(len(self.dimension)):
            key.append([])
            data = pd.read_csv(self.path + self.dimension[i] + '.csv').values.tolist()
            val = self.data[self.dimension[i]].values.tolist()
            for j in range(len(val)):
                for k in range(len(data)):
                    if(val[j] == data[k][1]):
                        key[i + len(self.time)].append(data[k][0])
                        break

        # fact of measurement
        df = pd.DataFrame({})
        total = []
        dim_head = []
        for i in range(len(self.time)):
            total.append(self.time[i])
            dim_head.append(self.time[i])
            df[self.time[i]] = key[i]
        for i in range(len(self.dimension)):
            total.append(self.dimension[i])
            dim_head.append(self.dimension[i])
            df[self.dimension[i]] = key[i + len(self.time)]
        for i in self.measure:
            total.append(i)
            df[i] = self.data[i].values.tolist()
        
        df_ordered = df[total]                          
        df = df_ordered.sort_values(dim_head)
        df.to_csv(self.path + 'fact.csv', index = False)

    ################### keep file name #########################################
    def set_file(self):
        with open(self.path + 'file.txt', 'w') as f:
            f.write('time:')
            for i in self.time:
                f.write(i + ',')
            f.write('\n')
            f.write('dimension:')
            for i in self.dimension:
                f.write(i + ',')
            f.write('\n')
            f.write('measure:')
            for i in self.measure:
                f.write(i + ',')
        '''with open('open_file.txt', 'r') as f:
            file_name = f.read().strip().split(',')
        if self.basename not in file_name:
            with open('open_file.txt', 'a') as f:
                f.write(self.basename + ',')'''
        return self.basename
        
