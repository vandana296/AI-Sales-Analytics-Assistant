from io import BytesIO
from datetime import datetime

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.enums import TA_CENTER

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors


# --------------------------------------------------
# Dataset Summary PDF
# --------------------------------------------------

def generate_pdf_report(
    summary,
    total_sales,
    total_profit,
    total_orders,
    profit_margin
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    # Title

    story.append(
        Paragraph(
            "AI Business Intelligence Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    # KPI Section

    story.append(
        Paragraph(
            "<b>Business KPIs</b>",
            styles["Heading2"]
        )
    )

    data = [
        ["Metric", "Value"],
        ["Total Sales", f"${total_sales:,.2f}"],
        ["Total Profit", f"${total_profit:,.2f}"],
        ["Total Orders", str(total_orders)],
        ["Profit Margin", f"{profit_margin:.2f}%"]
    ]

    table = Table(data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 10)

        ])

    )

    story.append(table)

    story.append(Spacer(1, 20))

    # Dataset Summary

    story.append(

        Paragraph(

            "<b>Dataset Summary</b>",

            styles["Heading2"]

        )

    )

    for key, value in summary.items():

        story.append(

            Paragraph(

                f"<b>{key}</b>: {value}",

                styles["Normal"]

            )

        )

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf


# --------------------------------------------------
# AI Executive Report PDF
# --------------------------------------------------

def generate_ai_report_pdf(

    title,

    report,

    kpis=None

):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(

        "CenteredTitle",

        parent=styles["Title"],

        alignment=TA_CENTER

    )

    story = []

    # Title

    story.append(

        Paragraph(

            title,

            title_style

        )

    )

    story.append(Spacer(1, 12))

    # Date

    story.append(

        Paragraph(

            f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}",

            styles["Normal"]

        )

    )

    story.append(Spacer(1, 20))

    # KPIs

    if kpis:

        story.append(

            Paragraph(

                "<b>Business KPIs</b>",

                styles["Heading2"]

            )

        )

        table_data = [["Metric", "Value"]]

        for key, value in kpis.items():

            table_data.append([key, str(value)])

        table = Table(table_data)

        table.setStyle(

            TableStyle([

                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 10)

            ])

        )

        story.append(table)

        story.append(Spacer(1, 20))

    # AI Report

    story.append(

        Paragraph(

            "<b>AI Executive Report</b>",

            styles["Heading2"]

        )

    )

    report = report.replace("###", "")

    report = report.replace("##", "")

    report = report.replace("#", "")

    report = report.replace("**", "")

    report = report.replace("*", "• ")

    for line in report.split("\n"):

        line = line.strip()

        if line == "":

            continue

        story.append(

            Paragraph(

                line,

                styles["Normal"]

            )

        )

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf