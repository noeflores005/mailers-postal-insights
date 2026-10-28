"""Build traceable annual data, demographics, forecasts and offline NLP evidence."""
from pathlib import Path
import json,re,math,csv,collections
R=Path(__file__).resolve().parents[1]
raw=json.loads((R/'data/markets.json').read_text())
annual={}
for row in sorted(raw,key=lambda x:x['edition']):
 if row['unit']=='Billions of pieces':annual[row['year'],row['market']]=row
annual=sorted(annual.values(),key=lambda r:(r['market'],r['year']))
demographics=[]
file='2025+HOUSEHOLD+MAIL+SURVEY.pdf'
text=(R/'data'/(file+'.txt')).read_text(encoding='utf8')
groups={'Age':('2.2',16),'Income':('2.3',16),'Education':('2.4',17),'Homeownership':('2.5',17),'Geography':('2.6',17)}
for dimension,(table,page) in groups.items():
 block=text.split(f'--- PDF PAGE {page} ---')[1].split('--- PDF PAGE')[0]
 block=block.split(f'Table {table}:')[-1].split('Source:')[0]
 for line in block.splitlines():
  m=re.match(r'^(.+?)\s+([\d.]+)\s+([\d.]+)\s+(\d+)%\s+(\d+)%\s*$',line)
  if m:demographics.append(dict(dimension=dimension,group=m[1],received=float(m[2]),sent=float(m[3]),mail_share=int(m[4]),household_share=int(m[5]),year=2025,file=file,page=page,table=table))
assert len(demographics)==19,len(demographics)

def predict(rows,model,h=1):
 vals=[r['value'] for r in rows];xs=[r['year'] for r in rows]
 if model=='Last observation':return vals[-1]
 n=len(vals);mx=sum(xs)/n;my=sum(vals)/n
 slope=sum((x-mx)*(y-my) for x,y in zip(xs,vals))/sum((x-mx)**2 for x in xs)
 if model=='Linear trend':return max(0,my+slope*(xs[-1]+h-mx))
 return max(0,vals[-1]+slope*sum(.8**i for i in range(1,h+1)))
forecasts={}
for market in sorted(set(r['market'] for r in annual)):
 if market=='Unclassified':continue
 rows=[r for r in annual if r['market']==market and 2015<=r['year']<=2023]
 if len(rows)<8:continue
 # Retrospective evaluation: historical estimates reflect later published revisions.
 models=['Last observation','Linear trend','Damped trend']
 validation={}
 for model in models:
  errors=[]
  for target in rows:
   train=[r for r in rows if r['year']<target['year']]
   if 2018<=target['year']<=2020 and len(train)>=3:errors.append(abs(predict(train,model)-target['value']))
  validation[model]=sum(errors)/len(errors)
 winner=min(validation,key=validation.get)
 holdout=[]
 for target in rows:
  if target['year']>=2021:
   train=[r for r in rows if r['year']<target['year']]
   holdout.append(dict(year=target['year'],actual=target['value'],prediction=round(predict(train,winner),4),baseline=round(predict(train,'Last observation'),4)))
 errors=[abs(d['actual']-d['prediction']) for d in holdout]
 mae=sum(errors)/len(errors);baseline=sum(abs(d['actual']-d['baseline']) for d in holdout)/len(holdout)
 band=max(errors)
 forecasts[market]=dict(model=winner,validation=validation,mae=mae,baseline_mae=baseline,holdout=holdout,training=rows,
  predictions=[dict(year=2023+h,value=round(predict(rows,winner,h),3),low=round(max(0,predict(rows,winner,h)-band*math.sqrt(h)),3),high=round(predict(rows,winner,h)+band*math.sqrt(h),3)) for h in range(1,8)])

# Extractive NLP: query-weighted TextRank on paragraphs from the 2025 report.
stop=set('the a an of to and in for is are was were by with as on that this from it at or be has have than their per mail household households'.split())
def tokens(s):return set(w for w in re.findall(r'[a-z]{3,}',s.lower()) if w not in stop)
passages=[]
for chunk in text.split('--- PDF PAGE ')[1:]:
 page=int(chunk.split(' ---')[0]);body=chunk.split('---',1)[1]
 lines=body.splitlines();paragraph=[]
 for line in lines+['']:
  line=line.strip()
  valid=len(line)>25 and not re.search(r'\.{4}|^Table |^Figure |^Source:|H O U S|C h a p|^\(',line) and sum(c.isalpha() for c in line)/max(1,len(line))>.65
  if valid:paragraph.append(line)
  else:
   p=' '.join(paragraph);paragraph=[]
   if 100<len(p)<1600:
    for sentence in re.split(r'(?<=[.!?])\s+(?=[A-Z])',p):
     if 90<len(sentence)<650 and len(tokens(sentence))>=8:passages.append(dict(text=sentence,page=page,file=file))
passages=passages[:300]
tok=[tokens(p['text']) for p in passages]
summaries={}
for topic in ['Overall mail usage','Correspondence','Transactions bills payments','Advertising marketing','Periodicals','Packages','Age demographics','Income','Homeownership']:
 q=tokens('decline growth volume received sent trends' if topic=='Overall mail usage' else topic)
 indices=[i for i,t in enumerate(tok) if t&q and passages[i]['page']>=7 and (re.search(r'\d',passages[i]['text']) or t&{'decline','increased','decreased','growth','changes'})]
 if not indices:indices=list(range(min(30,len(passages))))
 n=len(indices);weights=[[len(tok[i]&tok[j])/max(1,math.sqrt(len(tok[i])*len(tok[j]))) if i!=j else 0 for j in indices] for i in indices]
 scores=[1/n]*n
 for _ in range(25):
  sums=[sum(row) for row in weights]
  scores=[.15/n+.85*sum(scores[j]*weights[j][i]/sums[j] if sums[j] else scores[j]/n for j in range(n)) for i in range(n)]
 ranked=sorted(range(n),key=lambda k:scores[k]*(1+len(tok[indices[k]]&q)),reverse=True)
 chosen=[]
 for k in ranked:
  i=indices[k]
  if all(len(tok[i]&tok[j])/max(1,len(tok[i]|tok[j]))<.6 for j in chosen):chosen.append(i)
  if len(chosen)==3:break
 summaries[topic]=[passages[i] for i in chosen]

for forecast in forecasts.values():
 for point in forecast['predictions']:
  point['source_type']='model projection, not a published observation'
  point['sources']=[dict(file=r['file'],page=r['page'],year=r['year'],edition=r['edition']) for r in forecast['training']]
payload=dict(annual=annual,demographics=demographics,forecasts=forecasts,summaries=summaries,editions=raw,manifest=json.loads((R/'data/manifest.json').read_text()),demographicHistory=json.loads((R/'data/demographic-history.json').read_text()) if (R/'data/demographic-history.json').exists() else [])
(R/'data/submission.json').write_text(json.dumps(payload,indent=2),encoding='utf8')
(R/'data/dashboard-data.js').write_text('const DATA='+json.dumps(payload)+';',encoding='utf8')
for name,rows in [('annual',annual),('demographics',demographics)]:
 with (R/'data'/f'{name}.csv').open('w',newline='',encoding='utf8') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
print('Annual observations:',len(annual),'Demographic groups:',len(demographics),'Forecast markets:',len(forecasts),'NLP passages:',len(passages))
print('Total forecast:',json.dumps(forecasts['Total']))
