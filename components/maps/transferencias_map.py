# app/components/maps/transferencias_map.py
import streamlit as st
import json
from utils.geo import load_geojson
from utils.data import ensure_all_ufs
from constants.paths import GEOJSON_PATH
from constants.texts import WARNING_NO_UF_COLUMN
from constants.theme import get_theme_styles

def render_mapa_transferencias_chart(df_entrada, chart_title: str) -> None:
    # Carrega o GeoJSON do mapa
    geojson = load_geojson(GEOJSON_PATH)
    if not geojson or "UF" not in df_entrada.columns:
        st.warning(WARNING_NO_UF_COLUMN)
        return

    # Agrupa os dados por UF, garante que todas as UFs sejam exibidas e converte os valores para float
    df_map = df_entrada.groupby("UF")["Valor"].sum().reset_index()
    df_map.columns = ["UF", "Total_Gasto"]
    df_map = ensure_all_ufs(df_map, geojson)
    df_map["Total_Gasto"] = df_map["Total_Gasto"].astype(float)

    features = [
        {"name": row["UF"], "value": row["Total_Gasto"]}
        for _, row in df_map.iterrows()
    ]

    # Obtém os estilos do tema ativo
    theme = get_theme_styles()
    geojson_str = json.dumps(geojson)

    # Para o gradiente da visualMap, vamos inverter a ordem das cores definidas no tema.
    # Supondo que theme["GRADIENT_VERTICAL"] seja, por exemplo, ["#003366", "#e6f2ff"],
    # queremos que o gradiente no mapa seja: [ "#e6f2ff", "#003366" ]
    reversed_colors = [theme["GRADIENT_VERTICAL"][1], theme["GRADIENT_VERTICAL"][0]]
    
    register_and_render = f"""
    <div id="map" style="width: 100%; height: 550px;"></div>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.2/dist/echarts.min.js"></script>
    <script>
        // Inicializa o gráfico e registra o mapa
        var chart = echarts.init(document.getElementById('map'));
        echarts.registerMap('BR', {geojson_str});
        var option = {{
            title: {{
                text: '{chart_title}',
                left: 'center',
                textStyle: {{
                    color: '{theme["FOREGROUND_COLOR"]}',
                    fontWeight: 'bold',
                    fontSize: 18
                }}
            }},
            tooltip: {{
                trigger: 'item',
                backgroundColor: '{theme["TOOLTIP_BG"]}',
                borderColor: '{theme["PRIMARY_BLUE"]}',
                textStyle: {{
                    color: '{theme["TOOLTIP_TEXT"]}'
                }},
                formatter: function(params) {{
                    let valor = new Intl.NumberFormat('pt-BR', {{
                        style: 'currency',
                        currency: 'BRL'
                    }}).format(params.value || 0);
                    return params.name + ': ' + valor;
                }}
            }},
            visualMap: {{
                min: 0,
                max: {df_map["Total_Gasto"].max()},
                left: 'left',
                bottom: 'center',
                text: ['Maior', 'Menor'],
                calculable: true,
                inRange: {{
                    color: {json.dumps(reversed_colors)}
                }},
                textStyle: {{
                    color: '{theme["FOREGROUND_COLOR"]}',
                    fontSize: 13
                }},
                formatter: function(value) {{
                    let abs = Math.abs(value);
                    let abreviado = "";
                    if (abs >= 1e9) {{
                        abreviado = (value / 1e9).toFixed(1).replace('.', ',') + " B";
                    }} else if (abs >= 1e6) {{
                        abreviado = (value / 1e6).toFixed(1).replace('.', ',') + " M";
                    }} else if (abs >= 1e3) {{
                        abreviado = (value / 1e3).toFixed(1).replace('.', ',') + " K";
                    }} else {{
                        abreviado = value.toFixed(0);
                    }}
                    return 'R$ ' + abreviado;
                }}
            }},
            series: [{{
                type: 'map',
                map: 'BR',
                roam: true,
                emphasis: {{
                    label: {{
                        show: true,
                        color: '{theme["FOREGROUND_COLOR"]}',
                        fontWeight: 'bold'
                    }},
                    itemStyle: {{
                        areaColor: '{theme["HIGHLIGHT_COLOR"]}'
                    }}
                }},
                data: {json.dumps(features)}
            }}]
        }};
        chart.setOption(option);
    </script>
    """

    st.components.v1.html(register_and_render, height=580)
