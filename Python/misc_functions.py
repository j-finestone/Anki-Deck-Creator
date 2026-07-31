def df_to_txt(df, start, end):
    output_df = df.iloc[start:end]
    output = "\n".join(
    f"{row.Rank}|{row.Word}" 
    for _, row in output_df.iterrows()
    )
    return output