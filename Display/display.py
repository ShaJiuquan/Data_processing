
import sys
sys.path.append("../Database_Management/")
from STMdatabase import STMimage
import matplotlib.pyplot as plt


class STMimagePlot(STMimage):

    def __init__(self,filePath: str,dataseName="../../STMdata.db"):
        super().__init__(filePath,dataseName)


    def plot(self,channel=None):
        if channel==None:
            image_forward=self.get_image_value(channel="Z_forward")
            image_back=self.get_image_value(channel="Z_backward")
            fig,ax=plt.subplots(1,2,figsize=(14,7))
            ax[0].imshow(image_forward)
            ax[1].imshow(image_back[:,::-1])
        else:
            image=self.get_image_value(channel=channel)
            fig,ax=plt.subplots(1,1,figsize=(7,7))
            ax.imshow(image)


    
    
        
