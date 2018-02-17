from .models import Training, Top
from routes.models import Ascent
from routes.scales import convert_scale
from chartit import Chart, DataPool, PivotDataPool, PivotChart
from django.db.models import Count, Sum, Func
from django.db.models.functions import ExtractMonth, TruncDate, TruncMonth, TruncYear
from django.db.models import DateField

def verbose_months(date_trunc):
    names = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun',
         '07': 'Jul', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
    date_trunc = str(date_trunc)
    # for pivotchart
    if len(date_trunc) > 11:
        date_trunc = date_trunc.split("'")[1].split('-')[0:2]
        return [names[date_trunc[1]], date_trunc[0]]
    # for normal chart
    else:
        date_trunc = str(date_trunc).split('-')[0:2]
        joined =  ':'.join([names[date_trunc[1]], date_trunc[0]])
        return joined

def verbose_style(ascent_style):
    return dict(Ascent.ASCENT_STYLE_CHOICES)[ascent_style]


# Charts
def training_style_pie_chart(self, **kwargs):
    qs = Top.objects.filter(training__pk = self.kwargs.get('pk'))
    data = DataPool(
           series=
            [{'options': {
               'source': qs.values('ascent_style').order_by().annotate(Count=Count('ascent_style'))
               },
              'terms': [
                'ascent_style',
                'Count',
                ]
            }]
    )

    cht = Chart(
            datasource = data,
            series_options =
              [{'options':{
                  'type': 'pie',
                  'stacking': False},
                'terms':{
                    'ascent_style': [
                    'Count'
                    ]
                  }
                }],
            chart_options =
              {'title': {
                   'text': 'Styles of Ascent'},
               },
            x_sortf_mapf_mts=(None, verbose_style, False))
    return cht

def training_grade_pie_chart(self, **kwargs):
    qs = Top.objects.filter(training__pk = self.kwargs.get('pk'))

    data = DataPool(
           series=
            [{'options': {
               'source': qs.values('grade_fr').order_by().annotate(
                                               Count = Count('grade_fr')
                                               )},
              'terms': [
                'grade_fr',
                'Count',
                ]
            }]
    )

    cht = Chart(
            datasource = data,
            series_options =
              [{'options':{
                  'type': 'pie',
                  'stacking': False},
                'terms':{
                    'grade_fr': [
                    'Count'
                    ]
                  }
                }],
            chart_options =
              {'title': {
                   'text': 'Number of Routes'},
               })
    return cht

def gym_pie_chart(self, **kwargs):
    qs = Training.objects.filter(user__username = self.kwargs.get('username'))
    data = DataPool(
           series=
            [{'options': {
               'source': qs.values('location__name').order_by().annotate(Count=Count('location__name'))
               },
              'terms': [
                'location__name',
                'Count',
                ]
            }]
    )

    cht = Chart(
            datasource = data,
            series_options =
              [{'options':{
                  'type': 'pie',
                  'stacking': False},
                'terms':{
                    'location__name': [
                    'Count'
                    ]
                  }
                }],
            chart_options =
              {'title': {
                   'text': 'Gyms'},
               })
    return cht
