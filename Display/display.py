
import sys
sys.path.append("../Database/")

from STMdatabase import STMimage
import matplotlib.pyplot as plt
import pySPM


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
        pass


    def display_topo(image,fig,ax,x_n,y_n,title="SiC",isaxis=False,isbar=True,scalecolor="white",scalesize=0.3,cmap="Blues_r"):
        #image=gaussian_filter(image,sigma=1)
        Z_image= pySPM.SPM_image(image)
        Z_image.correct_median_diff()
        Z_image.correct_lines()
        (y_p,x_p)=image.shape
        Z_image.size["real"]["x"],Z_image.size["real"]["y"]=x_n*1e-9,y_n*1e-9
        Z_image.size["pixels"]["y"],Z_image.size["pixels"]["x"]=y_p,x_p
        img=Z_image.show(ax=ax,sig=None,cmap=cmap)
        if not isaxis:
            ax.axis ('off')
        Vmin=np.ndarray.min(Z_image.pixels) 
        Vmax=np.ndarray.max(Z_image.pixels) 
        cb=fig.colorbar(img,ax=ax,orientation="vertical",pad=0.02,shrink=0.8) 
        cb.ax.yaxis.set_tick_params(size=0.8,labeltop=True) 
        cb.set_ticks([Vmax,Vmin])
        cb.set_ticklabels(["High","Low"])
        scale=int(x_n/10) 
        scalebar=AnchoredSizeBar(ax.transData,scale*2,"{0} nm".format(scale*2),"lower right",pad=1,sep=3,color=scalecolor,label_top=True,frameon=False,size_vertical=scalesize)
        if isbar:
            ax.add_artist(scalebar)
        ax.set_title(title) 
        return img


    


    
    
        
