"""Extract Table E.2 while retaining each report's edition and source context."""
from pathlib import Path
import json,re,csv
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'data/manifest.json').read_text())
records=[]
for item in manifest:
 if item['year'] is None or 'ApxC' in item['file'] or '_Screen' in item['file']:continue
 text=(ROOT/'data'/(item['file']+'.txt')).read_text(encoding='utf8')
 lines=text.splitlines()
 for i,line in enumerate(lines):
  if not re.match(r'^Correspondence\s+\d',line):continue
  headers=[l for l in lines[max(0,i-12):i] if re.match(r'^Market\s+20\d{2}',l)]
  if not headers:continue
  yrs=re.findall(r'\b20\d{2}\b',headers[-1])
  if len(yrs)<3:continue
  yrs=list(map(int,yrs[:3]))
  if len(set(yrs))!=3:continue
  block=lines[i:i+8]
  page=int(re.findall(r'--- PDF PAGE (\d+) ---','\n'.join(lines[:i]))[-1])
  for row in block:
   m=re.match(r'^(Correspondence|Transactions|Advertising|Periodicals|Packages|Unclassified|Other|Total)\*?\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)',row)
   if not m:continue
   for yr,val in zip(yrs,m.groups()[1:]):
    records.append(dict(year=yr,edition=item['year'],market=m[1],value=float(val.replace(',','')),unit='Pieces per household per year' if item['year']>=2024 else 'Billions of pieces',file=item['file'],page=page,table='E.2',notes=' '.join(lines[i+7:i+22])))
  break
assert len(records)>200, len(records)
assert all(r['value']>=0 and 2000<=r['year']<=r['edition'] for r in records)
(ROOT/'data/markets.json').write_text(json.dumps(records,indent=2),encoding='utf8')
with (ROOT/'data/markets.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=records[0]);w.writeheader();w.writerows(records)
print(len(records),'observations;',len(set(r['edition'] for r in records)),'report editions')
