import pandas as pd

def merge_proba(df):
    main_keywords = pd.read_json('front-end/keywords.json')
    df_result = df.merge(
        main_keywords,
        left_on='jobs',
        right_on='Title_final_category',
        how='inner').drop(columns=['Title_final_category'])
    return df_result.head(5)
