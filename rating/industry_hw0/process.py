import pandas
import json
import chardet

df = pandas.read_csv('industry_hw0', sep='\t')
df.mae = map(lambda x: float(x.replace(',', '.')), df.mae)
values = sorted(df.mae)
bound_best = 0.0
bound_fst = values[-50]
bound_snd = values[-100]

df['industry/hw0'] = (df.mae <= bound_best) * 0.3 + (df.mae <= bound_fst) * 0.2 +  (df.mae <= bound_snd) * 0.2 + 0.3

del df['mae']

df.to_csv('industry_hw0.csv', index=False)
