import datetime
import decimal

import plotly.graph_objects as go
import plotly.io as pio
import requests
from bs4 import BeautifulSoup

from utils import utils
from . import models


def retrieve_data_from_web(target):
    url = utils.define_target_url(target)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    earthquake_data_list = map_data_to_object(soup)

    return earthquake_data_list


def collect_new_data(target):
    earthquake_data_list = retrieve_data_from_web(target)
    new_record_count, new_incoming_data = filter_out_the_existed_data(earthquake_data_list)

    models.Data.objects.bulk_create(new_incoming_data)

    return str(new_record_count) + " record(s) created"


def check_the_amount_of_new_data_available(target):
    earthquake_data_list = retrieve_data_from_web(target)
    new_record_count, new_incoming_data = filter_out_the_existed_data(earthquake_data_list)

    return str(new_record_count) + " new data available"


def filter_out_the_existed_data(earthquake_data_list):
    new_incoming_data = []
    new_record_count = 0

    for earthquake_data in earthquake_data_list:
        if not models.Data.objects.filter(occurrence_time_utc = earthquake_data.occurrence_time_utc,
                                          latitude = earthquake_data.latitude,
                                          longitude = earthquake_data.longitude).exists():
            new_incoming_data.append(earthquake_data)
            new_record_count += 1

    return new_record_count, new_incoming_data


def map_data_to_object(soup):
    earthquake_data_list = []
    tr = soup.body.tbody.find_all('tr')
    for tr_index in range(len(tr)):
        earthquake_data = models.Data()
        td = tr[tr_index].find_all('td')
        format_string = "%Y-%m-%d %H:%M:%S.%f"
        earthquake_data.occurrence_time_utc = datetime.datetime.strptime(str(td[1].string).replace('/', '-')
                                                                         , format_string)
        earthquake_data.latitude = decimal.Decimal(td[2].string)
        earthquake_data.longitude = decimal.Decimal(td[3].string)
        earthquake_data.magnitude = float(str(td[4].string).replace('M', ''))
        earthquake_data.depth_km = float(td[5].string)
        earthquake_data.area = str(td[6].a.string)

        earthquake_data_list.insert(0, earthquake_data)

    return earthquake_data_list


def test():
    # Create your plotly figure
    fig = go.Figure()

    # Add a scatter trace with initial marker size
    fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 2, 5], mode='markers', marker=dict(size=10)))

    # Add a button to update the marker size
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                buttons=[
                    dict(
                        label="Increase Marker Size",
                        method="restyle",
                        args=[{"marker": {"size": fig.data[0].marker.size + 1}}],
                    ),
                    dict(
                        label="Decrease Marker Size",
                        method="restyle",
                        args=[{"marker": {"size": fig.data[0].marker.size - 1}}],
                    ),
                ],
            )
        ]
    )

    # Save the figure as an HTML file
    output_file = 'earthquake/templates/main/file.html'
    pio.write_html(fig, output_file)