import pandas as pd
import os
import datetime

class Model:
    def __init__(self):
        self.key = {}  # key for dict
        self.dim = []  # keep dimension 
        self.time = []  # keep time dimension
        self.measure = []  # keep measurement
        self.checkC = []  # check old value of column
        self.checkR = []  # check old value of row
        self.keepC = []  # keep dataframe of column
        self.keepR = []  # keep dataframe of row
        self.quarter = ['Q1', 'Q2', 'Q3', 'Q4']
        self.month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    ##################### create dict for search data #######################
    def set_dict(self):

        for dim in self.time:
            data = pd.read_csv('./data/' + self.open_file + '/' + dim + '.csv')
            df = pd.DataFrame({})
            df['Year'] = data['Year'].values.tolist()
            df['Quarter'] = data['Quarter'].values.tolist()
            df['Month'] = data['Month'].values.tolist()
            df['Key'] = data['Key'].values.tolist()
            self.key[dim] = df

        for dim in self.dim:
            data = pd.read_csv('./data/' + self.open_file + '/' + dim + '.csv')
            df = pd.DataFrame({})
            df[dim] = data[dim].values.tolist()
            df['Key'] = data['Key'].values.tolist()
            self.key[dim] = df
              
    ################ select file to run program #############
    def select_file(self, open_file): 
        # set empty to keep data
        self.dim = []
        self.time = []
        self.measure = []
        self.open_file = open_file
        self.path = './data/' + open_file + '/'
        fact = pd.read_csv(self.path + 'fact.csv')

        # read file
        with open(self.path + 'file.txt') as read:
            for line in read:
                k, v = line.strip().split(':')
                val = v.strip().split(',')
                for i in val:
                    if i != '':
                        if k == 'time':
                            self.time.append(i)
                        elif k == 'dimension':
                            self.dim.append(i)
                        elif k == 'measure':
                            self.measure.append(i)
 
        # keep data 
        self.df = pd.DataFrame({})
        for i in self.time:
            self.df[i] = fact[i].values.tolist()
        for i in self.dim:
            self.df[i] = fact[i].values.tolist()
        for i in self.measure:
            self.df[i] = fact[i].values.tolist()
        self.set_dict()

    ############### get value for column in pivot table ###########
    def get_col(self, col, c, df_col):
        if len(self.checkC) < len(col):
            self.checkC = [None] * len(col)
        for i in range(len(col)):
            val = col[i].strip().split(':')
            if self.checkC[i] != c[i]:
                df_col = self.keepC[i]
                if val[0] in self.time:
                    if val[1] == 'Quarter':
                        num = c[i]
                        self.temp = (num - 1) * 3
                    elif val[1] == 'Month':
                        num = c[i] + self.temp
                    else:
                        num = c[i] 
                    df_col = df_col[df_col[val[0]].isin(self.get_key(val, num))]
                    self.keepC.insert(i + 1, df_col)
                    self.checkC[i] = c[i]
                else:
                    df_col = df_col[df_col[val[0]].isin(self.get_key(val, c[i]))]
                    self.keepC.insert(i + 1, df_col)
                    self.checkC[i] = c[i]
        self.keepR.insert(0, self.keepC[len(col)])

    ############ get value for row in pivot table ###########
    def get_row(self, row, r, df_row, measure):
        value = 0
        if len(self.checkR) < len(row):
            self.checkR = [None] * len(row)
        for i in range(len(row)):
            val = row[i].strip().split(':')
            if val[0] == 'Measurement':
                df_row = self.keepR[len(row)-1]
                if measure == 0:
                    value = df_row[r[i]].sum()
                elif measure == 1:
                    value = df_row[r[i]].mean()
                elif measure == 2:
                    value = df_row[r[i]].max()
                elif measure == 3:
                    value = df_row[r[i]].min()
            elif self.checkR[i] != r[i]:
                df_row = self.keepR[i]
                if val[0] in self.time:
                    if val[1] == 'Quarter':
                        num = r[i]
                        self.temp = (num - 1) * 3
                    elif val[1] == 'Month':
                        num = r[i] + self.temp
                    else:
                        num = r[i]
                    
                    df_row = df_row[df_row[val[0]].isin(self.get_key(val, num))]
                    self.keepR.insert(i + 1, df_row)
                    self.checkR[i] = r[i]
                else:
                    df_row = df_row[df_row[val[0]].isin(self.get_key(val, r[i]))]  
                    self.keepR.insert(i + 1, df_row) 
                    self.checkR[i] = r[i]    
        return value

    ############## get key of dimension (star schema) ##################
    def get_key(self, dim, val):
        df_key = self.key[dim[0]]
        data = [val]
        if dim[0] in self.time:
            df_key = df_key[df_key[dim[1]].isin(data)]
        else:
            df_key = df_key[df_key[dim[0]].isin(data)]
        return df_key['Key'].values.tolist()

    ############## get data ################
    def get_data(self, dim):
        dim = dim.strip().split(':')
        read = pd.read_csv('./data/' + self.open_file + '/' + dim[0] + '.csv')
        if dim[0] in self.time:
            if dim[1] == 'Month':
                data = [1, 2, 3]
            else:
                data = set(read[dim[1]].values.tolist())
        else:
            data = set(read[dim[0]].values.tolist())
        return sorted(data)
   
