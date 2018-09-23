# Python Pandas

---

**Max values**
```py
data.groupby(['Country','Place'])['Price'].max()
```
```py
df.loc[df['Value'].idxmax()]
```
---

** Boolean / Logical indexing: Value Condition Selection**
```py
df.loc[df['column_name'] == some_value]
```
```py
#To select rows whose column value is in an iterable
df.loc[df['column_name'].isin(some_values)]
```
```py
# Multiple conditions
df.loc[ (df['column_name'] == some_value) & (df['other_column'].isin(some_values)) ]
```
```py
# select rows whose value is not in some_values
df.loc[~df['column_name'].isin(some_values)]
```
---

** Row, Column selection**
```py
data.iloc[0] # first row
data.iloc[-1] # last row
data.iloc[:,0] # first column
data.iloc[:,-1] # last column
data.iloc[0:5] # first five
data.iloc[:, 0:2] # first two columns
data.iloc[[0,3,6,24], [0,5,6]] # 1st, 4th, 7th, 25th row
```
```py
# Select rows with index values 'Andrade' and 'Veness', with all columns between 'city' and 'email'
data.loc[['Andrade', 'Veness'], 'city':'email']
```
```py
# Change the index to be based on the 'id' column
data.set_index('id', inplace=True)
# select the row with 'id' = 487
data.loc[487]
```

** Change value **
```py
# Change the first name of all rows with an ID greater than 2000 to "John"
data.loc[data['id'] > 2000, "first_name"] = "John"
```
