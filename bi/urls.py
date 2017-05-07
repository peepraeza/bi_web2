from django.conf.urls import url

from . import views

app_name = 'bi'
urlpatterns = [
    url(r'^$', views.show, name='show'),
    url(r'^submit$', views.import_file, name='import_file'),
    url(r'^graph/$', views.graph, name='graph'),
    url(r'^graph/getsub$', views.get_subgraph, name='get_subgraph'),
    url(r'^graph/gselect$', views.graph_select, name='graph_select'),
    url(r'^graph/sgselect$', views.subgraph_select, name='subgraph_select'),
    url(r'^pivot/deleteg$', views.delete_subgraph, name='delete_subgraph'),
    url(r'^pivot/$', views.pivot_page, name='pivot_page'),
    url(r'^pivot/(?P<filename>[-\ \w]+)/$', views.pivot_table, name='pivot_table'),
    url(r'^pivot/cselect$', views.col_select, name='col_select'),
    url(r'^pivot/rselect$', views.row_select, name='row_select'),
    url(r'^pivot/mselect$', views.measure_select, name='measure_select'),
    url(r'^pivot/deletec$', views.delete_col, name='delete_col'),
    url(r'^pivot/deleter$', views.delete_row, name='delete_row'),
] 
