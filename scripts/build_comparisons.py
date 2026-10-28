"""Extract published comparison columns; never infer missing demographic years."""
from pathlib import Path
from pypdf import PdfReader
import json,re,hashlib
R=Path(__file__).resolve().parents[1]
name='2025+HOUSEHOLD+MAIL+SURVEY.pdf'
pdf=PdfReader(R/'reports'/name)
rows=[]
for page,table,dimension in [(18,'2.7','Age shares'),(52,'7.2','Packages by metro classification')]:
 text=pdf.pages[page-1].extract_text()
 (R/'data'/f'comparison-page-{page}.txt').write_text(text,encoding='utf8')
 block=text.split(f'Table {table}:')[-1].split('Source:')[0]
 for line in block.splitlines():
  if table=='2.7':
   m=re.match(r'^(Under 35|35-44|45-54|55-64|65-74|75 and Over)\s+'+r'\s+'.join([r'(\d+)%']*6),line)
   if m:
    for i,year in enumerate([2015,2020,2025]):
     for k,metric in enumerate(['Share of total mail','Share of households']):
      rows.append(dict(dimension=dimension,group=m[1],year=year,metric=metric,value=float(m[2+i*2+k]),unit='Percent',file=name,page=page,table=table,edition=2025))
  else:
   m=re.match(r'^(Large MSA|Other MSA|Non-MSA)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)',line)
   if m:
    for year,value in zip([2015,2020,2025],m.groups()[1:]):
     rows.append(dict(dimension=dimension,group=m[1],year=year,metric='Packages received',value=float(value),unit='Pieces per household per year',file=name,page=page,table=table,edition=2025))
assert len(rows)==45,len(rows)
(R/'data/demographic-history.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
# Archive the methodology pages used to substantiate the series break.
for page in [75,76,77,80]:
 (R/'data'/f'methodology-2025-page-{page}.txt').write_text(pdf.pages[page-1].extract_text(),encoding='utf8')
manifest=json.loads((R/'data/manifest.json').read_text())
p=R/'reports/USPS_HDS_FY11.pdf'
if p.exists() and not any(r['file']==p.name for r in manifest):
 reader=PdfReader(p)
 manifest.append(dict(year=2011,file=p.name,pages=len(reader.pages),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 (R/'data'/(p.name+'.txt')).write_text('\n'.join(f'--- PDF PAGE {i+1} ---\n'+(page.extract_text() or '') for i,page in enumerate(reader.pages[:25])),encoding='utf8')
 (R/'data/manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
print('45 published demographic comparison observations extracted.')
