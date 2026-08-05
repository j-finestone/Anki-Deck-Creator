import config
import re
from pypinyin import lazy_pinyin, Style


def df_to_txt(df, start, end):
    output_df = df.iloc[start:end]
    feilds = config.extracted_fields
    
    output = "\n".join(
    f"{row.Rank}|{row.Word}|{row.Pronunciation}" 
    for _, row in output_df.iterrows()
    )
    return output



#Adding pinyin with Ruby
CJK_PATTERN = re.compile(r'[\u4e00-\u9fff]+')

def hanzi_to_ruby(hanzi_run):
    """Convert a run of Hanzi into per-character ruby HTML."""
    syllables = lazy_pinyin(hanzi_run, style=Style.TONE, tone_sandhi=True)
    return "".join(
        f"<ruby>{char}<rt>{syll}</rt></ruby>"
        for char, syll in zip(hanzi_run, syllables)
    )


def add_ruby(text):
    """Replace every Hanzi run in a string with ruby-annotated HTML.
    Leaves everything else (English, punctuation) untouched."""
    if not text:
        return text
    return CJK_PATTERN.sub(lambda m: hanzi_to_ruby(m.group(0)), text)


