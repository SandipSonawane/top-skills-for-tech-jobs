import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import base64
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
from collections import Counter
import dash_bootstrap_components as dbc
import dash_table

# import dataset
df1 = pd.read_excel(r".\Data\job_data.xlsx")
df2 = df1[df1['country'] == 'US'].groupby(['state', 'category', 'company']).count()
df2.reset_index(level=0, inplace=True)
df2.reset_index(level=0, inplace=True)
df2.reset_index(level=0, inplace=True)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# add custom stopwords
global new_stopwords
new_stopwords = ['age', 'sexual', 'gender', 'disability', 'race', 'religion', 'belief', 'opportunity', 'employer',
                 'discrimate', 'opportunity', 'equal', 'national', 'origin', 'national', 'veteran', 'orientation',
                 'legally', 'problems', 'solutions', 'processing', 'state', 'peer', 'environment', 'proven',
                 'visit', 'https', 'status', 'jobs', 'amazon', 'diverse', 'individual', 'protected', 'discriminate',
                 'disabilities', 'individuals', 'workplace', 'inclusive', 'please', 'us', 'en', 'new', 'committed',
                 'demonstrated', 'minimum', 'current', 'system', 'pattern', 'fundamental',
                 'strong', 'degree', 'year', 'one', 'least', 'identity', 'accommodation', 'years', 'e g', 'ability',
                 'request',
                 'basis', 'g', 's', 'record', 'experience', 'working', 'etc', 'e', 'knowledge', 'using', 'team',
                 'design',
                 'bachelor', 'solution', 'field', 'related', 'scientist', 'work', 'hands', 'building', 'relevant',
                 'industry',
                 'equivalent', 'business', 'problem', 'skill', 'skills', 'application', 'track', 'similar', 'plus',
                 'including',
                 'professional', 'c c', 'reliability', 'role']

available_categories = df1.category.unique()
available_companies = df1.company.unique()

# maps figure
fig = go.Figure(data=go.Choropleth(
    locations=df2['state'],
    z=df2['job_id'].astype(float),
    locationmode='USA-states',
    colorscale='Blues',
))

fig.update_layout(
    title='Amazon Job Listing by State',
    geo_scope='usa',
    autosize=True,
    hovermode='closest',
    margin=dict(t=100, b=0, l=10, r=10),
)

fig.update_traces(showscale=False)

test_png = r".\Image\wordcould.png"
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')
column_list = ['title', 'country', 'state', 'link']

# define app layout
app.layout = html.Div([
    # title
    html.Div(
        [html.H3('Top skills by employer')], style={'text-align': 'center'}
    ),

    html.Div(className='dropdowns', children=[
        # company dropdown
        html.Div(id='company_dropdown', children=[
            html.Div(className="btn btn-secondary btn-lg", children=[
                html.H4('Select company')]),
            dcc.Dropdown(id='pick_company',
                         options=[{'label': i, 'value': i} for i in available_companies], value='Amazon')
        ]),

        # job category dropdown
        html.Div(id='category_dropdown', children=[
            html.Div(className="btn btn-secondary btn-lg", children=[
                html.H4('Select job category')]),
            dcc.Dropdown(id='pick_category',
                         options=[{'label': i, 'value': i} for i in available_categories], value='Data Science'),
        ]),
    ]),

    html.Div(className='wrapper', children=[

        html.Div(className='nested-wrapper1', children=[
            html.Div(className='card box1', children=[html.H5(id='jobs-box')]),

            # plot wordcloud
            html.Img(id='wordcloud-img', className='chart card', src='data:image/png;base64,{}'.format(test_base64),
                     ),

            html.Div(className='card box2', children=[html.H5(id='category-box')])]),

        # top 20 skills bar graph
        html.Div([
            dcc.Graph(id='my_graph', className='chart card',
                      figure={'data': [{'x': 'state_picker', 'y': 0}],
                              'layout': {'title': 'updating the graph'}})],
        ),

        # maps graph
        html.Div([
            dcc.Graph(id='maps_graph', className='chart card', figure=fig)],
        ),

        # maps graph
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i}
                     for i in column_list],
            style_cell=dict(textAlign='left'),
            page_size=15,
            style_table={'height': 'auto', 'overflowY': 'auto'}
            # style_header=dict(backgroundColor="paleturquoise"),
            # style_data=dict(backgroundColor="lavender")
        )
    ])
])


# update text cards
@app.callback(Output('jobs-box', 'children'),
              Output('category-box', 'children'),
              [Input('pick_company', 'value'),

               Input('pick_category', 'value')]
              )
def update_text_card(company, category):
    input_data = df1[df1.company == company]
    jobs_available = f"{company} jobs available: {len(input_data)}"
    input_data = input_data[input_data.category == category]
    category_jobs_available = f"{company} {category} jobs available: {len(input_data)}"

    return jobs_available, category_jobs_available


# dropdown callback
@app.callback(Output('pick_category', 'options'),
              [Input('pick_company', 'value')])
def update_job_category(company):
    input_data = df1[df1.company == company]
    available_categories_by_company = input_data.category.unique()
    options = [{'label': i, 'value': i} for i in available_categories_by_company]

    return options


# update top 20 skills bar graph
@app.callback(Output('my_graph', 'figure'),
              [Input('pick_company', 'value'),
               Input('pick_category', 'value')])
def update_graph(company, category):
    input_data = df1[df1.company == company]
    data = input_data[input_data.category == category]

    qualification_words = ''

    for word in new_stopwords:
        STOPWORDS.add(word)

    stopwords = set(STOPWORDS)

    for val in data.qualifications:
        val = str(val)
        tokens = val.split()
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        qualification_words += " ".join(tokens) + " "

    wordcloud = WordCloud(width=600, height=350,
                          background_color='white',
                          stopwords=stopwords,
                          min_font_size=8).generate(qualification_words)
    frequencies = wordcloud.process_text(qualification_words)
    frequencies = Counter(frequencies)
    data = frequencies.most_common(20)

    x = [x[1] for x in data]
    y = [y[0] for y in data]
    x.reverse()
    y.reverse()

    # fig = px.bar(y=x, x=y, text='pop')

    fig = go.Figure(go.Bar(
        x=y,
        y=x,
        text=x,
        orientation='v'))

    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(title=f'top 20 skills {category}', title_x=0.5, autosize=True,
                      uniformtext_minsize=8, uniformtext_mode='hide', template='plotly_white',
                      yaxis={'visible': False, 'showticklabels': False})

    return fig


# update maps information
@app.callback(Output('maps_graph', 'figure'),
              [Input('pick_category', 'value'),
               Input('pick_company', 'value')])
def update_graph(category_picker, company_picker):
    df3 = df2[df2.company == company_picker]
    df3 = df3[df3.category == category_picker]
    fig = go.Figure(data=go.Choropleth(
        locations=df3['state'],
        z=df3['job_id'].astype(float),
        locationmode='USA-states',
        colorscale='Blues',
    ))

    fig.update_layout(
        title=f'{company_picker} Job Listing by State for <br>       {category_picker}',
        geo_scope='usa',
        autosize=True,
        hovermode='closest',
        margin=dict(t=100, b=0, l=10, r=10),
    )

    fig.update_traces(showscale=False)

    return fig


# update wordcloud
@app.callback(Output('wordcloud-img', 'src'),
              [Input('pick_company', 'value'),
               Input('pick_category', 'value')])
def insert_word_could_image(company, category):
    input_data = df1[df1.company == company]
    data = input_data[input_data.category == category]

    qualification_words = ''

    for word in new_stopwords:
        STOPWORDS.add(word)

    stopwords = set(STOPWORDS)

    for val in data.qualifications:
        val = str(val)
        tokens = val.split()
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        qualification_words += " ".join(tokens) + " "

    wordcloud = WordCloud(width=600, height=350,
                          background_color='white',
                          stopwords=stopwords,
                          min_font_size=8).generate(qualification_words)
    frequencies = wordcloud.process_text(qualification_words)
    frequencies = Counter(frequencies)
    data = frequencies.most_common(20)

    wc_img = wordcloud.to_file('.\Image\wordcould.png')
    test_png = r".\Image\wordcould.png"
    test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

    src = 'data:image/png;base64,{}'.format(test_base64)
    return src


# update table
@app.callback(Output('table', 'data'),
              [Input('pick_category', 'value'),
               Input('pick_company', 'value')])
def update_table(category_picker, company_picker):
    df3 = df1[df1.company == company_picker]
    df3 = df3[df3.category == category_picker]
    df3 = df3[['title', 'country', 'state', 'link']]
    data = df3.to_dict('records')

    return data


# app.run_server(mode="inline")
app.run_server()
