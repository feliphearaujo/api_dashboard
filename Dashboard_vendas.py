# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Incorporate data
df = pd.read_csv('sales_data_samples.csv',encoding = 'latin-1')
# Transformar em datetime 
df['Data_Pedido'] = pd.to_datetime(df['Data_Pedido'])
df['Ano'] = df['Data_Pedido'].dt.year
df['Mes'] = df['Data_Pedido'].dt.month_name()

colors = {
    'background': '#212428',
    'text': 'white'
}

#pie chart
fig = px.pie(df, values='Valor_Total_Venda', names='Regional', title=' Valor Total de Vendas por Região')

df_agrupado_rep = df.groupby(['Nome_Representante'])['Valor_Total_Venda'].sum().reset_index()

figrp = px.bar(df_agrupado_rep, x='Nome_Representante', y='Valor_Total_Venda', text_auto=True, title=f'Valor Total de Vendas por representante')
figrp.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font=dict(
        color=colors['text']
    )
)

figrp.update_xaxes(showgrid=False)  #para não mostrar as linhas de grade no eixo x 
figrp.update_yaxes(showgrid=False)


# Initialize the app

external_stylesheets = [dbc.themes.SLATE]

app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div('DASHBOARD VENDAS', className=".text-light-emphasis text-center fs-3",style={
                            'text-align': 'center',
                            'font-weight': 'bold',
                            'font-size': '60px',
                            'color': '#FFFF',
                            'margin-top':'10px'
        })
    ]),
    dbc.Row(
        [
            dbc.Col(
                md=6,
                children=[
                    dbc.Row(
                        style={'margin': '5px'},children=[
                        html.H4('Total de Vendas / Mês',style={
                            'text-align': 'center',
                            'font-weight': 'bold',
                            'font-size': '30px',
                            'color': '#FFFF',
                            'background-color': '#212428',
                            'padding':'10px',
                            'margin':'5px'
                        }),
                        ]
                    )
                ]
            ),
            dbc.Col(
                md=6,
                children=[
                    dbc.Row(
                        style={'margin': '5px',
                                'margin-right':'25px'
                            },
                        children=[
                        html.H4('Total de Vendas / Representante',
                        style={
                            'text-align': 'center',
                            'font-weight': 'bold',
                            'font-size': '30px',
                            'color': '#FFFF',
                            'background-color': '#212428',
                            'padding':'10px',
                            'margin':'5px',
                        })
                        ],
                    )
                ]
            ),
            dbc.Row(
                [
                    # Gráfico de linhas
                    dbc.Col(
                        md=5,
                        children=[
                            dcc.Graph(
                                id='total-vendas-mes',
                                figure={
                                    'data': [
                                        {'x': df['Data_Pedido'], 'y': df['Valor_Total_Venda'], 'type': 'line', 'name': 'Total de Vendas'},
                                    ],
                                    
                                },
                                style={
                                    'margin-left':'10px',
                                }
                            )
                        ]
                    ),
                    dbc.Col(
                        md=1,
                        children=[
                            dcc.RadioItems(
                                id='filtro-mes',
                                options=[
                                {'label': 'Janeiro', 'value': 'January'},
                                {'label': 'Fevereiro', 'value': 'February'},
                                {'label': 'Março', 'value': 'March'},
                                {'label': 'Abril','value':'April'},
                                {'label': 'Maio','value':'May'},
                                {'label': 'Junho','value':'June'},
                                {'label': 'Julho','value':'July'},
                                {'label': 'Agosto','value':'August'},
                                {'label': 'Setembro','value':'September'},
                                {'label': 'Outubro','value':'October'},
                                {'label': 'Novembro','value':'November'},
                                {'label': 'Dezembro','value':'December'},
                            ],
                            value='January',
                            labelStyle={'display': 'block',
                                        'text-align': 'justify-content', 
                                        'font-family': 'sans-serif',
                                        'color': '#ffff',
                                        'font-size': '12px',
                                        'margin-top': '10px'           
                            }
                        )
                    ],
                    style={
                        'background-color':'#212428' 
                    }
                ),
                dbc.Col(
                    md=6,
                    children=[
                        dcc.Graph(
                                id='total-vendas-repr',
                                figure=figrp,
                                style={
                                    'margin-left':'25px',
                                }
                            )
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    md=12,
                    children=[
                        dbc.Row(
                        style={'margin': '5px',
                                'margin-top':'10px',
                                'margin-bottom':'0px'
                            },
                        children=[
                        html.H4('Total de Vendas / Produto',
                        style={
                            'text-align': 'center',
                            'font-weight': 'bold',
                            'font-size': '30px',
                            'color': '#FFFF',
                            'background-color': '#212428',
                            'padding':'10px',
                            'margin':'5px',
                        })
                        ]),
                        dbc.Row(
                            children=[
                                html.Div(className='custom-dropdown-style-1',
                                        children=[
                                            dcc.Dropdown(
                                                id = 'filtro-nome-produto',
                                                value = 'SSD',
                                                options = [
                                                            {'label': x , 'value': x}
                                                            for x in df['Nome_Produto'].unique()
                                                        ],
                                                className='dropdown-class-1',
                                                style={
                                                    'margin':'10px',
                                                    'background-color':'#6c6cf3',
                                                    'border':'none',
                                                    'border-radius':'10px'
                                                    
                                                },
                                                placeholder="Nome do Produto",
                                    ),
                                ])
                            ]),
                            html.Div(
                                style={'heigth':'600px',
                                        'margin':'10px',
                                        'background-color':'#212428'},
                                children=[
                                    dash_table.DataTable(
                                id='total-vendas-produto-tabela',
                                columns=[{"name": i, "id": i} for i in df.columns],
                                data=df.to_dict('records'),
                                style_table={
                                    'height':'300px',
                                    'overflowX': 'auto',
                                    'overflowY':'auto',
                                },
                                style_as_list_view=True,
                                style_cell={'padding': '5px'},
                                style_header={
                                    'backgroundColor': '#6c6cf3',
                                    'fontWeight': 'bold',
                                    'color':'#212428'
                                },
                                style_data={
                                    'color': 'white',
                                    'backgroundColor': colors['background']
                                },),
                            ])
                ]),

        ]),
        dbc.Row(children=[
            dbc.Col(md=4,children=[
                dbc.Row(style={'margin': '5px'
                            },children=[
                    html.H4('Total de Vendas / Região',
                        style={
                            'text-align': 'center',
                            'font-weight': 'bold',
                            'font-size': '30px',
                            'color': '#FFFF',
                            'background-color': '#212428',
                            'padding':'10px',
                            'margin':'5px',
                        }),
                ])
            ]),
            dbc.Col(md=8,children=[
                dbc.Row(style={'margin': '5px'
                            },children=[
                    html.H4('Total de Vendas / Estado',
                        style={
                            'text-align': 'center',
                            'font-weight': 'bold',
                            'font-size': '30px',
                            'color': '#FFFF',
                            'background-color': '#212428',
                            'padding':'10px',
                            'margin':'5px',
                        }),
                ])
            ]),
            dbc.Row([
                dbc.Col(md = 4, children=[
                    html.Div(
                                        children=[
                                            dcc.Dropdown(
                                                id = 'filtro-regiao',
                                                value = 'Todas',
                                                options = [
                                                            {'label': 'Sudeste', 'value': 'Sudeste'},
                                                            {'label': 'Nordeste', 'value': 'Nordeste'},
                                                            {'label': 'Regiões', 'value': 'Todas'},
                                                        ],
                                                style={
                                                    'margin':'10px',
                                                    'background-color':'#6c6cf3',
                                                    'border':'none',
                                                    'border-radius':'10px'
                                                },
                                                placeholder="Região",
                                    ),
                                ])
                ]),
                dbc.Col(md=4,children=[
                    html.Div(
                                        children=[
                                            dcc.Dropdown(
                                                id = 'filtro-estado',
                                                value = None,
                                                options = [
                                                            {'label': x , 'value': x}
                                                            for x in df['Estado_Cliente'].unique()
                                                        ],
                                                style={
                                                    'margin':'10px',
                                                    'background-color':'#6c6cf3',
                                                    'border':'none',
                                                    'border-radius':'10px'
                                                },
                                                placeholder="Estado",
                                    ),
                                ])
                ]),
                dbc.Col(md=4,children=[
                    html.Div(
                                        children=[
                                            dcc.Dropdown(
                                                id = 'filtro-cidade',
                                                value = None,
                                                options = [
                                                            {'label': x , 'value': x}
                                                            for x in df['Cidade_Cliente'].unique()
                                                        ],
                                                style={
                                                    'margin':'10px',
                                                    'background-color':'#6c6cf3',
                                                    'border':'none',
                                                    'border-radius':'10px'
                                                },
                                                placeholder="Cidade",
                                    ),
                                ])
                ])
            ])
        ]),
        dbc.Row(children=[
            dbc.Col(md=4,style={
                'margin':'10px'
            },
                    children=[
                    dcc.Graph(id = 'pie-fig', figure = fig)
            ]),
            dbc.Col(md=7 ,style={'margin':'10px',
                                'margin-left':'30px'
                                },children=[
                dcc.Graph(
                                id='total-vendas-estado',
                                figure={
                                    'data': [
                                        {'x': df['Estado_Cliente'], 'y': df['Valor_Total_Venda'], 'type': 'bar'},
                                    ],
                                    
                                },
                            )
            ])
        ])
        
    ])

], fluid=True)

@app.callback(
    Output( component_id = 'total-vendas-mes', component_property= 'figure'),
    Input(component_id='filtro-mes', component_property='value')
)
def filtra_mes(selected_month):
    filtered_df = df[df['Mes'] == selected_month]
    df_agrupado = filtered_df.groupby(['Data_Pedido'])['Valor_Total_Venda'].sum().reset_index()
    
    fig = px.line(df_agrupado, x='Data_Pedido', y='Valor_Total_Venda', title=f'Dados filtrados para o mês {selected_month}')
    
    fig.update_xaxes(showgrid=False)  #para não mostrar as linhas de grade no eixo x 
    fig.update_yaxes(showgrid=False)

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(
            family='Arial', 
            size=12,  
            color=colors['text']  
        ), 
    )

    return fig

@app.callback(
    Output( component_id = 'total-vendas-produto-tabela', component_property= 'data'),
    Input(component_id='filtro-nome-produto', component_property='value')
)
def filtra_nome(product_name):
    filtered_df = df[df['Nome_Produto'] == product_name]
    return filtered_df.to_dict('records')

@app.callback(
    Output(component_id = 'pie-fig', component_property= 'figure'),
    Input(component_id='filtro-regiao', component_property='value')
)
def filtra_regiao(region):
    if region == None:
        fig = px.pie(df, values='Valor_Total_Venda', names='Regional', title=f'Dados filtrados para {region} as regiões')
    elif region == 'Todas':
        fig = px.pie(df, values='Valor_Total_Venda', names='Regional', title=f'Dados filtrados para {region} as regiões')
    else:
        filtered_df = df[df['Regional'] == region]
        fig = px.pie(filtered_df, values='Valor_Total_Venda', names='Regional', title=f'Dados filtrados para a região {region}')
        fig.update_traces(textinfo='value')

    fig.update_xaxes(showgrid=False)  #para não mostrar as linhas de grade no eixo x 
    fig.update_yaxes(showgrid=False)

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(
            family='Arial', 
            size=12,  
            color=colors['text']  
        ), 
    )

    return fig

@app.callback(
    Output(component_id = 'total-vendas-estado', component_property='figure'),
    Input(component_id = 'filtro-estado', component_property='value'),
    Input(component_id='filtro-cidade',component_property='value')
)
def filtra_estado(estado,cidade):
    filter_df = df[df['Estado_Cliente'] == estado]
    df_agrupado1 = df.groupby(['Estado_Cliente'])['Valor_Total_Venda'].sum().reset_index()
    df_agrupado2 = filter_df.groupby(['Cidade_Cliente'])['Valor_Total_Venda'].sum().reset_index()

    if estado == None and cidade == None:
        fig = px.bar(df_agrupado1,x='Estado_Cliente',y='Valor_Total_Venda')
    elif estado != None and cidade == None:
        fig = px.bar(df_agrupado2, x='Cidade_Cliente', y='Valor_Total_Venda', title=f'Dados filtrados para o estado {estado}')
    else:
        df_cidade = df[df['Cidade_Cliente'] == cidade]
        df_agrupado3 = df_cidade.groupby(['Cidade_Cliente'])['Valor_Total_Venda'].sum().reset_index()
        fig = px.bar(df_agrupado3, x='Cidade_Cliente', y='Valor_Total_Venda', text_auto=True, title=f'Dados filtrados para o estado {estado}')

    fig.update_xaxes(showgrid=False)  #para não mostrar as linhas de grade no eixo x 
    fig.update_yaxes(showgrid=False)

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font=dict(
            family='Arial', 
            size=12,  
            color=colors['text']  
        ), 
    )

    return fig

@app.callback(
    Output(component_id = 'filtro-cidade', component_property='options'),
    Input(component_id='filtro-estado',component_property='value')
)
def filtra_estado_dropdown(estado):
    filter_df = df[df['Estado_Cliente'] == estado]

    if estado == None:
        return [{'label': i, 'value': i} for i in df['Cidade_Cliente'].unique()]
    else:
        return [{'label': i, 'value': i} for i in filter_df['Cidade_Cliente'].unique()]


# Run the app
if __name__ == '__main__':
    app.run(debug=True)