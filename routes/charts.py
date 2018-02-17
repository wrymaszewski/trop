from .models import Ascent, Route, Place
from .scales import convert_scale
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
def route_pie_chart(self, **kwargs):
    data = DataPool(
           series=
            [{'options': {
               'source': Route.objects.filter(location__slug__iexact = self.kwargs.get('slug')).values('grade').order_by().annotate(
                                               Count = Count('grade')
                                               )},
              'terms': [
                'grade',
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
                    'grade': [
                    'Count'
                    ]
                  }
                }],
            chart_options =
              {'title': {
                   'text': 'Number of Routes'},
               })
    return cht


def route_ascent_chart(self, **kwargs):
    qs = Ascent.objects.filter(route__slug__iexact = self.kwargs.get('route_slug'))

    data = DataPool(
           series=
            [{'options': {
               'source':  qs.annotate(date_trunc=TruncMonth('date')).values('date_trunc').order_by().annotate(Count = Count('date_trunc'))

            },
              'terms': [
                'date_trunc',
                'Count'
                ]
            }]
    )
    cht = Chart(
            datasource = data,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                    'date_trunc': [
                    'Count'
                    ]
                  }
                }],
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
             },
             x_sortf_mapf_mts=(None, verbose_months, False))
    return cht

def ascent_pie_chart(self, **kwargs):
    qs = Ascent.objects.filter(route__slug__iexact = self.kwargs.get('route_slug'))
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

def user_ascent_chart(self, **kwargs):
    qs = Ascent.objects.filter(user__username__iexact = self.kwargs.get('username'))

    data = PivotDataPool(
           series=
            [{'options': {
               'source':  (qs.annotate(date_trunc=TruncMonth('date'))
                            .values('date_trunc', 'route__grade_fr')
                            .order_by('route__grade_fr')
                            .order_by('date_trunc')),
                'categories': 'date_trunc',
                'legend_by': 'route__grade_fr'
            },
              'terms': {
                'count': Count('route__grade_fr')
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

def user_ascent_pie_chart(self, **kwargs):
    qs = Ascent.objects.filter(user__username__iexact = self.kwargs.get('username'))
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
