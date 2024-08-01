import dash
import numpy as np
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import calc_channel


app = dash.Dash(__name__)

N = 1
Fpow = 6
flo = 0.75   # D
xx = 1
# структура страницы
def plot_D(n, fpow):
    """
    построение графика
    :param n: число каналов
    :param fpow: степень
    :return:
    """
    q = np.linspace(0, 7, 500)
    d_res_D = [calc_channel.D(n, x, 10**(-fpow)) for x in q]

    nfig = go.Figure()
    nfig.add_trace(go.Scatter(x=q**2, y=d_res_D, mode='lines', name=f'D({n},{10**(-fpow)})'))

    return nfig

def plot_D0(n, fpow):
    """
    построение графика
    :param n: число каналов
    :param fpow: степень
    :return:
    """
    q = np.linspace(0, 7, 500)

    d_res_D0 = [calc_channel.D0(n, x, 10 ** (-fpow)) for x in q]

    nfig1 = go.Figure()

    nfig1.add_trace(go.Scatter(x=q**2, y=d_res_D0, mode='lines', name=f'D0({n},{10 ** (-fpow)})'))
    return nfig1

def plot_F(n, d):   #
    """
    построение графика
    :param n: число каналов
    :param DD: D
    :return:
    """
    q = np.linspace(0, 7, 500)

    d_res_F = [calc_channel.F1(n, x, d) for x in q]
    nfig2 = go.Figure()

    nfig2.add_trace(go.Scatter(x=q**2, y=d_res_F, mode='lines', name=f'F1({n},{d})'))
    return nfig2



app.layout = html.Div(children=[

    dcc.Markdown('''
            # Зависимость характеристик обнаружения от отношения сигнал-помеха по мощности $q^2$
            ## Формулы для нахождения вероятности:
    
            Вероятность правильного обнаружения D:
            $$
            D = 1 - \\Phi\\left (\\frac{\\Lambda_{p0}-M(\\Lambda_p)}{\\sigma_{\\Lambda_p}}\\right )
            $$
            Вероятность пропуска полезного сигнала 
            $D_0$:
            $$
            D_0 = 1-D
            $$
            Вероятность ложной тревоги F:
            $$
            F = 1 - \\Phi\\left (\\frac{\\Lambda_{p0}}{\\sigma_{\\Lambda_p}}\\right )
            ''', mathjax=True),

    html.Div(children=[
        html.P("Число каналов (N)"),
        dcc.Slider(id='val_N', min=1., max=5., step=1, value=N,
                   tooltip={"placement": "bottom", "always_visible": True}),
        html.P("Степень F=10^-p"),
        dcc.Slider(id='val_Fpow', min=1., max=6., step=1, value=Fpow,
                   tooltip={"placement": "bottom", "always_visible": True}),
        html.P("Значение D"),
        dcc.Slider(id='val_D', min=0.75, max=0.95, step=0.05, value=flo,
                   tooltip={"placement": "bottom", "always_visible": True}),
        html.P("Отображаем кривую"),
        dcc.Dropdown(
            options=['D', 'D0', 'F'],
            #multi=True,
            placeholder='Отобразить',
            id='plots',
            value='D'
        ),

        dcc.Graph(
            mathjax=True,
            id='example-graph',
            figure=plot_D(N, Fpow)

        ),

    ]),
])



@app.callback(
    Output("example-graph", "figure"),
    [Input("val_N", "value"),
     Input("val_Fpow", "value"),
     Input("plots", "value"),
     Input("val_D", "value")])

def update_figure(n, fpow,  v_plot_values, d):
    """
    Обработка измения параметров
    :param n: число каналов
    :param fpow: степень для порога
    :param d: вероятность D
    :return:
    """
    return plot_D0(n, fpow) if 'D0' == v_plot_values else plot_D(n, fpow) if 'D' == v_plot_values else plot_F(n, d) if 'F' == v_plot_values else None




if __name__ == '__main__':
    app.run_server(debug=True)
