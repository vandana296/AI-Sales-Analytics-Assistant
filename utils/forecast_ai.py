from utils.gemini_helper import ask_gemini_simple


def generate_forecast_analysis(
    category,
    region,
    segment,
    quantity,
    discount,
    prediction
):

    prompt = f"""
You are a Senior Business Analyst.

Sales Forecast

Category: {category}
Region: {region}
Segment: {segment}
Quantity: {quantity}
Discount: {discount}
Predicted Sales: {prediction:.2f}

Generate:

1. Executive Summary

2. Business Insights

3. Risks

4. Recommendations

Keep response professional and concise.
"""

    return ask_gemini_simple(prompt)