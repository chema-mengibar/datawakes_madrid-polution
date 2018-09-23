# Python Issues

#### Normalization
https://stackoverflow.com/questions/26414913/normalize-columns-of-pandas-data-frame
```
one easy way by using Pandas: (here I want to use mean normalization)
>> normalized_df=(df-df.mean())/df.std()
to use min-max normalization:
>> normalized_df=(df-df.min())/(df.max()-df.min())
```
