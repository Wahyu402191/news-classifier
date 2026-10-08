"""
Data visualization utilities using Plotly
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict
from config import COLOR_SCHEME


def plot_probability_distribution(probabilities: Dict[str, float]) -> go.Figure:
    """
    Create horizontal bar chart for probability distribution
    
    Args:
        probabilities: Dictionary with category probabilities
        
    Returns:
        Plotly figure object
    """
    categories = list(probabilities.keys())
    values = [probabilities[cat] * 100 for cat in categories]  # Convert to percentage
    
    colors = [COLOR_SCHEME.get(cat.lower(), COLOR_SCHEME['primary']) for cat in categories]
    
    fig = go.Figure(data=[
        go.Bar(
            y=categories,
            x=values,
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(color='rgba(0,0,0,0.2)', width=1)
            ),
            text=[f'{v:.1f}%' for v in values],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Probability: %{x:.2f}%<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text='Classification Probability',
            font=dict(size=16, family='Arial, sans-serif')
        ),
        xaxis=dict(
            title='Probability (%)',
            range=[0, 100],
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)'
        ),
        yaxis=dict(
            title=''
        ),
        height=250,
        margin=dict(l=10, r=10, t=40, b=10),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig


def plot_confusion_matrix(cm, labels: list) -> go.Figure:
    """
    Create confusion matrix heatmap
    
    Args:
        cm: Confusion matrix array
        labels: List of class labels
        
    Returns:
        Plotly figure object
    """
    # Create annotations
    annotations = []
    for i, row in enumerate(cm):
        for j, value in enumerate(row):
            annotations.append(
                dict(
                    x=labels[j],
                    y=labels[i],
                    text=str(value),
                    font=dict(color='white' if value > cm.max() / 2 else 'black', size=16),
                    showarrow=False
                )
            )
    
    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=labels,
        y=labels,
        colorscale='Blues',
        showscale=True,
        hovertemplate='Actual: %{y}<br>Predicted: %{x}<br>Count: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='Confusion Matrix',
            font=dict(size=16, family='Arial, sans-serif')
        ),
        xaxis=dict(title='Predicted Label', side='bottom'),
        yaxis=dict(title='Actual Label', autorange='reversed'),
        annotations=annotations,
        height=400,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    
    return fig


def plot_token_statistics(matched: int, oov: int) -> go.Figure:
    """
    Create pie chart for token statistics
    
    Args:
        matched: Number of matched tokens
        oov: Number of out-of-vocabulary tokens
        
    Returns:
        Plotly figure object
    """
    labels = ['Matched Vocabulary', 'Out of Vocabulary']
    values = [matched, oov]
    colors = [COLOR_SCHEME['secondary'], COLOR_SCHEME['sport']]
    
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors, line=dict(color='white', width=2)),
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text='Token Coverage Analysis',
            font=dict(size=16, family='Arial, sans-serif')
        ),
        height=350,
        margin=dict(l=10, r=10, t=40, b=10),
        showlegend=True
    )
    
    return fig


def plot_dataset_distribution(sport_count: int, finance_count: int) -> go.Figure:
    """
    Create bar chart for dataset distribution
    
    Args:
        sport_count: Number of sport articles
        finance_count: Number of finance articles
        
    Returns:
        Plotly figure object
    """
    categories = ['Sport', 'Finance']
    counts = [sport_count, finance_count]
    colors = [COLOR_SCHEME['sport'], COLOR_SCHEME['finance']]
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=counts,
            marker=dict(color=colors, line=dict(color='rgba(0,0,0,0.2)', width=1)),
            text=counts,
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Articles: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text='Training Dataset Distribution',
            font=dict(size=16, family='Arial, sans-serif')
        ),
        xaxis=dict(title='Category'),
        yaxis=dict(title='Number of Articles', showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
        height=350,
        margin=dict(l=10, r=10, t=40, b=10),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig
