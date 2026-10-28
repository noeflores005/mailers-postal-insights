from pathlib import Path
import json,unittest,re
R=Path(__file__).resolve().parent;D=json.loads((R/'data/submission.json').read_text())
class DataTests(unittest.TestCase):
 def test_sources(self):
  for r in D['editions']+D['demographics']:self.assertTrue((R/'reports'/r['file']).is_file())
 def test_year_alignment(self):
  for edition,year,v in [(2019,2019,116.0),(2020,2020,104.4),(2017,2017,124.3),(2025,2025,637.3),(2024,2024,682.0)]:
   r=next(r for r in D['editions'] if r['edition']==edition and r['year']==year and r['market']=='Total');self.assertEqual(r['value'],v)
 def test_units(self):
  for r in D['editions']:self.assertEqual(r['unit'],'Pieces per household per year' if r['edition']>=2024 else 'Billions of pieces')
 def test_annual(self):
  rows=D['annual'];self.assertEqual(len(rows),len({(r['year'],r['market']) for r in rows}));self.assertEqual(len({r['year'] for r in rows}),21)
 def test_demographics(self):
  self.assertEqual(len(D['demographics']),19);self.assertEqual(next(r['received'] for r in D['demographics'] if r['group']=='Under 35'),346.9)
 def test_forecast(self):
  for f in D['forecasts'].values():
   self.assertEqual([r['year'] for r in f['holdout']],[2021,2022,2023]);self.assertAlmostEqual(f['mae'],sum(abs(r['actual']-r['prediction']) for r in f['holdout'])/3)
   for r in f['predictions']:self.assertTrue(0<=r['low']<=r['value']<=r['high'])
 def test_quotes(self):
  for passages in D['summaries'].values():
   for p in passages:
    original=(R/'data'/(p['file']+'.txt')).read_text(encoding='utf8');self.assertIn(re.sub(r'\s+',' ',p['text']),re.sub(r'\s+',' ',original))
if __name__=='__main__':unittest.main()
