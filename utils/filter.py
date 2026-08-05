def apply_filters(df, region, category, segment):

    filtered = df.copy()

    if region != "All":
        filtered = filtered[filtered["Region"] == region]

    if category != "All":
        filtered = filtered[filtered["Category"] == category]

    if segment != "All":
        filtered = filtered[filtered["Segment"] == segment]

    return filtered