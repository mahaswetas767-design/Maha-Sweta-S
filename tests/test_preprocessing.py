import pandas as pd
def test_duplicate_detection():
    df=pd.DataFrame({"x":[1,1,2]})
    assert len(df.drop_duplicates())==2
