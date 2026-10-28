from pathlib import Path
from pypdf import PdfReader
import zipfile, shutil, json, re
root=Path(__file__).resolve().parents[1]
(root/'reports').mkdir(exist_ok=True)
(root/'data').mkdir(exist_ok=True)
sources=[Path.home()/'Downloads',Path.home()/'Downloads'/'Python Bootcamp']
files=[]
for d in sources:
 for p in d.iterdir():
  if p.suffix.lower()=='.pdf' and any(s in p.name.lower() for s in ['household','hds','diary']):
   files.append((p.name,p.read_bytes()))
for name in ['2005_HDS.zip','2006_HDS.zip','2008_HDS.zip','62842.zip','Household+Diary_FY12.zip','Household+Diary+Study.zip']:
 p=sources[0]/name
 if p.exists():
  with zipfile.ZipFile(p) as z:
   for n in z.namelist():
    if n.lower().endswith('.pdf'): files.append((Path(n).name,z.read(n)))
seen=set(); manifest=[]
for name,b in files:
 import hashlib,io
 h=hashlib.sha256(b).hexdigest()
 if h in seen:continue
 seen.add(h)
 r=PdfReader(io.BytesIO(b))
 if len(r.pages)<30:continue
 dest=root/'reports'/name;dest.write_bytes(b)
 pages=[p.extract_text() or '' for p in r.pages[:25]]
 text='\n'.join(f'--- PDF PAGE {i+1} ---\n{t}' for i,t in enumerate(pages))
 (root/'data'/(name+'.txt')).write_text(text,encoding='utf8')
 years=re.findall(r'20\d{2}',name.replace('+',' '))
 if not years:
  m=re.search(r'FY[_ ]?(\d{2})',name,re.I)
  years=['20'+m[1]] if m else []
 year=int(years[0]) if years else None
 manifest.append(dict(year=year,file=name,pages=len(r.pages),sha256=h))
 print(name,year,len(r.pages),flush=True)
(root/'data'/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
