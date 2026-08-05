from io import BytesIO
import streamlit as st


# ------------------------------------------
# CSV Download
# ------------------------------------------

def dataframe_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")


def download_chart_csv(df, filename="chart_data.csv"):

    st.download_button(
        label="📥 Download CSV",
        data=dataframe_to_csv(df),
        file_name=filename,
        mime="text/csv",
        use_container_width=True
    )


# ------------------------------------------
# HTML Download
# ------------------------------------------

def figure_to_html(fig):

    return fig.to_html(
        include_plotlyjs="cdn"
    )


def download_chart_html(fig, filename="chart.html"):

    st.download_button(
        label="🌐 Download HTML",
        data=figure_to_html(fig),
        file_name=filename,
        mime="text/html",
        use_container_width=True
    )


# ------------------------------------------
# PNG Download
# ------------------------------------------

def figure_to_png(fig):

    """
    Requires:
    pip install kaleido
    """

    buffer = BytesIO()

    fig.write_image(
        buffer,
        format="png",
        scale=2
    )

    buffer.seek(0)

    return buffer


def download_chart_png(fig, filename="chart.png"):

    st.download_button(
        label="🖼 Download PNG",
        data=figure_to_png(fig),
        file_name=filename,
        mime="image/png",
        use_container_width=True
    )