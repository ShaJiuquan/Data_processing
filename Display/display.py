
import sys
sys.path.append("../Database/")

from STMdatabase import STMimage,STMspec,STMgrid
import matplotlib.pyplot as plt
import pySPM
import pandas as pd
from IPython.display import HTML, display
from scipy.ndimage import gaussian_filter
import numpy as np
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from scipy.fft import fftshift, fft2,ifftshift,ifft2
from scipy.signal import hann
from math import pi


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


    def correct_line_median(self,channel="Z_forward"):
        image=self.get_image_value(channel=channel)
        Z_image= pySPM.SPM_image(image)
        Z_image.correct_median_diff()
        Z_image.correct_lines()
        return Z_image.pixels
    
    def my_FFT(self,image,isnormalize=False):
        [x_p,_]=self.get_pix()
        if isnormalize:
            image=(image-image.min())/(image.max()-image.min())
        window_hann = image * hann(x_p, sym=True)
        ft = np.fft.fftshift(np.fft.fft2(window_hann))
        power_spectrum = np.abs(ft) ** 2
        if isnormalize:
            return (power_spectrum-power_spectrum.min())/(power_spectrum.max()-power_spectrum.min())
        else:
            return power_spectrum
        

    def my_iFFT(self,img):
        ifftshift(img)
        x_p=img.shape[0]
        image_bw=(img-img.min())/(img.max()-img.min())
        image_bw=img
        window_hann = image_bw * hann(x_p, sym=True)
        ft = np.fft.fftshift(np.fft.fft2(window_hann))
        power_spectrum = np.abs(ft) ** 2
        #return (power_spectrum-power_spectrum.min())/(power_spectrum.max()-power_spectrum.min())
        return ft.real
    
    def display_FT(self,fig,ax,channel="Z_forward",Z_factor=0.8,title="FT image",sig=None,isnormolize=True,isaxis=False,isscalebar=True,scalecolor="white",scalesize=0.3,cmap="Blues_r",iscolorbar=True,iscorrect=True,isgauss=True,sigma=1):
        if iscorrect:
            image=self.correct_line_median(channel=channel)
        else:
            image=self.get_image_value(channel=channel)

        if isgauss:
            image=gaussian_filter(image,sigma=sigma)
        Z_fft=self.my_FFT(image=image)
        posX,posY=self.get_pos()
        [x_p,y_p]=self.get_pix()
        [x_n,y_n]=self.get_image_size()
        zoomValue=int(x_p*Z_factor)
        d=x_n/zoomValue #Sample spacing 
        y_freq=np.fft.fftshift(np.fft.fftfreq(y_p,d)) 
        x_freq=np.fft.fftshift(np.fft.fftfreq(x_p,d)) 
        extent=[x_freq[0],x_freq[-1],y_freq[0],y_freq[-1]]
        Z_fft=pySPM.zoom_center(Z_fft, sx=zoomValue, sy=zoomValue) 
        scalebar=AnchoredSizeBar(ax.transData,1/0.438/1.731,r'$1/3a^{-1}$',"lower right",pad=1,sep=3,color="black",label_top=True,frameon=False,size_vertical=scalesize)
        if isscalebar:
            ax.add_artist(scalebar)
        if not isaxis:
            ax.axis("off")
        x=r'$q_x/2\pi$ $(nm^{-1})$'
        y=r'$q_y/2\pi$ $(nm^{-1})$'
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_title("The FFT image of kagome lattice") 
        if isnormolize:
            min_val = np.min(Z_fft)
            max_val = np.max(Z_fft)
            Z_fft = (Z_fft - min_val) / (max_val - min_val)
            if sig !=None and sig>0 and sig<1:
                Z_fft[Z_fft>sig]=sig
                Z_fft[Z_fft<1-sig]=1-sig
        img=ax.imshow(Z_fft,origin="lower",extent=extent,cmap=cmap)
        Vmin=np.ndarray.min(Z_fft) 
        Vmax=np.ndarray.max(Z_fft) 
        if iscolorbar:
            cb=fig.colorbar(img,ax=ax,orientation="vertical",pad=0.02,shrink=0.8) 
            cb.ax.yaxis.set_tick_params(size=0.8,labeltop=True) 
            cb.set_ticks([Vmax,Vmin])
            cb.set_ticklabels(["High","Low"])
        ax.set_title(title)

    def Rotate_v(self,theta, v):
        theta = theta/180*pi
        rotation_matrix = np.zeros((2, 2)) 
        rotation_matrix[0, 0] = np.cos(theta) 
        rotation_matrix[1, 1] = np.cos(theta) 
        rotation_matrix[0, 1] = -np.sin(theta) 
        rotation_matrix[1, 0] = np.sin(theta) 
        return np.dot(rotation_matrix,v)
    
    def plot_arrow(self,ax,pos,shift=(0,0),color="green",text=r"$Q_{\sqrt{3}*\sqrt{3}R30^0}$"): 
        ax.arrow(shift[0],shift[1],pos[0],pos[1],width=0.02,ec=color,head_length=0.1,length_includes_head=True) 
        circleArray=[]
        c1=(pos[0],pos[1]) 
        c1=self.Rotate_v(-0,c1) 
        for i in range(6):
            c=self.Rotate_v(60,c1)
            circleArray.append(c)
            c1=c
        for circleP in circleArray: 
            circle=plt.Circle(circleP,0.08,color=color,fill=False) 
            ax.add_patch(circle)
        pos = [pos[0]*1.1,pos[1]]
        ax.text(pos[0],pos[1],text,color=color)

    



    def display_topo(self,fig,ax,channel="Z_forward",imagetitle="SiC",sig=None,isnormolize=True,isaxis=False,isscalebar=True,scalecolor="white",scalesize=0.3,cmap="Blues_r",iscolorbar=True,iscorrect=True,isgauss=True,sigma=1,zorder=0):
        if iscorrect:
            image=self.correct_line_median(channel=channel)
        else:
            image=self.get_image_value(channel=channel)

        if isgauss:
            image=gaussian_filter(image,sigma=sigma)
        posX,posY=self.get_pos()
        image_range=self.get_image_range()
        [x_p,y_p]=self.get_pix()
        [x_n,y_n]=self.get_image_size()
        
        if isnormolize:
            min_val = np.min(image)
            max_val = np.max(image)
            image = (image - min_val) / (max_val - min_val)
            if sig !=None and sig>0 and sig<1:
                image[image>sig]=sig
                image[image<1-sig]=1-sig

        img=ax.imshow(image[::,::],cmap=cmap,origin="upper",extent=image_range,zorder=zorder)
        if not isaxis:
            ax.axis ('off')

        if iscolorbar:
            Vmin=np.ndarray.min(image) 
            Vmax=np.ndarray.max(image) 
            cb=fig.colorbar(img,ax=ax,orientation="vertical",pad=0.02,shrink=0.8) 
            cb.ax.yaxis.set_tick_params(size=0.8,labeltop=True) 
            cb.set_ticks([Vmax,Vmin])
            cb.set_ticklabels(["High","Low"])
        
        if isscalebar:
            factor=x_p/x_n
            scale=int(x_n/5)
            scalebar=AnchoredSizeBar(ax.transData,scale,"{0} nm".format(scale),"lower right",pad=1,sep=3,color=scalecolor,label_top=True,frameon=False,size_vertical=scalesize)
            ax.add_artist(scalebar)
        if imagetitle!="":
            ax.set_title(imagetitle) 

            
class STMspecPlot(STMspec):
    def __init__(self,filePath: str,dataseName="../../STMdata.db"):
        super().__init__(filePath,dataseName)
    def plot(self,channel=None):
        if channel==None:
            bias,curr_forward=self.get_spec_value(channel="Current_forward")
            bias,spec_forward=self.get_spec_value(channel="LIY_1_omega_forward")
            fig,ax=plt.subplots(1,2,figsize=(14,7))
            ax[0].plot(bias,spec_forward,"-r")
            ax[1].plot(bias,curr_forward)
        else:
            bias,spec=self.get_spec_value(channel=channel)
            fig,ax=plt.subplots(1,1,figsize=(7,7))
            ax.plot(bias,spec)
    def display_meta_data(self):
        specInfo=self.get_data_info()
        df=pd.DataFrame(list(specInfo.items()),columns=["Name","Value"])
        html_pd=df.to_html()
        display(HTML(html_pd))

    def display_single_spec(self,fig,ax,channel="LIY_1_omega_forward",biasvalue=0.1,isnormolize=True,offset=3e-12,isgauss=True,sigma=1,color="r",spectitle="",isline=False,islegend=True):
        bias,spec=self.get_spec_value(channel=channel)
        pos=self.get_pos()
        if isnormolize:
            min_val = np.min(spec)
            max_val = np.max(spec)
            spec= (spec - min_val) / (max_val - min_val)
        if isgauss:
            spec=gaussian_filter(spec,sigma=sigma)
        if isline:
            point_per_bias=abs(bias[-1]-bias[0])/spec.shape[-1]
            bias_point=int((biasvalue-bias[0])/point_per_bias)
            line=ax.vlines(biasvalue,ymin=0,ymax=spec.max())
        spec=spec+offset
        ax.plot(bias,spec,label=r"$dI/dV$ ($a.u.$)",color=color)
        xlabel="Sample bias (V)"
        ylabel=r"$dI/dV$ ($a.u.$)"
        title=r"The $STS$ of selected point: {0}".format(pos)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.xaxis.get_label().set_fontsize(18)
        ax.yaxis.get_label().set_fontsize(18)
        ax.tick_params(axis='y', labelsize=14)
        ax.tick_params(axis='x', labelsize=14)
        if islegend:
            ax.legend()
        ax.set_title(title,fontsize=18)
        if spectitle!="":
            ax.set_title(spectitle) 
        else:
            ax.set_title(title) 


class STMgridPlot(STMgrid):
    def __init__(self,filePath: str,dataseName="../../STMdata.db"):
        super().__init__(filePath,dataseName)
    def plot(self,channel=None):
        if channel==None:
            bias,grid=self.get_grid_value(channel="LIY_1_omega")
            fig,ax=plt.subplots(1,2,figsize=(14,7))
            ax[0].plot(bias,grid[0][0],"-r")
            ax[1].imshow(grid[::,::,1],"Blues_r",origin="lower")
            
        else:
            bias,grid=self.get_grid_value(channel=channel)
            fig,ax=plt.subplots(1,2,figsize=(14,7))
            ax[0].plot(bias,grid[0][0],"-r")
            ax[1].imshow(grid[::,::,1],"-r")
    def display_meta_data(self):
        specGrid=self.get_data_info()
        df=pd.DataFrame(list(specGrid.items()),columns=["Name","Value"])
        html_pd=df.to_html()
        display(HTML(html_pd))

    def correct_line_median(self,image):
        Z_image= pySPM.SPM_image(image)
        Z_image.correct_median_diff()
        Z_image.correct_lines()
        return Z_image.pixels
    
    def plot_STS_line_spectrum(self,ax,line,channel="LIY_1_omega",offset=3e-13,color="C3",unit=1e11,lines=[],colorA=["r",'coral',"peachpuff","lightskyblue","royalblue","k",'coral',"grey","yellow"]):
    
        xlabel="Sample bias (V)"
        ylabel=r"$dI/dV$ ($a.u.$)"
        title=r"The waterfall of $STS$ along the cut line"
        bias,grid=self.get_grid_value(channel=channel)
        raw=grid[::,line,::]
        step=(bias[-1]-bias[0])/raw.shape[1]
        for j,cole in enumerate(raw):
            spec = cole
            if isnormolize:
                min_val = np.min(spec)
                max_val = np.max(spec)
                spec= (spec - min_val) / (max_val - min_val)
            if isgauss:
                spec=gaussian_filter(spec,sigma=sigma)
            if isline:
                bias,grid=self.get_grid_value(channel=channel)
                point_per_bias=abs(bias[-1]-bias[0])/grid.shape[-1]
                bias_point=int((biasvalue-bias[0])/point_per_bias)
                line=ax.vlines(biasvalue,ymin=0,ymax=spec.max())
            raw_filted=gaussian_filter(raw_data, sigma=3)
            peak, _ = find_peaks(raw_filted, distance=200)
            peak_bias = peak*step+sweep[0]
            ax.plot(sweep,(raw_filted+offset*j)*unit,color=color)
            if len(lines):
                for i,line in enumerate(lines):
                    if j==line:
                        ax.plot(sweep,(raw_filted+offset*j)*unit,color=colorA[i])
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.xaxis.get_label().set_fontsize(18)
        ax.yaxis.get_label().set_fontsize(18)
        ax.tick_params(axis='y', labelsize=14)
        ax.tick_params(axis='x', labelsize=14)
        ax.set_title(title,fontsize=18)
    


    def display_STS_image(self,fig,ax,biasvalue=-0.1,channel="LIY_1_omega",imagetitle="SiC",sig=None,isnormolize=True,isaxis=False,isscalebar=True,scalecolor="white",scalesize=0.3,cmap="Blues_r",iscolorbar=True,iscorrect=True,isgauss=True,sigma=1,ispoint=False,point=(0,0),pointcolor="r"):
        bias,grid=self.get_grid_value(channel=channel)
        point_per_bias=abs(bias[-1]-bias[0])/grid.shape[-1]
        bias_point=int((biasvalue-bias[0])/point_per_bias)
        
        grid_settings=self.get_grid_settings()
        image=grid[::,::,bias_point]
        [x_p,y_p]=image.shape
        [x_n,y_n]=[grid_settings[-3]*1e9,grid_settings[-2]*1e9]
        fact=x_n/x_p
        
        if iscorrect:
            image=self.correct_line_median(image)
        if isgauss:
            image=gaussian_filter(image,sigma=sigma)
        posX,posY=self.get_pos()
        
        if isnormolize:
            min_val = np.min(image)
            max_val = np.max(image)
            image = (image - min_val) / (max_val - min_val)
            if sig !=None and sig>0 and sig<1:
                image[image>sig]=sig
                image[image<1-sig]=1-sig

        img=ax.imshow(image[::,::],cmap=cmap,origin="lower")
        if not isaxis:
            ax.axis ('off')

        if iscolorbar:
            Vmin=np.ndarray.min(image) 
            Vmax=np.ndarray.max(image) 
            cb=fig.colorbar(img,ax=ax,orientation="vertical",pad=0.02,shrink=0.8) 
            cb.ax.yaxis.set_tick_params(size=0.8,labeltop=True) 
            cb.set_ticks([Vmax,Vmin])
            cb.set_ticklabels(["High","Low"])
        
        if isscalebar:
            factor=x_p/x_n
            scale=int(x_n/5)
            scalebar=AnchoredSizeBar(ax.transData,scale*factor,"{0} nm".format(scale),"lower right",pad=1,sep=3,color=scalecolor,label_top=True,frameon=False,size_vertical=scalesize)
            ax.add_artist(scalebar)
        if ispoint:
            ax.scatter(point[0],point[1],s=10,color=pointcolor)
        if imagetitle!="":
            ax.set_title(imagetitle) 

    def display_topo(self,fig,ax,imagetitle="SiC",sig=None,isnormolize=True,isaxis=False,isscalebar=True,scalecolor="white",scalesize=0.3,cmap="Blues_r",iscolorbar=True,iscorrect=True,isgauss=True,sigma=1,ispoint=False,point=(0,0),pointcolor="r"):
        bias,para=self.get_grid_para(channel="Para")
        grid_settings=self.get_grid_settings()
        image=para[::,::,4]
        if iscorrect:
            image=self.correct_line_median(image)
        if isgauss:
            image=gaussian_filter(image,sigma=sigma)
        posX,posY=self.get_pos()
        [x_p,y_p]=image.shape
        [x_n,y_n]=[grid_settings[-3]*1e9,grid_settings[-2]*1e9]
        fact=x_n/x_p
        
        if isnormolize:
            min_val = np.min(image)
            max_val = np.max(image)
            image = (image - min_val) / (max_val - min_val)
            if sig !=None and sig>0 and sig<1:
                image[image>sig]=sig
                image[image<1-sig]=1-sig

        img=ax.imshow(image[::,::],cmap=cmap,origin="lower")
        if not isaxis:
            ax.axis ('off')

        if iscolorbar:
            Vmin=np.ndarray.min(image) 
            Vmax=np.ndarray.max(image) 
            cb=fig.colorbar(img,ax=ax,orientation="vertical",pad=0.02,shrink=0.8) 
            cb.ax.yaxis.set_tick_params(size=0.8,labeltop=True) 
            cb.set_ticks([Vmax,Vmin])
            cb.set_ticklabels(["High","Low"])
        
        if isscalebar:
            factor=x_p/x_n
            scale=int(x_n/5)
            scalebar=AnchoredSizeBar(ax.transData,scale*factor,"{0} nm".format(scale),"lower right",pad=1,sep=3,color=scalecolor,label_top=True,frameon=False,size_vertical=scalesize)
            ax.add_artist(scalebar)
        if ispoint:
            ax.scatter(point[0],point[1],s=10,color=pointcolor)
        if imagetitle!="":
            ax.set_title(imagetitle) 


    def display_single_spec(self,fig,ax,point=(0,0),channel="LIY_1_omega",biasvalue=0.1,isnormolize=True,isgauss=True,sigma=1,color="r",spectitle="",isline=False,islegend=True,offset=0):
        bias,grid=self.get_grid_value(channel=channel)
        spec=grid[point[0]][point[1]]
        if isnormolize:
            min_val = np.min(spec)
            max_val = np.max(spec)
            spec= (spec - min_val) / (max_val - min_val)
        if isgauss:
            spec=gaussian_filter(spec,sigma=sigma)
        if isline:
            bias,grid=self.get_grid_value(channel=channel)
            point_per_bias=abs(bias[-1]-bias[0])/grid.shape[-1]
            bias_point=int((biasvalue-bias[0])/point_per_bias)
            line=ax.vlines(biasvalue,ymin=0,ymax=spec.max())
        spec=spec+offset
        ax.plot(bias,spec,label=r"$dI/dV$ ($a.u.$)",color=color)
        xlabel="Sample bias (V)"
        ylabel=r"$dI/dV$ ($a.u.$)"
        title=r"The $STS$ of selected point: ({0},{1})".format(point[0],point[1])
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.xaxis.get_label().set_fontsize(18)
        ax.yaxis.get_label().set_fontsize(18)
        ax.tick_params(axis='y', labelsize=14)
        ax.tick_params(axis='x', labelsize=14)
        if islegend:
            ax.legend()
        ax.set_title(title,fontsize=18)
        if spectitle!="":
            ax.set_title(spectitle) 
        else:
            ax.set_title(title) 


    def point_spec_with_topo(self,fig,ax1,ax2,points=[(0,0),],colors=["r",'coral',"peachpuff","lightskyblue","royalblue","k",'coral',"grey","yellow"]):

        point=points[0]
        color=colors[0]
        self.display_topo(fig,ax1,imagetitle="",sig=None,isnormolize=True,isaxis=False,isscalebar=True,scalecolor="white",scalesize=0.3,cmap="Blues_r",iscolorbar=True,iscorrect=True,isgauss=True,sigma=1,ispoint=True,point=point,pointcolor=color)
        self.display_single_spec(fig,ax2,point=point,isnormolize=True,isgauss=True,sigma=1,color=color,spectitle=r"The $STS$ of selected point")
        for i,point in enumerate(points):
            self.display_topo(fig,ax1,imagetitle="",sig=None,isnormolize=True,isaxis=False,isscalebar=True,scalecolor="white",scalesize=0.3,cmap="Blues_r",iscolorbar=False,iscorrect=True,isgauss=True,sigma=1,ispoint=True,point=point,pointcolor=colors[i])
            self.display_single_spec(fig,ax2,point=point,isnormolize=True,isgauss=True,sigma=1,color=colors[i],spectitle=r"The $STS$ of selected point")


    def point_spec_with_mapping(self,fig,ax1,ax2,points=[(0,0),],bias=0.1,colors=["r",'coral',"peachpuff","lightskyblue","royalblue","k",'coral',"grey","yellow"]):
        point=points[0]
        color=colors[0]
        self.display_STS_image(fig,ax1,biasvalue=bias,channel="LIY_1_omega",imagetitle="SiC",sig=None,isnormolize=True,isaxis=False,isscalebar=True,scalecolor="white",scalesize=0.3,cmap="Blues_r",iscolorbar=True,iscorrect=True,isgauss=True,sigma=1,ispoint=True,point=point,pointcolor=color)
        self.display_single_spec(fig,ax2,point=point,isnormolize=True,isgauss=True,sigma=1,color=color,spectitle=r"The $STS$ of selected point",isline=True,biasvalue=bias)
        


    


        


   
              


    


    
    
        
