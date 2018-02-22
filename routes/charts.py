from .models import Ascent, Route, Sector
from django.db.models import Count
from django.db.models.functions import TruncMonth
from charts.charts import verbose_style, verbose_months, pie, line
from chartit import PivotChart, PivotDataPool

# Charts routes
def route_pie_chart(args):
    return pie(
        queryset = (Route.objects
                    .filter(sector__slug__iexact = args)
                    .values('grade')
                    .order_by()
                    .annotate(Count = Count('grade'))),
        terms = ['grade', 'Count'],
        title = 'Number of Routes'
    )

def route_ascent_chart(args):
    return line(
        queryset = (Ascent.objects
                    .filter(route__slug__iexact = args)
                    .annotate(date_trunc=TruncMonth('date'))
                    .values('date_trunc')
                    .order_by()
                    .annotate(Count = Count('date_trunc'))),
        terms = ['date_trunc', 'Count'],
        title = 'Number of Ascents',
        axes = ['Date', 'Ascents'],
        verbose = verbose_months
    )

def ascent_pie_chart(args):
    return pie(
        queryset = (Ascent.objects
                    .filter(route__slug__iexact = args)
                    .values('ascent_style')
                    .order_by()
                    .annotate(Count=Count('ascent_style'))),
        terms = ['ascent_style', 'Count'],
        title = 'Style of Ascent',
        verbose = verbose_style
    )

def user_ascent_pie_chart(args):
    return pie(
                queryset = (Ascent.objects
                            .filter(user__username__iexact = args)
                            .values('ascent_style')
                            .order_by()
                            .annotate(Count=Count('ascent_style'))),
                terms = ['ascent_style', 'Count'],
                title = 'Styles of Ascent',
                verbose = verbose_style
    )

def user_ascent_chart(args):
    data = PivotDataPool(
           series=
            [{'options': {
               'source':  (Ascent.objects
                            .filter(user__username__iexact = args)
                            .annotate(date_trunc=TruncMonth('date'))
                            .values('date_trunc', 'route__grade_converted')
                            .order_by('route__grade_converted')
                            .order_by('date_trunc')),
                'categories': 'date_trunc',
                'legend_by': 'route__grade_converted'
            },
              'terms': {
                'count': Count('route__grade_converted')
              }
            }],
            sortf_mapf_mts=(None, verbose_months, False)
    )

    cht = PivotChart(
            datasource = data,
            series_options=[
                {'options': {
                   'type': '',
                   'stacking': False,
                   'xAxis': 0,
                   'yAxis': 0},
                 'terms': ['count']}],
            chart_options =
              {'title': {
                   'text': 'Number of Ascents'},
              'xAxis': {
                  'title': {
                      'text': 'Date'
                  }
              },
              'yAxis': {
                  'title': {
                      'text': 'Ascents'
                  }
              }
             }
    )

    return cht
