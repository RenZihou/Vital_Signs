# -*- encoding: utf-8 -*-
# @Author: RZH

import json
from typing import List, Dict
from datetime import datetime, timedelta

import pandas as pd
import plotly as py
import plotly.graph_objs as go


def change_date(date: str, delta: int) -> str:
    """
    shift date by `delta` days
    :param date: the current date
    :param delta: days to shift backwards (if positive)
    :return: new date
    """
    return (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=delta))\
        .strftime('%Y-%m-%d')


def plot(data) -> None:
    """
    plot `VITAL SIGNS` diagram and save it to `./output/vital_signs.html`
    :param data: data saved as `DataFrame`
    :return: None
    """
    names = json.load(open('./config/subtitles.json', 'r'))
    colors = json.load(open('./config/colors.json', 'r'))
    # params: data, terms, other configs (title, color, size)
    traces: list = []  # plots' information
    axes: Dict[str, dict] = {}  # axes' information
    annotations: List[dict] = []  # subtitles and notes
    count = 0  # number of plots
    height = 0  # height of the image
    y_pos: List[tuple] = []  # y_position of each plot

    for name, plot_type in names.items():
        count += 1
        if plot_type[0] == 'bar':
            y_pos.append((height + plot_type[1], height))
            height += (plot_type[1] + 20)
            traces.append(go.Bar(
                x=data['DATE'], y=data[name], yaxis='y%d' % count,
                marker={'color': colors['filling'], 'line': {'width': 0}},
                name=name
            ))
            axes['yaxis%d' % count] = {
                'zerolinecolor': colors['zero'], 'zerolinewidth': 1,
                'showgrid': False, 'showticklabels': False,
            }
            annotations.append({
                'text': '<b>%s</b>' % name.upper().replace('_', ' '),
            })
        elif plot_type[0] == 'line':
            y_pos.append((height + plot_type[1], height))
            height += (plot_type[1] + 20)
            traces.append(go.Scatter(
                x=data['DATE'], y=data[name], yaxis='y%d' % count,
                marker={'color': colors['line']}, mode='lines',
                name=name,
            ))
            axes['yaxis%d' % count] = {
                'zerolinecolor': colors['zero'], 'zerolinewidth': 1,
                'showgrid': False, 'showticklabels': False,
            }
            annotations.append({
                'text': '<b>%s</b>' % name.upper().replace('_', ' '),
            })
        elif plot_type[0] == 'scatter':
            y_pos.append((height + plot_type[1], height))
            height += (plot_type[1] + 20)
            for each in name.split('|'):
                traces.append(go.Scatter(
                    x=data['DATE'], y=data[each], yaxis='y%d' % count,
                    marker={'color': None}, mode='markers',
                    name=each,
                ))
                axes['yaxis%d' % count] = {
                    'zeroline': False,
                    'showgrid': True, 'gridcolor': colors['grid2'],
                    # 'gridwidth': 1,
                    'showticklabels': True,
                    'tickmode': 'array', 'tickvals': [60, -60, -360, -480],
                    'ticktext':
                        ['    23:00', '    01:00', '    06:00', '    08:00'],
                    'side': 'right',
                }
            annotations.append({
                'text': '<b>%s</b>' % ' & '.join(
                    name.upper().split('|')[::-1]
                ).replace('_', ' '),
            })
        elif plot_type[0] == 'bool':  # TODO: y-axis offset
            y_pos.append((height + plot_type[1], height))
            height += (plot_type[1] + 20)
            traces.append(go.Bar(
                x=data['DATE'], y=data[name], yaxis='y%d' % count,
                marker={'color': colors['filling_2'], 'line': {'width': 0}},
                name=name,
            ))
            axes['yaxis%d' % count] = {
                'zeroline': False,
                'showgrid': True, 'gridcolor': colors['zero'],
                'tickmode': 'array', 'tickvals': [0.5],
                'showticklabels': False,
            }
            annotations.append({
                'text': '<b>%s</b>' % name.upper().replace('_', ' '),
            })
        else:
            y_pos.append((height, height))
            height += 20
            axes['yaxis%d' % count] = {
                'zeroline': False,
                'showgrid': False, 'showticklabels': False,
            }
            annotations.append({
                'text': '',
            })
    for index, value in enumerate(y_pos):
        axes['yaxis%d' % (index + 1)]['domain'] = list(
            map(lambda x: 1 - x / height, value)
        )
        annotations[index].update({
            'x': 1.02, 'xref': 'paper', 'xanchor': 'left',
            'y': 1 - (value[0] - 10) / height, 'yref': 'paper',
            'yanchor': 'top',
            'showarrow': False,
            'font': {'family': 'Montserrat', 'size': 12},
        })
    axes['xaxis'] = {
        'showgrid': True, 'gridcolor': colors['grid'],
        'position': 8 / height, 'anchor': 'free',
        'type': 'date',
        'range': [change_date(data['DATE'][0], -1),
                  change_date(data['DATE'][data.shape[0] - 1], 1)],
        'tickfont': {'family': 'Montserrat', 'size': 10},
        'dtick': 'M1', 'tickformat': '<b>%b</b>\n%Y',
        'ticklabelmode': 'period',
        # TODO: connect vertical grid lines
        }

    layout = go.Layout(
        title={'text': 'V I T A L    S I G N S',
               'font': {'family': 'Geometos', 'size': 16},
               'x': 0.5, 'xanchor': 'center',
               'y': 1 - 40 / height, 'yanchor': 'middle', },
        paper_bgcolor='#f3f3f3',
        plot_bgcolor='#f3f3f3',
        autosize=False,
        width=data.shape[0] * 5 + 230,
        height=height + 150,
        margin=go.layout.Margin(l=50, r=180, t=80, b=70),
        annotations=annotations,
        showlegend=False,
        **axes,
    )

    fig = go.Figure(data=traces, layout=layout)
    py.offline.plot(fig, filename='./output/vital_signs.html')
    return


if __name__ == '__main__':
    plot(pd.read_csv('../data/out.csv'))
    pass
