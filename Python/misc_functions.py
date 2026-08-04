import config


def df_to_txt(df, start, end):
    output_df = df.iloc[start:end]
    feilds = config.extracted_fields
    
    output = "\n".join(
    f"{row.Rank}|{row.Word}|{row.Pronunciation}" 
    for _, row in output_df.iterrows()
    )
    return output