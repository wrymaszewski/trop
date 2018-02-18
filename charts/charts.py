from chartit import Chart, DataPool
from routes.models import Ascent

#Helper functions
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

#generic chart views
def pie(queryset, terms, title, verbose=None):
    data = DataPool(
           series=
            [{'options': {
               'source': queryset
               },
              'terms': [
                terms[0],
                terms[1],
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
                    terms[0]: [
                    terms[1]
                    ]
                  }
                }],
            chart_options =
              {'title': {
                   'text': title},
               },
                x_sortf_mapf_mts=(None, verbose, False))
    return cht

def line(queryset, terms, title, axes, verbose=None):
    data = DataPool(
           series=
            [{'options': {
               'source': queryset
            },
              'terms': [
                terms[0],
                terms[1]
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
                    terms[0]: [
                    terms[1]
                    ]
                  }
                }],
            chart_options =
              {'title': {
                   'text': title},
              'xAxis': {
                  'title': {
                      'text': axes[0]
                  }
              },
              'yAxis': {
                  'title': {
                      'text': axes[1]
                  }
              }
             },
                 x_sortf_mapf_mts=(None, verbose, False))
    return cht
