import tensorflow as tf
import pandas as pd
import pprint
import zipfile
dst = {}
class dictEval(object):
    
    def eval_dict(self,src):
        
        
        for key, value in src.items():
            if isinstance(value, dict):
                node = dst.setdefault(key, {})
                self.eval_dict(value)
            else:
                if "@lazy" not in key :
                    dst[key] = value
                else :
                    if 'pandas' in key :
                        key2 = key.split(":")[-1]
                        ext = value.split('.')[-1]
                        if ext == 'zip':
                            zf = zipfile.ZipFile(value)
                            dst[key2] = pd.read_csv(zf.open(src['filename']))
                        elif ext in ['csv','txt']:
                            dst[key2] = pd.read_csv(value)
                        elif ext == 'parquet':
                            dst[key2] = pd.read_parquet(value)
        return dst

test = dictEval()

dataset_url = 'http://storage.googleapis.com/download.tensorflow.org/data/petfinder-mini.zip'
csv_file    = 'datasets/petfinder-mini/petfinder-mini.csv'
zip_file = 'datasets/petfinder_mini.zip'
tf.keras.utils.get_file('petfinder_mini.zip', dataset_url,extract=True, cache_dir='.')

data_pars = {
    'train':{
        'filename':'petfinder-mini/petfinder-mini.csv',
        '@lazy_pandas:Xtrain':csv_file, #CSV file extraction
        '@lazy_pandas:Xtest':zip_file, #zip File Extraction
        '@lazy_tfdataset:Xtest':csv_file,
    },
    'pars': 23,
    
     "batch_size" : 5000,
    "n_train": 500, 
    "n_test": 500
}

dic = test.eval_dict(data_pars)
pprint.pprint(dic)