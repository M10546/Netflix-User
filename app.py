from flask import Flask, render_template,request, redirect, url_for
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import openpyxl
import plotly.figure_factory as ff
import plotly.graph_objects as go

df = pd.read_excel('Netflix.xlsx')
bins3 = [0, 101, 201, 301, 401, 501, 601, 701, 801, 901, 1001]
labels3 = ['0-100','100-200','200-300','300-400','400-500','500-600','600-700','700-800','800-900','900-1000']

df['Category_Hours'] = pd.cut(df['Watch_Time_Hours'], bins=bins3, labels=labels3, right= True)


app = Flask(__name__)
dash_app = dash.Dash(
    'mahreen_fathima_data_netflix',  
    server=app,
    url_base_pathname='/dashboard/'
)


@app.route("/")
def homepage():
    return render_template("index.html")

@app.route('/check_password', methods=['POST'])
def check_password():
    password = request.form['password']
    if password == 'tudum':
        return redirect(url_for('intro'))
    else:
        return render_template('index.html', error='Incorrect password. Try again.')

@app.route('/intro')
def intro():
    return render_template('intro.html')

pie_fig = px.pie(df, names='Favorite_Genre', values='User_ID', color_discrete_sequence=['#831010','#A91916','#db0000','#f01e2c','#e1dcdc','#9C8686','#564d4d'])
pie_fig.update_traces(
    hovertemplate='%{label}<extra></extra>'
)
pie_fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font = dict(
        family='"Lucida Grande", sans-serif'
    ),
    font_color='white',
    hovermode='x'
)

avg_watch = df['Watch_Time_Hours'].mean()
kpi1 = go.Figure(go.Indicator(
    mode="number",
    value=avg_watch,
    number={'font': {'size': 40, 'color':"#f8c5c5", 'family':'Helvetica'}},
))


kpi1.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font = dict(
        family='"Lucida Grande", sans-serif'
    ),
    font_color='white',
)

avg_age = df['Age'].mean()
kpi2 = go.Figure(go.Indicator(
    mode='number',
    value=avg_age,
    number={'font': {'size': 40, 'color':"#F8C5C5", 'family':'Helvetica'}}
))

kpi2.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='white'
)


hist_fig = px.histogram(df, x='Favorite_Genre', color='Subscription_Type', barmode='group', color_discrete_sequence=['#db0000', "#CBC7C7",'#564d4d'])
hist_fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    
    xaxis_showgrid = False,
    yaxis_showgrid=False,
    yaxis_title = 'Users',
    xaxis_title='Favorite Genre'
)
area_grp = df.groupby('Age_Category')['Watch_Time_Hours'].mean().reset_index()
area_plot = px.area(area_grp, x='Age_Category', y='Watch_Time_Hours', color_discrete_sequence=["#e73434"], markers=True)
area_plot.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    xaxis_showgrid = False,
    yaxis_showgrid=False,
    yaxis_title = 'Watch Time Average',
    xaxis_title='Age Category'
)
c_df = df.groupby('Country')['Age'].mean().round(2).reset_index()
country_fig = px.scatter_geo(c_df, locations="Country", color="Age",
                     hover_name="Country", size="Age", color_continuous_scale='reds',
                     projection="natural earth", locationmode = "country names")
country_fig.update_geos(
    showland=True, landcolor="#1f1f1f",
    showocean=True, oceancolor="#0d0d0d",
    showlakes=True, lakecolor="#1c1c1c",
    showrivers=True, rivercolor="#2c2c2c",
    bgcolor="rgba(0,0,0,0)"
)
country_fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='white',
)
new = df.groupby('Country')['User_ID'].count().sort_values(ascending=False).reset_index()
overall =  px.bar(new, x='Country', y='User_ID', color='Country', 
color_discrete_sequence=["#700404","#980b0b","#d11e1e","#fc2424","#d44e4e","#c17575","#ea9999","#f0b3b3","#d0bcbc","#807676"]
)
overall.update_traces(marker_line_width=0, selector=dict(type="bar"))
overall.update_layout(
    bargap=0.5,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    showlegend=False,
    xaxis_showgrid = False,
    yaxis_showgrid=False,
    yaxis_title = 'Users',
    xaxis_title='Favorite Genre'
)

sub_df = df.groupby(['Country','Subscription_Type', 'Category_Hours']).count().reset_index()
sunburst = px.sunburst(
    sub_df,
    path=['Subscription_Type', 'Country'],
    values='User_ID',
    color='Subscription_Type',
    color_discrete_sequence=['#db0000', "#ebedee", "#424141"]
)
sunburst.update_traces(
    branchvalues='total',
    hovertemplate='<b>%{label}</b><br>Users: %{value}<br>Percentage: %{percentParent:.2%}'
)

sunburst.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_showgrid=False,
    yaxis_showgrid=False,
    font_color='white'
)

date_df = df.groupby('Category_Hours').agg({'Watch_Time_Hours':'mean','Favorite_Genre':'first', 'Age':'mean', 'Subscription_Type':'first'}).sort_values(by='Category_Hours').reset_index()
watch = px.line(date_df, x='Category_Hours', y='Age',color_discrete_sequence=["#f45252"], markers=True)
watch.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_showgrid=False,
    xaxis_title='Watch Hours Category',
    font_color='white'
)

dash_app.layout = html.Div(className='dashboard',
                           children=[
                               html.H1('Netflix Audience Insights'),
                               html.Div(className='piechart' ,children=[
                                    html.H3("What Everyone's Watching?", className='chart1' ),
                                    dcc.Graph(
                                        id='piechart',
                                        figure = pie_fig,
                                        style={'backgroundColor':'rgba(0,0,0,0)'}
                                    )

                               ]),
                               html.Div(className='kpi1', title="This shows the average hours watched by users", children=[
                                html.H3("Average Watch Hours", className='kpi1t'),
                                   dcc.Graph(
                                       id='kpi1',
                                       figure=kpi1,
                                       config={'displayModeBar': False},
                                       style={'backgroundColor':'rgba(0,0,0,0)'}
                                   )
                                   
                               ]),
                                html.Div(className='kpi2', title="This shows the average age of the users", children=[
                                html.H3("Average Age", style={'padding':'10px'}, className='kpi2t'),
                                   dcc.Graph(
                                       id='kpi2',
                                       figure=kpi2,
                                       config={'displayModeBar': False},
                                       style={'backgroundColor':'rgba(0,0,0,0)'}
                                   )
                                   
                               ]),
                               html.Div(className='hist_chart', children=[
                                   html.H3("Plan Breakdown : Genre Edition ", style={'padding':'20px'}, className='histt'),
                                   dcc.Graph(
                                       id='histchart',
                                       figure=hist_fig,
                                       style={'backgroundColor':'rgba(0,0,0,0)'}
                                   )
                               ]),
                               html.Div(className='sun', children=[
                                   html.H3("Subscription by Country - Who's Leading?",style={'padding':'20px', 'align-items':'center'}, className='sunt'),
                                   dcc.Graph(
                                       id='sun',
                                       figure=sunburst,
                                       style={'backgroundColor':'rgba(0,0,0,0)'}
                                   )
                               ]),
                               html.Div(className='watch', children=[
                                   html.H3('Binge Watchers Age Wise', style={'padding':'20px'}, className='watcht'),
                                   dcc.Graph(
                                       id='watch',
                                       figure=watch,
                                       style={'backgroundColor':'rgba(0,0,0,0)'}
                                   )
                               ]),
                               html.Div(className='countries', children=[
                                   html.H3('User Distribution Across Countries',style={'padding':'20px'}, className='countryt'),
                                   dcc.Graph(
                                       id='countries',
                                       figure=overall,
                                       style={'backgroundColor':'rgba(0,0,0,0)'}
                                   )
                               ]),
                               html.Div(className='areachart', children=[
                                   html.H3('Stream Time Breakdown by Age',style={'padding':'20px'}, className='areat'),
                                   dcc.Graph(
                                       id='area',
                                       figure=area_plot,
                                       style={'backgroundColor':'rgba(0,0,0,0)'}
                                   )
                               ]),
                               html.Div(className='map', children=[
                                   html.H3('Age Demographics Across Countries',style={'padding':'20px'}, className='mapt'),
                                   dcc.Graph(
                                       id='map',
                                       figure=country_fig,
                                       style={'backgroundColor':'rgba(0,0,0,0)'}
                                   )
                               ]),
                                
                               
                               

                           ])
if __name__ == "__main__":
    app.run(debug=True)