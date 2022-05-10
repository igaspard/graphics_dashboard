import os
import sys
import time
import re
from dash import Dash, html, dash_table
import pandas as pd
from pandas.api.types import is_numeric_dtype

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

app = Dash(__name__)


def creat_df_3dmark(input_xml):
    if not input_xml.endswith('.xml'):
        print('Error: input file is not xml file')
        return None

    df = pd.read_xml(input_xml, xpath='.//result')

    number_list = []
    for name in df.columns:
        if (is_numeric_dtype(df[name]) & df[name].count() > 0):
            number_list.append(name)

    data = []
    for name in number_list:
        if (pd.isnull(df[name][0])):
            data.append(df[name][1])
        else:
            data.append(df[name][0])
    new_df = pd.DataFrame([data], columns=number_list, dtype=float)
    return new_df


def append_df_3dmark(input_xml, df):
    if not input_xml.endswith('.xml'):
        print('Error: input file is not xml file')
        return None

    df_xml = pd.read_xml(input_xml, xpath='.//result')

    data = []
    for name in df.columns:
        if (pd.isnull(df_xml[name][0])):
            data.append(df_xml[name][1])
        else:
            data.append(df_xml[name][0])
    new_df = pd.DataFrame([data], columns=df.columns, dtype=float)
    return pd.concat([df, new_df], ignore_index=True)


app = Dash(__name__)

headline = '3DMark Results'
root = './'
if len(sys.argv) > 1:
    root = sys.argv[1]
headline = headline + ' at ' + root

# 1. list all the sub folder in the root directory
dirs = []
for r, d, f in os.walk(root):
    for dir in d:
        dirs.append(dir)

if dirs == []:
    print('Error: no sub folder in the root directory')
# print(dirs)

# 2. create the file list contain the test items we expect & create dataframe
test_items = ['firestrike', 'firestrike-extreme',
              'nightraid', 'skydiver', 'wildlife']
first_subfolder = os.path.join(root, dirs[0])
files = next(os.walk(first_subfolder), (None, None, []))[2]  # [] if no file
dict_df = {}
for test in test_items:
    for file in files:
        if test+'_' in file.lower():
            dict_df[test] = creat_df_3dmark(
                os.path.join(first_subfolder, file))

# 3. append data into each dataframes from the rest of subfolders
for dir in dirs[1:]:
    subfolder = os.path.join(root, dir)
    files = next(os.walk(subfolder), (None, None, []))[2]
    for test in test_items:
        for file in files:
            if test+'_' in file.lower():
                dict_df[test] = append_df_3dmark(
                    os.path.join(subfolder, file), dict_df[test])

# 4. append the create time of each folder into the dataframe
modified_times = []
for dir in dirs:
    modified_time = os.path.getmtime(os.path.join(root, dir))
    modified_times.append(time.strftime(
        '%Y-%m-%d %H:%M:%S', time.localtime(modified_time)))
s1 = pd.Series(modified_times, name='Last Modified Time')

for test in test_items:
    dict_df[test] = pd.concat([s1, dict_df[test]], axis=1)
    dict_df[test].sort_values(
        by='Last Modified Time', inplace=True, ascending=False, ignore_index=True)
    # 5. Shorten the cloumns by removing the test name
    cleanup_dict = {}
    for name in dict_df[test].columns:
        cleanup_dict[name] = re.sub(test.replace(
            '-', ''), '', name, flags=re.IGNORECASE)
    dict_df[test].rename(columns=cleanup_dict, inplace=True)


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(children=headline, style={
        'textAlign': 'center',
        'color': colors['text']}
    ),

    html.Div(children='This is a dashboard to show the 3DMark results', style={
        'textAlign': 'center',
        'color': colors['text']}
    ),

    html.H2(children=test_items[0], style={'textAlign': 'center', 'color': colors['text']}
            ),
    dash_table.DataTable(
        dict_df[test_items[0]].to_dict('records'),
        [{"name": i, "id": i} for i in dict_df[test_items[0]].columns],
        style_as_list_view=True),

    html.H2(children=test_items[1], style={'textAlign': 'center', 'color': colors['text']}
            ),
    dash_table.DataTable(
        dict_df[test_items[1]].to_dict('records'),
        [{"name": i, "id": i} for i in dict_df[test_items[1]].columns],
        style_as_list_view=True),

    html.H2(children=test_items[2], style={'textAlign': 'center', 'color': colors['text']}
            ),
    dash_table.DataTable(
        dict_df[test_items[2]].to_dict('records'),
        [{"name": i, "id": i} for i in dict_df[test_items[2]].columns],
        style_as_list_view=True),

    html.H2(children=test_items[3], style={'textAlign': 'center', 'color': colors['text']}
            ),
    dash_table.DataTable(
        dict_df[test_items[3]].to_dict('records'),
        [{"name": i, "id": i} for i in dict_df[test_items[3]].columns],
        style_as_list_view=True),

    html.H2(children=test_items[4], style={'textAlign': 'center', 'color': colors['text']}
            ),
    dash_table.DataTable(
        dict_df[test_items[4]].to_dict('records'),
        [{"name": i, "id": i} for i in dict_df[test_items[4]].columns],
        style_as_list_view=True),
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
