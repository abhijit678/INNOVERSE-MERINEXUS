import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Import backend modules
from data_generator import generate_mock_data
from analyzer import CognitiveAnalyzer
from recommender import RecommendationEngine
from report_generator import generate_report_data

# ----------------- Data Initialization ----------------- #
students_df, logs_df = generate_mock_data()
analyzer = CognitiveAnalyzer()
metrics_df = analyzer.analyze_all(students_df, logs_df)
recommender = RecommendationEngine()
recs_df = recommender.get_all_recommendations(metrics_df)
report_data = generate_report_data(students_df, logs_df, metrics_df)

# Global variables for styling
COLORS = {
    'bg': '#F8FAFC',           # Slate 50 (Very light background)
    'card': '#FFFFFF',         # White
    'border': '#E2E8F0',       # Slate 200 (Light border)
    'text': '#0F172A',         # Slate 900 (Dark text)
    'text_muted': '#64748B',   # Slate 500 (Muted text)
    'Cyan': '#0EA5E9',         # Sky Blue (Darker for light theme)
    'Green': '#10B981',        # Emerald (Darker for light theme)
    'Purple': '#8B5CF6',       # Violet (Darker for light theme)
    'Orange': '#F97316',       # Orange (Darker for light theme)
    'Red': '#EF4444',          # Red (Darker for light theme)
    'Yellow': '#EAB308'        # Yellow (Darker for light theme)
}

PATTERN_COLORS = {
    "Visual Learner": COLORS['Cyan'],
    "Analytical Thinker": COLORS['Purple'],
    "Kinesthetic Learner": COLORS['Green'],
    "Social Collaborator": COLORS['Orange'],
    "Mixed Learner": COLORS['Yellow']
}

EXTERNAL_STYLESHEETS = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
]

# ----------------- App Setup ----------------- #
app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS, suppress_callback_exceptions=True)
app.title = "CogniLearn AI"

app.index_string = f'''
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <style>
            body {{
                background-color: {COLORS['bg']};
                margin: 0;
                padding: 0;
                font-family: 'Inter', sans-serif;
            }}
        </style>
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
'''

# Common chart layout settings
def apply_chart_layout(fig):
    fig.update_layout(
        paper_bgcolor=COLORS['card'],
        plot_bgcolor=COLORS['card'],
        font={'family': "Inter, sans-serif", 'color': COLORS['text']},
        margin={'l': 40, 'r': 40, 't': 50, 'b': 40},
        xaxis={'showgrid': True, 'gridcolor': COLORS['border'], 'zeroline': False},
        yaxis={'showgrid': True, 'gridcolor': COLORS['border'], 'zeroline': False},
        colorway=[COLORS['Cyan'], COLORS['Purple'], COLORS['Green'], COLORS['Orange'], COLORS['Yellow']]
    )
    return fig

# ----------------- Layout Components ----------------- #
def create_kpi_card(title, value, subtitle="", style_overrides=None):
    return html.Div(
        style={
            'backgroundColor': COLORS['card'],
            'border': f"1px solid {COLORS['border']}",
            'borderRadius': '12px',
            'padding': '24px',
            'flex': '1',
            'margin': '12px',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
        } | (style_overrides or {}),
        children=[
            html.H4(title, style={'margin': '0 0 8px 0', 'color': COLORS['text_muted'], 'fontSize': '12px', 'textTransform': 'uppercase', 'letterSpacing': '0.05em', 'fontWeight': '600'}),
            html.H2(value, style={'margin': '0', 'fontSize': '32px', 'color': COLORS['text'], 'fontWeight': '700'}),
            html.Div(subtitle, style={'fontSize': '13px', 'color': COLORS['Cyan'], 'marginTop': '8px', 'fontWeight': '500'}) if subtitle else None
        ]
    )

app.layout = html.Div(
    style={
        'backgroundColor': COLORS['bg'],
        'color': COLORS['text'],
        'minHeight': '100vh',
        'padding': '40px 50px',
        'fontFamily': 'Inter, sans-serif'
    },
    children=[
        html.Div([
            html.H1(["Cogni", html.Span("Learn AI", style={'color': COLORS['Cyan']})], 
                    style={'margin': '0', 'fontSize': '36px', 'fontWeight': '700', 'letterSpacing': '-0.02em'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '40px'}),
        
        dcc.Tabs(
            id="tabs",
            value="tab-1",
            style={'marginBottom': '32px', 'display': 'flex', 'borderBottom': f'2px solid {COLORS["border"]}'},
            colors={
                "border": 'transparent',
                "primary": COLORS['Cyan'],
                "background": 'transparent'
            },
            children=[
                dcc.Tab(label="Overview", value="tab-1", 
                        style={'backgroundColor': 'transparent', 'color': COLORS['text_muted'], 'border': 'none', 'padding': '12px 24px', 'fontWeight': '500', 'fontSize': '15px'}, 
                        selected_style={'backgroundColor': 'transparent', 'color': COLORS['text'], 'border': 'none', 'borderBottom': f"3px solid {COLORS['Cyan']}", 'padding': '12px 24px', 'fontWeight': '600', 'fontSize': '15px'}),
                dcc.Tab(label="Pattern Analysis", value="tab-2", 
                        style={'backgroundColor': 'transparent', 'color': COLORS['text_muted'], 'border': 'none', 'padding': '12px 24px', 'fontWeight': '500', 'fontSize': '15px'}, 
                        selected_style={'backgroundColor': 'transparent', 'color': COLORS['text'], 'border': 'none', 'borderBottom': f"3px solid {COLORS['Cyan']}", 'padding': '12px 24px', 'fontWeight': '600', 'fontSize': '15px'}),
                dcc.Tab(label="Student Drill-Down", value="tab-3", 
                        style={'backgroundColor': 'transparent', 'color': COLORS['text_muted'], 'border': 'none', 'padding': '12px 24px', 'fontWeight': '500', 'fontSize': '15px'}, 
                        selected_style={'backgroundColor': 'transparent', 'color': COLORS['text'], 'border': 'none', 'borderBottom': f"3px solid {COLORS['Cyan']}", 'padding': '12px 24px', 'fontWeight': '600', 'fontSize': '15px'}),
                dcc.Tab(label="Recommendations", value="tab-4", 
                        style={'backgroundColor': 'transparent', 'color': COLORS['text_muted'], 'border': 'none', 'padding': '12px 24px', 'fontWeight': '500', 'fontSize': '15px'}, 
                        selected_style={'backgroundColor': 'transparent', 'color': COLORS['text'], 'border': 'none', 'borderBottom': f"3px solid {COLORS['Cyan']}", 'padding': '12px 24px', 'fontWeight': '600', 'fontSize': '15px'}),
                dcc.Tab(label="Analytics Report", value="tab-5", 
                        style={'backgroundColor': 'transparent', 'color': COLORS['text_muted'], 'border': 'none', 'padding': '12px 24px', 'fontWeight': '500', 'fontSize': '15px'}, 
                        selected_style={'backgroundColor': 'transparent', 'color': COLORS['text'], 'border': 'none', 'borderBottom': f"3px solid {COLORS['Cyan']}", 'padding': '12px 24px', 'fontWeight': '600', 'fontSize': '15px'}),
            ]
        ),
        
        html.Div(id="tab-content")
    ]
)

# ----------------- Tab Generators ----------------- #
def render_tab_1():
    avg_acc = f"{metrics_df['accuracy'].mean()*100:.1f}%"
    avg_rt = f"{metrics_df['avg_response_time'].mean():.1f}s"
    top_pattern = metrics_df['pattern'].mode()[0]
    avg_ret = f"{metrics_df['retention'].mean()*100:.1f}%"
    
    # Charts
    fig_hist = apply_chart_layout(px.histogram(metrics_df, x="accuracy", nbins=10, title="Accuracy Distribution", color_discrete_sequence=[COLORS['Cyan']]))
    fig_pie = apply_chart_layout(px.pie(metrics_df, names="pattern", title="Pattern Distribution", color="pattern", color_discrete_map=PATTERN_COLORS))
    fig_pie.update_traces(hole=0.4)
    fig_scatter = apply_chart_layout(px.scatter(metrics_df, x="avg_response_time", y="accuracy", color="pattern", title="Response Time vs Accuracy", color_discrete_map=PATTERN_COLORS, hover_data=['name']))
    
    # Line chart trend
    trend_df = logs_df.groupby('session')['score'].mean().reset_index()
    fig_line = apply_chart_layout(px.line(trend_df, x="session", y="score", title="Class Performance Trend", markers=True, color_discrete_sequence=[COLORS['Green']]))
    
    chart_style = {'flex': '1', 'margin': '12px', 'backgroundColor': COLORS['card'], 'borderRadius': '12px', 'border': f"1px solid {COLORS['border']}", 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'}

    return html.Div([
        html.Div([
            create_kpi_card("Avg Accuracy", avg_acc, "Overall Class Average"),
            create_kpi_card("Avg Response Time", avg_rt),
            create_kpi_card("Top Pattern", top_pattern),
            create_kpi_card("Avg Retention", avg_ret)
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '32px'}),
        
        html.Div([
            html.Div(dcc.Graph(figure=fig_hist), style=chart_style),
            html.Div(dcc.Graph(figure=fig_pie), style=chart_style)
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '24px'}),
        
        html.Div([
            html.Div(dcc.Graph(figure=fig_scatter), style=chart_style),
            html.Div(dcc.Graph(figure=fig_line), style=chart_style)
        ], style={'display': 'flex', 'flexWrap': 'wrap'})
    ])

def render_tab_2():
    # Radar chart
    categories = ['accuracy', 'avg_response_time', 'retry_rate', 'mistake_freq', 'retention']
    fig_radar = go.Figure()
    
    grouped_norm = metrics_df.groupby('pattern')[[f"{c}_norm" for c in categories]].mean().reset_index()
    for _, row in grouped_norm.iterrows():
        fig_radar.add_trace(go.Scatterpolar(
            r=row[[f"{c}_norm" for c in categories]].tolist(),
            theta=categories,
            fill='toself',
            name=row['pattern'],
            marker_color=PATTERN_COLORS.get(row['pattern'], COLORS['Cyan'])
        ))
    fig_radar.update_layout(
        polar={'radialaxis': {'visible': True, 'range': [0, 1], 'gridcolor': 'rgba(255,255,255,0.1)'}, 'bgcolor': 'rgba(0,0,0,0)'},
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': "Outfit", 'color': COLORS['text']},
        title="Pattern Metric Profiles (Normalized)",
        margin={'t': 60, 'b': 40, 'l': 40, 'r': 40}
    )
    
    # Box plots
    fig_box_acc = apply_chart_layout(px.box(metrics_df, x="pattern", y="accuracy", color="pattern", title="Accuracy by Pattern", color_discrete_map=PATTERN_COLORS))
    fig_box_rt = apply_chart_layout(px.box(metrics_df, x="pattern", y="avg_response_time", color="pattern", title="Response Time by Pattern", color_discrete_map=PATTERN_COLORS))
    
    # Heatmap
    heatmap_data = grouped_norm.set_index('pattern')
    fig_heat = apply_chart_layout(px.imshow(heatmap_data, labels={'x': "Metric", 'y': "Pattern", 'color': "Score"}, title="Pattern Attributes Heatmap", color_continuous_scale="Viridis", aspect="auto"))
    
    chart_style = {'flex': '1', 'margin': '12px', 'backgroundColor': COLORS['card'], 'border': f"1px solid {COLORS['border']}", 'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'}
    
    return html.Div([
        html.Div([
            html.Div(dcc.Graph(figure=fig_radar), style=chart_style),
            html.Div(dcc.Graph(figure=fig_heat), style=chart_style)
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '24px'}),
        
        html.Div([
            html.Div(dcc.Graph(figure=fig_box_acc), style=chart_style),
            html.Div(dcc.Graph(figure=fig_box_rt), style=chart_style)
        ], style={'display': 'flex', 'flexWrap': 'wrap'})
    ])

def render_tab_3():
    options = [{'label': f"{r['name']} ({r['pattern']})", 'value': r['student_id']} for _, r in metrics_df.iterrows()]
    
    return html.Div([
        html.Div([
            html.Label("Select Student:", style={'fontWeight': '600', 'marginRight': '15px', 'fontSize': '15px', 'color': COLORS['text_muted']}),
            dcc.Dropdown(
                id="student-select",
                options=options,
                value=options[0]['value'],
                style={'width': '350px', 'color': 'black', 'borderRadius': '8px'}
            )
        ], style={
            'marginBottom': '32px', 'padding': '24px', 'backgroundColor': COLORS['card'], 
            'borderRadius': '12px', 'border': f"1px solid {COLORS['border']}",
            'display': 'flex', 'alignItems': 'center',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
        }),
        
        html.Div(id="student-profile-content")
    ])

def render_tab_4():
    strategies = recommender.get_pattern_strategies()
    
    cards = []
    for pattern, strats in strategies.items():
        cards.append(html.Div(
            style={
                'backgroundColor': COLORS['card'], 
                'border': f"1px solid {PATTERN_COLORS.get(pattern, COLORS['border'])}", 
                'borderRadius': '12px', 'padding': '24px', 'margin': '12px', 'flex': '1', 'minWidth': '250px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
            },
            children=[
                html.H4(pattern, style={'color': PATTERN_COLORS.get(pattern, COLORS['Cyan']), 'marginTop': '0', 'fontSize': '18px', 'fontWeight': '600'}),
                html.Ul([html.Li(s, style={'fontSize': '14px', 'marginBottom': '10px', 'lineHeight': '1.5', 'color': COLORS['text']}) for s in strats])
            ]
        ))
        
    table_df = recs_df.copy()
    
    # Style condition for Priority
    style_cond = [
        {'if': {'filter_query': '{Priority} = "🔴 Critical"'}, 'backgroundColor': '#FEE2E2', 'color': '#B91C1C', 'fontWeight': '600'},
        {'if': {'filter_query': '{Priority} = "🟡 Moderate"'}, 'backgroundColor': '#FEF3C7', 'color': '#B45309', 'fontWeight': '600'},
        {'if': {'filter_query': '{Priority} = "🟢 On Track"'}, 'backgroundColor': '#D1FAE5', 'color': '#047857', 'fontWeight': '600'}
    ]
    
    table = dash_table.DataTable(
        data=table_df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in table_df.columns],
        sort_action='native',
        page_size=10,
        style_table={'overflowX': 'auto', 'borderRadius': '12px', 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'},
        style_header={'backgroundColor': COLORS['card'], 'color': COLORS['text_muted'], 'fontWeight': '600', 'fontFamily': 'Inter', 'borderBottom': f"2px solid {COLORS['border']}", 'padding': '16px'},
        style_cell={'backgroundColor': COLORS['bg'], 'color': COLORS['text'], 'fontFamily': 'Inter', 'padding': '16px', 'textAlign': 'left', 'border': f"1px solid {COLORS['border']}", 'fontSize': '14px'},
        style_data_conditional=style_cond
    )
    
    return html.Div([
        html.H3("Cognitive Pattern Strategies", style={'marginTop': '0', 'fontSize': '20px', 'fontWeight': '600', 'marginBottom': '20px'}),
        html.Div(cards, style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '48px'}),
        html.H3("Intervention Priority Table", style={'fontSize': '20px', 'fontWeight': '600', 'marginBottom': '20px'}),
        html.Div(table, style={'borderRadius': '12px', 'overflow': 'hidden'})
    ])

def render_tab_5():
    s = report_data['summary']
    
    fig_multi = apply_chart_layout(px.line(
        logs_df.merge(metrics_df[['student_id', 'pattern']], on='student_id').groupby(['pattern', 'session'])['score'].mean().reset_index(),
        x="session", y="score", color="pattern", title="Improvement Trajectory by Pattern", color_discrete_map=PATTERN_COLORS
    ))
    
    # Mock Funnel Data based on retention and risk
    funnel_data = pd.DataFrame([
        dict(stage="Enrolled", count=50),
        dict(stage="Active", count=48),
        dict(stage="Progressing", count=50 - s['at_risk_count']),
        dict(stage="Proficient", count=len(metrics_df[metrics_df['accuracy'] > 0.75])),
        dict(stage="Mastery", count=len(metrics_df[metrics_df['accuracy'] > 0.9]))
    ])
    fig_funnel = apply_chart_layout(px.funnel(funnel_data, x='count', y='stage', title="Student Learning Funnel"))
    fig_funnel.update_traces(marker=dict(color=COLORS['Cyan']))
    
    insights_list = html.Ul([
        html.Li(insight, style={'marginBottom': '15px', 'fontSize': '16px', 'lineHeight': '1.6'}) 
        for insight in report_data['insights']
    ])
    
    chart_style = {'flex': '1', 'margin': '12px', 'backgroundColor': COLORS['card'], 'borderRadius': '12px', 'border': f"1px solid {COLORS['border']}", 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'}
    
    return html.Div([
        html.Div([
            create_kpi_card("Total Sessions", s['total_sessions']),
            create_kpi_card("Avg Improvement", f"+{s['avg_improvement']:.1f}"),
            create_kpi_card("At-Risk Students", s['at_risk_count'], style_overrides={'border': f"1px solid {COLORS['Red']}", 'boxShadow': f'0 4px 6px {COLORS["Red"]}20'} if s['at_risk_count']>0 else {}),
            create_kpi_card("Top Performer", s['top_performer'])
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '32px'}),
        
        html.Div([
            html.Div(dcc.Graph(figure=fig_multi), style=chart_style),
            html.Div(dcc.Graph(figure=fig_funnel), style=chart_style)
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '24px'}),
        
        html.Div([
            html.H3("AI-Generated Insights", style={'color': COLORS['Cyan'], 'marginBottom': '16px', 'fontSize': '20px', 'fontWeight': '600'}),
            html.Div(insights_list, style={'backgroundColor': COLORS['card'], 'padding': '32px', 'borderRadius': '12px', 'border': f"1px solid {COLORS['border']}", 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'})
        ], style={'marginTop': '24px'})
    ])

# ----------------- Callbacks ----------------- #
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def render_content(tab):
    if tab == "tab-1":
        return render_tab_1()
    elif tab == "tab-2":
        return render_tab_2()
    elif tab == "tab-3":
        return render_tab_3()
    elif tab == "tab-4":
        return render_tab_4()
    elif tab == "tab-5":
        return render_tab_5()
    return html.Div("Unknown Tab")

@app.callback(
    Output("student-profile-content", "children"),
    Input("student-select", "value")
)
def update_student_profile(student_id):
    if not student_id:
        return html.Div()
        
    student = metrics_df[metrics_df['student_id'] == student_id].iloc[0]
    s_logs = logs_df[logs_df['student_id'] == student_id]
    
    pat_color = PATTERN_COLORS.get(student['pattern'], COLORS['Cyan'])
    
    banner = html.Div(style={
        'display': 'flex', 'alignItems': 'center', 'padding': '32px', 
        'backgroundColor': COLORS['card'], 'borderRadius': '12px', 
        'border': f"1px solid {COLORS['border']}", 'marginBottom': '32px',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
    }, children=[
        html.Div(student['name'][0], style={
            'width': '72px', 'height': '72px', 'borderRadius': '36px', 
            'backgroundColor': pat_color, 'color': COLORS['bg'], 
            'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 
            'fontSize': '32px', 'fontWeight': 'bold', 'marginRight': '24px'
        }),
        html.Div([
            html.H2(student['name'], style={'margin': '0 0 8px 0', 'fontSize': '28px', 'fontWeight': '600', 'color': COLORS['text']}),
            html.Div(f"Grade {student['grade']} • ", style={'display': 'inline', 'color': COLORS['text_muted'], 'fontSize': '15px'}),
            html.Span(student['pattern'], style={
                'backgroundColor': f"{pat_color}15", 'color': pat_color, 'border': f'1px solid {pat_color}40',
                'padding': '4px 12px', 'borderRadius': '16px', 'fontSize': '13px', 'fontWeight': '600', 'marginLeft': '8px'
            })
        ])
    ])
    
    kpis = html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '30px'}, children=[
        create_kpi_card("Accuracy", f"{student['accuracy']*100:.1f}%"),
        create_kpi_card("Response Time", f"{student['avg_response_time']:.1f}s"),
        create_kpi_card("Retry Rate", f"{student['retry_rate']*100:.1f}%"),
        create_kpi_card("Retention", f"{student['retention']*100:.1f}%")
    ])
    
    # Line+bar combo chart 
    fig_combo = make_subplots(specs=[[{"secondary_y": True}]])
    
    s_trend = s_logs.groupby('session').agg({'score':'mean', 'response_time':'mean'}).reset_index()
    
    fig_combo.add_trace(
        go.Bar(x=s_trend['session'], y=s_trend['response_time'], name="Response Time (s)", marker_color='rgba(255,255,255,0.1)'),
        secondary_y=False
    )
    fig_combo.add_trace(
        go.Scatter(x=s_trend['session'], y=s_trend['score'], name="Score", line={'color': pat_color, 'width': 4}, mode='lines+markers', marker={'size': 8, 'line': {'width': 2, 'color': COLORS['bg']}}),
        secondary_y=True
    )
    fig_combo.update_layout(title="Performance Over Time", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'family': "Outfit", 'color': COLORS['text']}, margin={'t': 60, 'b': 40, 'l': 40, 'r': 40})
    fig_combo.update_yaxes(title_text="Response Time /s", secondary_y=False, gridcolor='rgba(255,255,255,0.05)')
    fig_combo.update_yaxes(title_text="Score", secondary_y=True, gridcolor='rgba(0,0,0,0)')
    fig_combo.update_xaxes(gridcolor='rgba(255,255,255,0.05)')
    
    # Mistake frequency by subject
    mistakes = s_logs[s_logs['correct'] == 0].groupby('subject').size().reset_index(name='count')
    # Use empty if perfectly accurate to avoid errors
    if len(mistakes) == 0:
        fig_mistakes = apply_chart_layout(go.Figure().add_annotation(text="No mistakes recorded!", showarrow=False, font={'size': 20}))
    else:
        fig_mistakes = apply_chart_layout(px.bar(mistakes, x="subject", y="count", title="Mistakes by Subject", color_discrete_sequence=[COLORS['Red']]))
    
    chart_style = {'margin': '12px', 'backgroundColor': COLORS['card'], 'borderRadius': '12px', 'border': f"1px solid {COLORS['border']}", 'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'}
    
    charts = html.Div([
        html.Div(dcc.Graph(figure=fig_combo), style={'flex': '2'} | chart_style),
        html.Div(dcc.Graph(figure=fig_mistakes), style={'flex': '1'} | chart_style)
    ], style={'display': 'flex', 'flexWrap': 'wrap'})
    
    return html.Div([banner, kpis, charts])

if __name__ == "__main__":
    print(f"Starting CogniLearn AI dashboard at http://127.0.0.1:8050")
    app.run(debug=False, port=8050)
