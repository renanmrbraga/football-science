# app/components/charts/evolucao_brasileiro_chart.py
import streamlit as st
import json
from app.constants.theme import get_theme_styles  # Corrigido para importar a função

# Acessando os estilos do tema
theme = get_theme_styles()
CHART_TEXT_STYLE = theme["CHART_TEXT_STYLE"]
CHART_AXIS_LABEL_STYLE = theme["CHART_AXIS_LABEL_STYLE"]

def render_evolucao_brasileirao_chart(df_brasileirao_clube, chart_title: str) -> None:
    if df_brasileirao_clube.empty or "Ano" not in df_brasileirao_clube or "Posição" not in df_brasileirao_clube:
        st.warning("Dados insuficientes para exibir o gráfico de evolução no Brasileirão.")
        return

    df_sorted = df_brasileirao_clube.sort_values("Ano")
    anos = df_sorted["Ano"].astype(str).tolist()
    posicoes = df_sorted["Posição"].fillna(0).astype(int).tolist()

    chart_data = {
        "anos": anos,
        "posicoes": posicoes,
        "title": chart_title,
        "textColor": CHART_TEXT_STYLE["color"],
        "pointColor": "#00c6ff"  # cor azul da bolinha
    }

    container = f"""
    <div id="grafico-posicoes" style="width: 100%; height: 400px;"></div>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
    <script>
        var chart = echarts.init(document.getElementById('grafico-posicoes'));

        var option = {{
            title: {{
                text: {json.dumps(chart_data["title"])},
                textStyle: {{
                    color: '{chart_data["textColor"]}',
                    fontWeight: 'bold',
                    fontSize: 14
                }}
            }},
            tooltip: {{
                trigger: 'axis'
            }},
            xAxis: {{
                type: 'category',
                boundaryGap: false,
                data: {json.dumps(chart_data["anos"])},
                axisLabel: {{
                    color: '{chart_data["textColor"]}'
                }},
                axisLine: {{
                    lineStyle: {{ color: '{chart_data["textColor"]}' }}
                }}
            }},
            yAxis: {{
                type: 'value',
                inverse: true,
                min: 1,
                max: 20,
                interval: 1,
                axisLabel: {{
                    color: '{chart_data["textColor"]}',
                    formatter: function(value) {{
                        return [1,5,10,15,20].includes(value) ? value : '';
                    }}
                }},
                axisLine: {{
                    lineStyle: {{ color: '{chart_data["textColor"]}' }}
                }},
                splitLine: {{
                    lineStyle: {{ color: '#333' }}
                }}
            }},
            series: [{{
                data: {json.dumps(chart_data["posicoes"])},
                type: 'line',
                smooth: true,
                symbol: 'circle',
                symbolSize: 10,
                lineStyle: {{
                    width: 3,
                    color: '{chart_data["textColor"]}'
                }},
                itemStyle: {{
                    color: '{chart_data["pointColor"]}'
                }},
                areaStyle: {{
                    origin: 'end',  // CORREÇÃO: gradiente desce a partir do fim da linha
                    color: {{
                        type: 'linear',
                        x: 0, y: 0, x2: 0, y2: 1,
                        colorStops: [
                            {{ offset: 0, color: 'rgba(0,198,255,0.35)' }},
                            {{ offset: 1, color: 'rgba(0,114,255,0.05)' }}
                        ]
                    }}
                }}
            }}]
        }};

        chart.setOption(option);
    </script>
    """

    st.components.v1.html(container, height=500)
