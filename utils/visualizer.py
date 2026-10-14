"""
Modul untuk visualisasi data menggunakan Plotly
Membuat chart: bar chart probabilitas, pie chart token, bar chart dataset
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict
from config import COLOR_SCHEME


def plot_probability_distribution(probabilities: Dict[str, float]) -> go.Figure:
    """
    Buat horizontal bar chart untuk menampilkan probabilitas klasifikasi
    Contoh: Sport 75%, Finance 25%
    
    Args:
        probabilities: Dictionary with category probabilities
        
    Returns:
        Plotly figure object
    """
    categories = list(probabilities.keys())  # Nama kategori (Sport, Finance)
    values = [probabilities[cat] * 100 for cat in categories]  # Konversi ke persen
    
    # Ambil warna dari config untuk setiap kategori
    colors = [COLOR_SCHEME.get(cat.lower(), COLOR_SCHEME['primary']) for cat in categories]
    
    # Buat horizontal bar chart
    fig = go.Figure(data=[
        go.Bar(
            y=categories,
            x=values,
            orientation='h',  # Horizontal
            marker=dict(
                color=colors,
                line=dict(color='rgba(0,0,0,0.2)', width=1)
            ),
            text=[f'{v:.1f}%' for v in values],  # Tampilkan persentase di bar
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
    Buat pie chart untuk statistik token
    Matched = kata yang ada di vocabulary model
    OOV (Out of Vocabulary) = kata yang tidak dikenali model
    
    Args:
        matched: Jumlah token yang ada di vocabulary
        oov: Jumlah token yang tidak dikenali (out-of-vocabulary)
        
    Returns:
        Plotly figure object (pie chart)
    """
    labels = ['Matched Vocabulary', 'Out of Vocabulary']
    values = [matched, oov]
    colors = [COLOR_SCHEME['secondary'], COLOR_SCHEME['sport']]
    
    # Buat pie chart
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors, line=dict(color='white', width=2)),
            textinfo='label+percent',  # Tampilkan label dan persentase
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
    Buat bar chart untuk menampilkan distribusi dataset training
    Menunjukkan berapa artikel Sport dan Finance yang digunakan untuk training
    
    Args:
        sport_count: Jumlah artikel sport (90)
        finance_count: Jumlah artikel finance (90)
        
    Returns:
        Plotly figure object (bar chart)
    """
    categories = ['Sport', 'Finance']
    counts = [sport_count, finance_count]
    colors = [COLOR_SCHEME['sport'], COLOR_SCHEME['finance']]
    
    # Buat vertical bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=counts,
            marker=dict(color=colors, line=dict(color='rgba(0,0,0,0.2)', width=1)),
            text=counts,  # Tampilkan angka di atas bar
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
