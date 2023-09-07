
import sys
sys.path.append("../Database/")

from STMdatabase import STMimage
import matplotlib.pyplot as plt
import pySPM
import pandas as pd
from IPython.display import HTML, display
from scipy.ndimage import gaussian_filter
import numpy as np
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar

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


    def display_meta_data(self):
        imageInfo=self.get_data_info()
        df=pd.DataFrame(list(imageInfo.items()),columns=["Name","Value"])
        html_pd=df.to_html()
        display(HTML(html_pd))


    def correct_line(self,channel="Z_forward"):
        image=self.get_image_value(channel=channel)
        Z_image= pySPM.SPM_image(image)
        Z_image.correct_median_diff()
        Z_image.correct_lines()
        return Z_image.pixels



    def display_topo(self,fig,ax,channel="Z_forward",imagetitle="SiC",sig=None,isaxis=False,isbar=True,scalecolor="white",scalesize=0.3,cmap="Blues_r",iscolorbar=True,iscorrect=True,isgauss=True,sigma=1):
        if iscorrect:
            image=self.correct_line(channel=channel)
        else:
            image=self.get_image_value(channel=channel)

        if isgauss:
            image=gaussian_filter(image,sigma=sigma)
        posX,posY=self.get_pos()
        [x_p,y_p]=self.get_pix()
        [x_n,y_n]=self.get_image_size()
        
        Z_image= pySPM.SPM_image(image[::,::])
        Z_image.size["real"]["x"],Z_image.size["real"]["y"]=x_n*1e-9,y_n*1e-9
        Z_image.size["pixels"]["y"],Z_image.size["pixels"]["x"]=y_p,x_p
        #img=Z_image.show(ax=ax,sig=sig,cmap=cmap)
        img=ax.imshow(image,cmap=cmap)
        if not isaxis:
            ax.axis ('off')

        if iscolorbar:
            Vmin=np.ndarray.min(image) 
            Vmax=np.ndarray.max(image) 
            cb=fig.colorbar(img,ax=ax,orientation="vertical",pad=0.02,shrink=0.8) 
            cb.ax.yaxis.set_tick_params(size=0.8,labeltop=True) 
            cb.set_ticks([Vmax,Vmin])
            cb.set_ticklabels(["High","Low"])
        
        if isbar:
            scale=int(x_n/10) 
            scalebar=AnchoredSizeBar(ax.transData,scale*2,"{0} nm".format(scale*2),"lower right",pad=1,sep=3,color=scalecolor,label_top=True,frameon=False,size_vertical=scalesize)
            ax.add_artist(scalebar)
        if imagetitle!="":
            ax.set_title(imagetitle) 
        return img


    


    
    
        
