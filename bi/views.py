from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from datetime import datetime
from .models import Bi, TimeTable, DimenTable, MeasureTable, Colselect, Rowselect, Measureselect, FileSelect, Graphselect, Subgraph, Graphmeasure, Selectsub
from .model_2 import Model
from .create import Create
import csv, os, cgi
from os.path import basename
import json
import itertools 
import pandas as pd

m = Model()
def show(request):
    #Bi.objects.all().delete()
    FileSelect.objects.all().delete()
    Colselect.objects.all().delete()
    Rowselect.objects.all().delete()
    Measureselect.objects.all().delete()
    Graphselect.objects.all().delete()
    Selectsub.objects.all().delete()
    Graphmeasure.objects.all().delete()
    Subgraph.objects.all().delete()
    with open('bi/static/css/data.json', 'w') as f:
        f.write("")
    with open('bi/static/css/table.html', 'w') as f:
        f.write("")
    return render(request, 'bi/home.html', {'all_list':Bi.objects.order_by('file_name')})

def graph(request):
    #Bi.objects.all().delete()
    return render(request, 'bi/graph.html', {'all_time':TimeTable.objects.all(),
                   'all_dim':DimenTable.objects.all(),
                   'all_measure':MeasureTable.objects.all(), 
                   'all_select':Graphselect.objects.all(),
                   'sub_select':Selectsub.objects.all(),
                   'measure':Graphmeasure.objects.all(),
                   'all_sub':Subgraph.objects.all()})

def get_subgraph(request):
    Subgraph.objects.all().delete()
    data = request.GET.get('data')
    for i in FileSelect.objects.all().values_list('file_name', flat=True):
        m.select_file(i)
    if data in m.time:
        data = data + ':Year'
    array = [] 
    for i in m.get_data(data):
        record = Subgraph(sub_graph = i)
        record.save()
        array.append(i)
    return HttpResponse(json.dumps(array))

def subgraph_select(request):
    Selectsub.objects.all().delete()
    data = request.GET.getlist('data[]')
    for i in data:
        record = Selectsub(sub_select = i)
        record.save()
    return HttpResponseRedirect(reverse('bi:graph'))
def graph_select(request):
    data = request.GET.getlist('data[]')
    if data[0] != " ":
        Graphselect.objects.all().delete()
        record = Graphselect(graph = data[0])
        record.save()
    if data[1] != " ":
        Graphmeasure.objects.all().delete()
        record = Graphmeasure(measure_graph = data[1])
        record.save()
    showGraph()
    return HttpResponseRedirect(reverse('bi:graph'))

def showGraph():
    data = []
    df = pd.DataFrame({})
    dimen = ""
    for i in FileSelect.objects.all().values_list('file_name', flat=True):
        m.select_file(i)
    for i in Graphselect.objects.all().values_list('graph', flat=True):
        dimen = i
        if i in m.time:
            col = [i+':Year']
        else:
            col = [i]
    for i in Graphmeasure.objects.all().values_list('measure_graph', flat=True):
        row = ['Measurement']
        r = [[i]]
    c = [[]]
    for i in Selectsub.objects.all().values_list('sub_select', flat=True):
        if dimen in m.time:
            i = int(i)
        c[0].append(i)
    df['label'] = c[0]
    val = []
    if len(row)>0:
        m.keepC.append(m.df)
        for a in range(len(col)):
            m.keepC.append(None)
        for a in range(len(row)):
            m.keepR.append(None)
        sendC = list(itertools.product(*c))
        sendR = list(itertools.product(*r))
        for j in range(len(sendC)):
            m.get_col(col, sendC[j], m.keepC[0])
            for i in range(len(sendR)):
                val.append(m.get_row(row, sendR[i], m.keepR[0], 0))
        df['value'] = val
    out = df.to_json(orient = 'records')
    with open('bi/static/css/data.json', 'w') as f:
        f.write(out)
    

def delete_subgraph(request):
    record = Selectsub.objects.get(pk = int(request.GET.get('data')))
    record.delete()
    return HttpResponseRedirect(reverse('bi:graph'))

def import_file(request):
    if request.method == 'POST':
        try:
            if(str(request.FILES['file']).endswith('.xlsx')):
                filename = str(request.FILES['file'])
                filename = os.path.splitext(filename)[0]
                handle_uploaded_file(request.FILES['file'], filename)
                starschema(filename)
                record = Bi(file_name = filename)
                record.save()
            else:
                raise
        except:
            return render(request, 'bi/import.html',{'error_message':'Please Select xlsx file!!!'})
    return HttpResponseRedirect(reverse('bi:show'))

def pivot_page(request):
    return render(request, 'bi/pivot.html',
                  {'all_time':TimeTable.objects.all(),
                   'all_dim':DimenTable.objects.all(),
                   'all_measure':MeasureTable.objects.all(), 
                   'all_col':Colselect.objects.all(),
                   'measure':Measureselect.objects.all(),
                   'all_row':Rowselect.objects.all()})

def pivot_table(request, filename):
    '''FileSelect.objects.all().delete()
    Colselect.objects.all().delete()
    Rowselect.objects.all().delete()
    Measureselect.objects.all().delete()'''
    m.select_file(filename)
    record = FileSelect(file_name = filename)
    record.save()
    TimeTable.objects.all().delete()
    DimenTable.objects.all().delete()
    MeasureTable.objects.all().delete()
    for i in m.time:
        record = TimeTable(time = i)
        record.save()
    for i in m.dim:
        record = DimenTable(dimension = i)
        record.save()
    for i in m.measure:
        record = MeasureTable(measure = i)
        record.save()
    return HttpResponseRedirect(reverse('bi:pivot_page'))

def col_select(request):
    data = request.GET.getlist('data[]')
    for i in data:
        record = Colselect(column = i)
        record.save()
    return HttpResponseRedirect(reverse('bi:pivot_page'))
def row_select(request):
    data = request.GET.getlist('data[]')
    for i in data:
        record = Rowselect(row = i)
        record.save()
    return HttpResponseRedirect(reverse('bi:pivot_page'))
def measure_select(request):
    data = request.GET.get('data')
    if data != " ":
        Measureselect.objects.all().delete()
        record = Measureselect(measure = data)
        record.save()
    test()
    return HttpResponseRedirect(reverse('bi:pivot_page'))

def test():
    col = []
    row = []
    rows = []
    c = []
    r = []
    value = []
    measure = ""
    for i in FileSelect.objects.all().values_list('file_name', flat=True):
        filename = i
        m.select_file(filename)
    for i in Colselect.objects.all().values_list('column', flat=True):
        if i in m.time:
            i = i+":Year"
        col.append(i)
    for i in Rowselect.objects.all().values_list('row', flat=True):
        if i in m.time:
            i = i+":Year"
        row.append(i)
        rows.append(i)
    for i in Measureselect.objects.all().values_list('measure', flat=True):
        measure = i
    if measure != "":
        row.append("Measurement")
        value.append(measure)
    for i in range(len(col)):
        c.append([])
        for j in m.get_data(col[i]):
            c[i].append(j)
    for i in range(len(row)):
        r.append([])
        if row[i] == 'Measurement':
            r[i].append(measure)
        else:
            for j in m.get_data(row[i]):
                r[i].append(j)
    #print(row)
    df = pd.DataFrame({})
    get_col = []
    get_row = []
    get_value = []
    columns = []
    if len(value) > 0:
        m.keepC.append(m.df)
        for a in range(len(col)):
            get_col.append([])
            m.keepC.append(None)
        for a in range(len(row)):
            get_row.append([])
            m.keepR.append(None)
        sendC = list(itertools.product(*c))
        sendR = list(itertools.product(*r))
        for j in range(len(sendC)):
            m.get_col(col, sendC[j], m.keepC[0])
            for i in range(len(sendR)):
                val = m.get_row(row, sendR[i], m.keepR[0], 0)
                for k in range(len(col)):
                    get_col[k].append(sendC[j][k])
                for l in range(len(row)):
                    get_row[l].append(sendR[i][l])
                get_value.append(val)
                columns.append("Value")
        for i in range(len(col)):
            df[col[i]] = get_col[i]
        for i in range(len(row)):
            df[row[i]] = get_row[i]
        df['Value'] = get_value
        df['Column'] = columns
        if len(col) > 0:
            colu = col
        else:
            colu = ['Column']
        if len(row) > 1:
            index = rows
        else:
            index = ['Measurement']
        table = pd.pivot_table(df, values = 'Value',
                               index = index, columns = colu)
        with open("bi/static/css/table.html", 'w') as fo:
            fo.write(table.to_html())
               

def delete_col(request):
    record = Colselect.objects.get(pk = int(request.GET.get('data')))
    record.delete()
    return HttpResponseRedirect(reverse('bi:pivot_page'))
def delete_row(request):
    record = Rowselect.objects.get(pk = int(request.GET.get('data')))
    record.delete()
    return HttpResponseRedirect(reverse('bi:pivot_page'))

def handle_uploaded_file(file, filename):
    if not os.path.exists('upload/'):
        os.mkdir('upload/')
 
    with open('upload/' + filename+".xlsx", 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def starschema(filename):
    c = Create()
    c.import_file('./upload/'+filename+".xlsx")
    c.convert_data()
    c.manage_file()
    c.set_file()

