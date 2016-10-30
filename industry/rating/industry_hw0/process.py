import pandas
import json
import chardet

df = pandas.read_csv('industry_hw0', sep='\t')
values = sorted(df.mae)
bound_best = 0
bound_fst = values[-50]
bound_snd = values[-100]

df['industry/hw0'] = (df.mae <= bound_best) * 0.3 + (df.mae <= bound_fst) * 0.2 +  (df.mae <= bound_snd) * 0.2 + 0.3

del df['mae']

df.to_csv('industry_hw0.csv', index=False)

students = sorted(set(df.name))
with open('all_students.json', 'w') as f:
	json.dump(students, f, indent=4, ensure_ascii=False)
