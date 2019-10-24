from pandas.io.json import json_normalize

# Converts the input JSON to a DataFrame
def convertToDF(dfJSON):
    return (json_normalize(dfJSON))


# Converts the input DataFrame to JSON
def convertToJSON(df):
    resultJSON = df.to_json(orient='records')
    return (resultJSON)
