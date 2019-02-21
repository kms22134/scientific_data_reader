from pyhdf.HDF	import *
from pyhdf.SD 	import *
from pyhdf.VS 	import *

class Read_hdf(object):
    '''
    '''
   
    def __init__(self,f):
        '''
        '''
        
        self.file = f
        self._read_hdf_dataset()

    def _read_hdf_dataset(self):
        '''
        '''
        
        self.dataset  = SD(self.file,SDC.READ)
        self.dataKeys = self.dataset.datasets().keys()

    def _formatData(self,):
        '''
        '''
        
        fData = self.rawData.astype(float)
        fData[fData == self.attributes._FillValue] = self.attributes._FillValue
        fData = self.attributes.factor * (fData - self.attributes.offset)
        fData[(fData < min(self.attributes.valid_range)) | 
                (fData > max(self.attributes.valid_range))
             ] = self.attributes._FillValue

        fData[fData == self.attributes._FillValue] = nan

        return fData

    def read_var_sd(self,var):
        '''
        '''

        data = self.dataset.select(var)

        self.attributes = hdfATTRS(data.attributes())
        self.rawData    = data[:,]
        self.formatData = self._formatData()

    def read_var_vg(self,var):
        '''
        '''
        vSG1  = HDF(self.file,HC.READ)
        vs1   = vSG1.vstart()
        
        self.vgData = array(vs1.attach(var)[:,]).flatten()
