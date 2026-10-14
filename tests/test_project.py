from pathlib import Path
import sys,unittest
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import project as p

class Tests(unittest.TestCase):
    def test_bh_known_values(self):
        np.testing.assert_allclose(p.bh([.01,.04,.03]),[.03,.04,.04])
    def test_pairing_required(self):
        c,m,g=p.demo_data();m=m.iloc[:-1];c=c[m.index]
        with self.assertRaises(AssertionError):p.validate((c,m,g))
    def test_sample_order_required(self):
        c,m,g=p.demo_data()
        with self.assertRaises(AssertionError):p.validate((c,m.iloc[::-1],g))
    def test_integer_counts_required(self):
        c,m,g=p.demo_data();c=c.astype(float);c.iloc[0,0]+=.5
        with self.assertRaises(AssertionError):p.validate((c,m,g))
    def test_demo_direction_and_label(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            result=p.differential(p.demo_data(),d)
        self.assertGreater(result.log2FoldChange.iloc[:30].median(),0)
        self.assertLess(result.log2FoldChange.iloc[30:60].median(),0)
        self.assertTrue(result.method.str.startswith('DEMO').all())
    def test_enrichment_universe_excludes_ambiguous_symbols(self):
        import tempfile
        from pathlib import Path
        result=pd.DataFrame({'gene_name':['g'+str(i) for i in range(20)]+['dup','dup'],
           'pvalue':[.01]*22,'padj':[.02]*22,'log2FoldChange':[2]*22})
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'sets.gmt';path.write_text('set\\turl\\t'+'\\t'.join('g'+str(i) for i in range(20)))
            # use literal tab-delimited GMT
            path.write_text(path.read_text().replace('\\t','\t'))
            out=p.enrich(result,path,d)
        self.assertEqual(out.background.iloc[0],20)

if __name__=='__main__':unittest.main()
