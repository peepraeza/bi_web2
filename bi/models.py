from django.db import models


class Bi(models.Model):
    file_name = models.CharField(max_length = 200)
class FileSelect(models.Model):
    file_name = models.CharField(max_length = 200)

class TimeTable(models.Model):
    time = models.CharField(max_length = 20)
    
class DimenTable(models.Model):
    dimension = models.CharField(max_length = 20)
    
class MeasureTable(models.Model):
    measure = models.CharField(max_length = 20)

class Colselect(models.Model):
    column = models.CharField(max_length = 20)

class Rowselect(models.Model):
    row = models.CharField(max_length = 20)

class Measureselect(models.Model):
    measure = models.CharField(max_length = 20)

class Graphselect(models.Model):
    graph = models.CharField(max_length = 20)

class Subgraph(models.Model):
    sub_graph = models.CharField(max_length = 20)

class Selectsub(models.Model):
    sub_select = models.CharField(max_length = 20)

class Graphmeasure(models.Model):
    measure_graph = models.CharField(max_length = 20)
