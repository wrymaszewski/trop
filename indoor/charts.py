from .models import Training, Top
from routes.models import Ascent
from charts.charts import pie, line, verbose_style, verbose_months
from django.db.models import Count
from django.db.models.functions import TruncMonth
from chartit import PivotChart, PivotDataPool

def training_style_pie_chart(args):
    return pie(
            queryset = (Top.objects
                        .filter(training__pk = args)
                        .values('ascent_style')
                        .order_by()
                        .annotate(Count=Count('ascent_style'))),
            terms = ['ascent_style', 'Count'],
            title = 'Styles of Ascent',
            verbose = verbose_style
    )

def training_grade_pie_chart(args):
    return pie(
            queryset = (Top.objects
                        .filter(training__pk = args)
                        .values('grade_fr')
                        .order_by()
                        .annotate(Count = Count('grade_fr'))),
            terms = ['grade_fr', 'Count'],
            title = 'Number of Ascents'
    )

def gym_pie_chart(args):
    return pie(
            queryset = (Training.objects
                        .filter(user__username = args)
                        .values('location__name')
                        .order_by()
                        .annotate(Count=Count('location__name'))),
            terms = ['location__name', 'Count'],
            title = 'Gyms'
    )

def training_line_chart(args):
    data = PivotDataPool(
           series=
            [{  'options': {
                'source': (Top.objects
                           .filter(training__user__username__iexact = args)
                           .values('training__date', 'grade_fr')
                           .order_by('grade_fr')
                           .order_by('training__date')),

                'categories': 'training__date',
                'legend_by': 'grade_fr'
            },
              'terms': {
                'Count': Count('grade_fr')
              }
            }],
    )

    cht = PivotChart(
            datasource = data,
            series_options=[
                {'options': {
                   'type': 'line',
                   'stacking': False,
                   'xAxis': 0,
                   'yAxis': 0},
                 'terms': ['Count']}],
            chart_options =
              {'title': {
                   'text': 'Number of Tops'},
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
