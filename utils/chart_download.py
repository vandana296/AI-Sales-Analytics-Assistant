from io import BytesIO
import streamlit as st


# =========================================================
# CSV DOWNLOAD
# =========================================================

def dataframe_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")


def download_chart_csv(
    df,
    filename="chart_data.csv"
):

    st.download_button(
        label="📥 Download CSV",
        data=dataframe_to_csv(df),
        file_name=filename,
        mime="text/csv",
        use_container_width=True
    )


# =========================================================
# HTML DOWNLOAD
# =========================================================

def figure_to_html(fig):

    return fig.to_html(
        include_plotlyjs="cdn"
    )


def download_chart_html(
    fig,
    filename="chart.html"
):

    st.download_button(
        label="🌐 Download HTML",
        data=figure_to_html(fig),
        file_name=filename,
        mime="text/html",
        use_container_width=True
    )


# =========================================================
# PNG DOWNLOAD
# =========================================================

def figure_to_png(fig):

    try:

        buffer = BytesIO()

        fig.write_image(
            buffer,
            format="png",
            scale=2
        )

        buffer.seek(0)

        return buffer.getvalue()

    except Exception as e:

        st.error(
            "❌ PNG export is currently unavailable."
        )

        st.code(
            f"{type(e).__name__}: {str(e)}"
        )

        return None


def download_chart_png(
    fig,
    filename="chart.png"
):

    png_data = figure_to_png(fig)

    if png_data is not None:

        st.download_button(
            label="🖼 Download PNG",
            data=png_data,
            file_name=filename,
            mime="image/png",
            use_container_width=True
        )