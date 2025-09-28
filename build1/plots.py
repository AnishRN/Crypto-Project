import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from .apis import *
import plotly.graph_objects as go
from .forecast import *
from django.http import HttpResponse,JsonResponse

def generate_dashboard_plot():
    dashboard_plot = go.Figure() 
    x = bitcoin['Date']
    dashboard_plot.add_trace(go.Scatter( 
        name='Bitcoin', 
        x=x, 
        y=bitcoin['Close'],
        line=dict(color='yellow')
    ))

    dashboard_plot.add_trace(go.Scatter( 
        name='Ripple', 
        x=x, 
        y=ripple['Close'],
        line=dict(color='grey')
    ))

    dashboard_plot.add_trace(go.Scatter( 
        name='Ethereum', 
        x=x, 
        y=ethereum['Close'],
        line=dict(color='blue')
    ))

    dashboard_plot.add_trace(go.Scatter( 
        name='Litecoin', 
        x=x, 
        y=litecoin['Close'],
        line=dict(color='white')
    ))

    dashboard_plot.add_trace(go.Scatter( 
        name='Dogecoin', 
        x=x, 
        y=dogecoin['Close'],
        line=dict(color='orange')
    ))

    dashboard_plot.update_layout(
        plot_bgcolor='rgba(12, 12, 107, 0.85)', 
        paper_bgcolor='rgba(12, 12, 107, 0.3)',  
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.5)'  
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.5)'
        )
    )
    return dashboard_plot.to_html(full_html=True, include_plotlyjs=True)

def plot_forecast(currency, period, timestamp):
    # Call generate_forecasts directly
    future_data, model_params = generate_forecasts(currency, period, timestamp)

    # Plot forecast using model_params and forecast_data
    forecast_fig = plot_plotly(model_params, future_data)
    div = forecast_fig.to_html(full_html=False, include_plotlyjs=False)
    return div

'''def plot_components(currency, period, timestamp):
    # Call generate_forecasts directly
    forecast_data, model_params = generate_forecasts(currency, period, timestamp)

    # Plot the components
    component_fig = model_params.plot_components(forecast_data)

    # Convert the plotly figure to HTML
    div = component_fig.to_html(full_html=False, include_plotlyjs=False)
    return div'''


def generate_trend(currency):
    if currency == "BTC-USD":
        data = btc_data
    elif currency == "LTC_USD":
        data = ltc_data
    elif currency == "XRP-USD":
        data = xrp_data
    elif currency == "DGC-USD":
        data = dgc_data
    elif currency == "ETH-USD":
        data = eth_data
        
    if data is not None:
        line_trace = go.Scatter(
            x=data['Date'],
            y=data['Close'],  # Using Close prices for the y-axis
            mode='lines',
            name='Closing Price'
        )

        layout = {
            'title': 'Closing Price Trend',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Closing Price'}
        }
        

        fig = go.Figure(data=[line_trace], layout=layout)
        return fig.to_html(full_html=True, include_plotlyjs=True)
    else:
        return "Currency not found"


def generate_trend_plot(currency):
        
    if currency == "BTC-USD":
        data = btc_data
    elif currency == "LTC-USD":  
        data = ltc_data
    elif currency == "XRP-USD":
        data = xrp_data
    elif currency == "DGC-USD":
        data = dgc_data
    elif currency == "ETH-USD":
        data = eth_data
            
    if data is not None:
        candlestick_trace = go.Candlestick(
            x=data['Date'],
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Candlestick'
        )

        layout = go.Layout(
            title={
                'text': 'Price Trend Chart',
                'font': {
                    'color': 'white'
                }
            },
            xaxis={
                'title': 'Date',
                'title_font': {'color': 'white'},
                'tickfont': {'color': 'white'}
            },
            yaxis={
                'title': 'Price',
                'title_font': {'color': 'white'},
                'tickfont': {'color': 'white'}
            },
            plot_bgcolor='rgba(12, 12, 107, 0.85)',  # Dark background for the plot area
            paper_bgcolor='rgba(12, 12, 107, 0.3)'   # Lighter dark shade for the entire chart area
        )

        fig = go.Figure(data=[candlestick_trace], layout=layout)
        return fig.to_html(full_html=True, include_plotlyjs=True)
    else:
        return "Currency not found"
    
def generate_volume_plot(currency):
    volume_plot = go.Figure() 
    
    if currency == "BTC-USD":
        data = btc_data
        name = 'Bitcoin'
    elif currency == "LTC-USD":  
        data = ltc_data
        name = 'Litecoin'
    elif currency == "XRP-USD":
        data = xrp_data
        name = 'Ripple'
    elif currency == "DGC-USD":
        data = dgc_data
        name = 'Dogecoin'
    elif currency == "ETH-USD":
        data = eth_data
        name = 'Ethereum'
    x = data['Date']
    volume_plot.add_trace(go.Scatter( 
        name=name, 
        x=x, 
        y=data['Volume'],
        line=dict(color='blue')
    ))

    volume_plot.update_layout(
        title="Trade Volume Trend",
        plot_bgcolor='rgba(12, 12, 107, 0.85)', 
        paper_bgcolor='rgba(12, 12, 107, 0.3)',  
        font=dict(
            family="Arial",
            size=12,
            color="white"
        ),
        xaxis=dict(
            title = "Date",
            gridcolor='rgba(255,255,255,0.5)'  
        ),
        yaxis=dict(
            title = "Volume",
            gridcolor='rgba(255,255,255,0.5)'
        )
    )
    return volume_plot.to_html(full_html=True, include_plotlyjs=True)