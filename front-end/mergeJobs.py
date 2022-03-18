import pandas as pd

def merge_proba(response):
    main_keywords = pd.read_json('front-end/new_keywords.json')
    df_result = pd.DataFrame()
    df_result['values'] = pd.Series(response['values'])
    df_result['jobs'] = pd.Series(response['jobs'])

    df_result = df_result.merge(
        main_keywords,
        left_on='jobs',
        right_on='Title_final_category',
        how='inner').drop(columns=['Title_final_category'])
    df_result = df_result[['values', 'jobs']]
    df_result = df_result.sort_values(by='values', ascending=False).head(5)
    return df_result
