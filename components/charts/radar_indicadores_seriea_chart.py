# app/components/charts/radar_indicadores_chart.py
from streamlit_echarts import st_echarts
import streamlit as st
from constants.theme import get_theme_styles
from utils.data_extractor import (
    get_aproveitamento,
    get_media_pontos,
    get_classificacao_media,
    get_saldo_gols,
    get_gasto_medio,
    get_vitorias,
    get_derrotas,
    get_empates,
)


def render_kpi_radar_chart(
    df_clubes, df_bras, df_transf, clube_1: str, clube_2: str | None = None
):
    theme = get_theme_styles()

    def get_dados(clube):
        df_info = df_clubes[df_clubes["Nome Oficial"] == clube].iloc[0]
        df_bras_clube = df_bras[df_bras["Nome Oficial"] == clube]
        df_transf_clube = df_transf[df_transf["Nome Oficial"] == clube]

        return [
            round(get_aproveitamento(df_info), 2),
            get_vitorias(df_bras_clube),
            get_derrotas(df_bras_clube),
            get_empates(df_bras_clube),
            get_gasto_medio(df_transf_clube),
        ]

    metric_names = [
        "Aproveitamento (%)",
        "Vitórias",
        "Derrotas",
        "Empates",
        "Gasto Médio (R$)",
    ]

    vals1 = get_dados(clube_1)
    label1 = "\n".join(
        [clube_1] + [f"{metric_names[i]}: {vals1[i]}" for i in range(len(vals1))]
    )

    data = [
        {
            "value": vals1,
            "name": label1,
            "lineStyle": {"color": theme["CHART_PRIMARY_COLOR"]},
            "itemStyle": {"color": theme["CHART_PRIMARY_COLOR"]},
            "areaStyle": {"color": theme["CHART_PRIMARY_COLOR"], "opacity": 0.1},
        }
    ]

    if clube_2:
        vals2 = get_dados(clube_2)
        label2 = "\n".join(
            [clube_2] + [f"{metric_names[i]}: {vals2[i]}" for i in range(len(vals2))]
        )
        data.append(
            {
                "value": vals2,
                "name": label2,
                "lineStyle": {"color": theme["CHART_SECONDARY_COLOR"]},
                "itemStyle": {"color": theme["CHART_SECONDARY_COLOR"]},
                "areaStyle": {"color": theme["CHART_SECONDARY_COLOR"], "opacity": 0.1},
            }
        )

    labels = [
        {"name": "Aproveitamento (%)", "max": 100},
        {"name": "Vitórias", "max": 38},
        {"name": "Derrotas", "max": 38},
        {"name": "Empates", "max": 38},
        {"name": "Gasto Médio (R$)", "max": 6_500_000},
    ]

    options = {
        "title": {
            "text": "Indicadores Estratégicos",
            "textStyle": theme["CHART_TEXT_STYLE"],
        },
        "legend": [
            {
                "data": [label1],
                "icon": "circle",
                "itemStyle": {"color": theme["CHART_PRIMARY_COLOR"]},
                "orient": "horizontal",
                "left": "5%",
                "top": "12%",
                "textStyle": {
                    "color": theme["CHART_TEXT_STYLE"]["color"],
                    "fontSize": 14,
                    "lineHeight": 20,
                },
            },
            *(
                [
                    {
                        "data": [label2],
                        "icon": "circle",
                        "itemStyle": {"color": theme["CHART_SECONDARY_COLOR"]},
                        "orient": "horizontal",
                        "right": "5%",
                        "top": "12%",
                        "textStyle": {
                            "color": theme["CHART_TEXT_STYLE"]["color"],
                            "fontSize": 14,
                            "lineHeight": 20,
                        },
                    }
                ]
                if clube_2
                else []
            ),
        ],
        "radar": {
            "indicator": labels,
            "splitArea": {"areaStyle": {"color": theme["CHART_RADAR_BG"]}},
            "axisName": theme["CHART_AXIS_LABEL_STYLE"],
            "axisLine": theme["CHART_AXIS_LINE_STYLE"],
            "splitLine": {"lineStyle": {"color": theme["CHART_GRIDLINE_COLOR"]}},
            "center": ["50%", "50%"],
            "radius": "70%",
        },
        "series": [{"type": "radar", "data": data}],
    }

    st_echarts(options=options, height="500px")
