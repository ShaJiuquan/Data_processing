import sqlite3
import pySPM
import datetime
import platform
import numpy as np
import pandas as pd
import nanonispy as nap


class STMdatabase:

    DATA_LIST_NAME="STMdataLists"
    SPEC_VALUE_NAME="STMSpecValue"
    GRID_VALUE_NAME="STMGridValue"
    GRID_INFO_NAME="STMGridInfo"
    SPEC_INFO_NAME="STMSpecInfo"
    IMAGE_VALUE_NAME="STMimageValue"
    IMAGE_INFO_NAME="STMimageInfo"

    STMDATALIST={"Name":"SiC001","TimeStamp":20.0,"UpdateFilePath":"",
             "Date":'24.02.2023',"Time":'09:09:29',"Bias_V": 2.5,
             "Current_pA": 30,"Type":"SXM","PosX_nm":328,"PosY_nm":328}
    STMIMAGEINFO= {"List_ID":1,"TIME_STAMP":100,"NANONIS_VERSION":"SiC001","SCANIT_TYPE":"",
              "REC_DATE":"","REC_TIME":"","REC_TEMP":290,"ACQ_TIME":20.0,
              "SCAN_PIXELS":512,"SCAN_FILE":"","SCAN_TIME":30.0,"SCAN_RANGE":20,
              "SCAN_OFFSET":"","SCAN_ANGLE":10.0,"SCAN_DIR":'up',
              "BIAS": 2.5,"Z_CONTROLLER": "","COMMENT":"SXM","Session_Path":"",
              "SW_Version":"","UI_Release":"","RT_Release":"","RT_Frequency":"",
              "Signals_Oversampling":"","Animations_Period":"","Indicators_Period":"",
              "Measurements_Period":"","DATA_INFO":""}
    STMIMAGEVALUE={"Info_ID":1,"List_ID":1,"TIME_STAMP":1,"Z_forward":"",
                  "Z_backward" :"","Current_forward":"","Current_backward":"","LIY_1_omega_forward":"",
                  "LIY_1_omega_backward":""}
    STMSPECINFO={"List_ID":1,"TIME_STAMP":2.0,"Date":"11.08.2022 12:15:27","User":"NaN",
                 "X_m":"91.6774E-9","Y_m":"91.6774E-9","Z_m":"91.6774E-9","Z_offset":"0",
                 "Settling_time":"4E-3","Integration_time":"8E-3","Z_Ctrl_hold":"TRUE",
                 "Final_Z":"-211.889E-9","Filter_type":"Gaussian","Filter_Order":"3",
                 "Cut_off":"","comment":""}
    STMSPECVALUE={"Info_ID":1,"List_ID":1,"TIME_STAMP":1,"Bias":'Bias calc (V)', "Current_forward":'Current (A)',
                    "Current_backward":'Current (A)',"LIY_1_omega_forward":"",'LIY_1_omega_backward':"LIY_1_omega_forward"}

    STMGRIDINFO={"List_ID":1,"TIME_STAMP":2.0,"Grid_dim":"11.08.2022 12:15:27","Grid_settings":"NaN",
                 "Filetype":"91.6774E-9","Sweep_Signal":"91.6774E-9","Fixed_parameters":"91.6774E-9",
                 "Experiment_parameters":"0","Parameters":"4E-3"," Experiment_size":"8E-3","Points":"TRUE",
                 "Channels":"-211.889E-9","Delay":"Gaussian","Experiment":"3","Start_time":"","End_time":"",
                 "User":"Gaussian","comment":"3","Current":"","Calibration":"","Offset":"","Gain":""}
    STMGRIDVALUE={"Info_ID":1,"List_ID":1,"TIME_STAMP":1,"Para":"","Current":"",
                  "Bias":"","LIX_1_omega":"","LIY_1_omega":""}
    
    CREATE_SPEC_VALUE_SQL = """ CREATE TABLE IF NOT EXISTS {0} (
                                        Data_ID   INTEGER PRIMARY KEY AUTOINCREMENT,
                                        Info_ID INTEGER,
                                        List_ID INTEGER,
                                        TIME_STAMP  REAL,
                                        Bias  BLOB,
                                        Current_forward   BLOB,
                                        Current_backward   BLOB,
                                        LIY_1_omega_forward   BLOB,
                                        LIY_1_omega_backward   BLOB,
                                        FOREIGN KEY (List_ID) 
                                            REFERENCES STMSpecInfo (List_ID) 
                                                ON DELETE CASCADE 
                                                ON UPDATE NO ACTION    
                                        FOREIGN KEY (Info_ID) 
                                            REFERENCES STMSpecInfo(Info_ID) 
                                                ON DELETE CASCADE 
                                                ON UPDATE NO ACTION
                                        );
                                     """.format(SPEC_VALUE_NAME)
    CREATE_DATA_LIST_SQL= """ CREATE TABLE IF NOT EXISTS {0} (
                                        List_ID   INTEGER PRIMARY KEY AUTOINCREMENT,
                                        Name TEXT NOT NULL,
                                        TimeStamp REAL,
                                        UpdateFilePath TEXT,
                                        Date TEXT NOT NULL,
                                        Time TEXT NOT NULL,
                                        Bias_V REAL NOT NULL,
                                        Current_pA REAL NOT NULL,
                                        Type TEXT NOT NULL,
                                        PosX_nm  REAL NOT NULL, 
                                        PosY_nm REAL NOT NULL
                                    ) """.format(DATA_LIST_NAME)
    CREATE_GRID_VALUE_SQL = """ CREATE TABLE IF NOT EXISTS {0} (

                                        Data_ID   INTEGER PRIMARY KEY AUTOINCREMENT,
                                        Info_ID INTEGER,
                                        List_ID INTEGER,
                                        TIME_STAMP  REAL,
                                        Para   BLOB,
                                        Current   BLOB,
                                        Bias   BLOB,
                                        LIX_1_omega   BLOB,
                                        LIY_1_omega   BLOB,
                                        FOREIGN KEY (List_ID) 
                                            REFERENCES STMGridInfo (List_ID) 
                                                ON DELETE CASCADE 
                                                ON UPDATE NO ACTION         
                                        FOREIGN KEY (Info_ID) 
                                            REFERENCES STMGridInfo(Info_ID) 
                                                ON DELETE CASCADE 
                                                ON UPDATE NO ACTION

                                        );
                                     """.format(GRID_VALUE_NAME)
    CREATE_GRID_INFO_SQL= """ CREATE TABLE IF NOT EXISTS {0} (
                                        Info_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        List_ID INTEGER,
                                        TIME_STAMP  REAL,
                                        Grid_dim TEXT,
                                        Grid_settings TEXT,
                                        Filetype TEXT,
                                        Sweep_Signal TEXT,
                                        Fixed_parameters TEXT,
                                        Experiment_parameters TEXT,
                                        Parameters TEXT,
                                        Experiment_size TEXT,
                                        Points TEXT,
                                        Channels TEXT,
                                        Delay TEXT,
                                        Experiment TEXT,
                                        Start_time TEXT,
                                        End_time TEXT,
                                        User TEXT,
                                        Comment TEXT,
                                        Current TEXT,
                                        Calibration TEXT,
                                        Offset TEXT,
                                        Gain TEXT,
                                        FOREIGN KEY (List_ID) 
                                        REFERENCES STMdataLists (List_ID) 
                                            ON DELETE CASCADE 
                                            ON UPDATE NO ACTION                                      
                                    ); """.format(GRID_INFO_NAME)
    CREATE_SPEC_INFO_SQL= """ CREATE TABLE IF NOT EXISTS {0} (
                                        Info_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        List_ID INTEGER,
                                        TIME_STAMP  REAL,
                                        Date TEXT,
                                        User TEXT,
                                        X_m TEXT,
                                        Y_m TEXT,
                                        Z_m TEXT,
                                        Z_offset TEXT,
                                        Settling_time TEXT,
                                        Integration_time TEXT,
                                        Z_Ctrl_hold TEXT,
                                        Final_Z TEXT,
                                        Filter_type TEXT,
                                        Filter_order TEXT,
                                        Cut_off TEXT,
                                        Comment TEXT,
                                        FOREIGN KEY (List_ID) 
                                        REFERENCES STMdataLists (List_ID) 
                                            ON DELETE CASCADE 
                                            ON UPDATE NO ACTION
          
                                    ); """.format(SPEC_INFO_NAME)
    CREATE_IMAGE_VALUE_SQL= """ CREATE TABLE IF NOT EXISTS {0} (
                                        Data_ID   INTEGER PRIMARY KEY AUTOINCREMENT,
                                        Info_ID INTEGER,
                                        List_ID INTEGER,
                                        TIME_STAMP  REAL,
                                        
                                        Z_forward   BLOB,
                                        Z_backward   BLOB,
                                        Current_forward   BLOB,
                                        Current_backward   BLOB,
                                        LIY_1_omega_forward   BLOB,
                                        LIY_1_omega_backward   BLOB,
                                        FOREIGN KEY (List_ID) 
                                            REFERENCES STMimageInfo (List_ID) 
                                                ON DELETE CASCADE 
                                                ON UPDATE NO ACTION
                                                
                                                
                                        FOREIGN KEY (Info_ID) 
                                            REFERENCES STMimageInfo(Info_ID) 
                                                ON DELETE CASCADE 
                                                ON UPDATE NO ACTION

                                        );
                                     """.format(IMAGE_VALUE_NAME)
    
    CREATE_IMAGE_INFO_SQL= """ 
                                CREATE TABLE {}(
                                Info_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                List_ID INTEGER,
                                TIME_STAMP  REAL,
                                NANONIS_VERSION TEXT,
                                SCANIT_TYPE TEXT,
                                REC_DATE TEXT,
                                REC_TIME TEXT,
                                REC_TEMP TEXT,
                                ACQ_TIME TEXT,
                                SCAN_PIXELS TEXT,
                                SCAN_FILE TEXT,
                                SCAN_TIME TEXT,
                                SCAN_RANGE TEXT,
                                SCAN_OFFSET TEXT,
                                SCAN_ANGLE TEXT,
                                SCAN_DIR TEXT,
                                BIAS TEXT,
                                Z_CONTROLLER TEXT,
                                COMMENT TEXT,
                                Session_Path TEXT,
                                SW_Version TEXT,
                                UI_Release TEXT,
                                RT_Release TEXT,
                                RT_Frequency TEXT,
                                Signals_Oversampling TEXT,
                                Animations_Period TEXT,
                                Indicators_Period TEXT,
                                Measurements_Period  TEXT,
                                DATA_INFO TEXT, 
                                FOREIGN KEY (List_ID) 
                                    REFERENCES STMdataLists (List_ID) 
                                        ON DELETE CASCADE 
                                        ON UPDATE NO ACTION

                                ); """.format(IMAGE_INFO_NAME)
     
    def __init__(self,databaseName: str) -> None:
        self.databaseName=databaseName
    def creat_all_table(self)->None:
        self.drop_creat_list_table()
        self.drop_creat_imageInfo_table()
        self.drop_creat_imageValue_table()
        self.drop_creat_specInfo_table()
        self.drop_creat_specValue_table()
        self.drop_creat_GridInfo_table()
        self.drop_creat_GridValue_table()

        
    def execute_sql(self,sql:str)->None:
        try:
            with sqlite3.connect(self.databaseName) as conn:
                    c = conn.cursor()
                    c.execute(sql)
            print("SUCCESS---------"+sql)
        except Exception as ex:
            print("ErroMsg-----",ex)
            print("ERRO-------"+sql)
    
    def execute_sql_arg(self,sql:str,arg)->None:
        try:
            with sqlite3.connect(self.databaseName) as conn:
                    c = conn.cursor()
                    c.execute(sql,arg)
            print("SUCCESS---------"+sql,arg)
        except Exception as ex:
            print("ErroMsg-----",ex)
            print("ERRO-------"+sql)
    def execute_sql_fetchone(self,sql):
        try:
            with sqlite3.connect(self.databaseName) as conn:
                    c = conn.cursor()
                    data=c.execute(sql)
                    Value=data.fetchall()[0][0]
            
            print("SUCCESS---------"+sql)
            return Value
        except Exception as ex:
            print("ErroMsg-----",ex)
            print("ERRO-------"+sql)
            return None
    @staticmethod
    def get_list_id(cls,myfile):
        try:
            select_list_id="SELECT List_ID FROM {0} WHERE UpdateFilePath='{1}'".format(cls.DATA_LIST_NAME,myfile)
            listID=cls.execute_sql_fetchone(select_list_id)
            return listID
        except Exception as ex:
            print("ERRO-----","get_list_id")
            print("ErroMsg----", ex)
            print("the databaseName is",cls.databaseName)
    @staticmethod
    def get_time_stamp(cls,myfile):
        select_time_stamp="SELECT TimeStamp FROM {0} WHERE UpdateFilePath='{1}'".format(cls.DATA_LIST_NAME,myfile)
        timeStamp=cls.execute_sql_fetchone(select_time_stamp)
        return  timeStamp
    
    @staticmethod
    def get_image_pix(cls,myfile):
        try:
            listID=cls.get_list_id(cls,myfile)
            sql_pix="SELECT SCAN_PIXELS from {0} WHERE List_ID={1}".format(cls.IMAGE_INFO_NAME,listID)
            Pix_s=cls.execute_sql_fetchone(sql_pix)
            pix=[int(x) for x in Pix_s.split(" ") ]
            return  pix
        
        except Exception as ex:
            print("ERRO---------------get_image_pix",ex)
    
    @staticmethod
    def get_pos_X(cls,myfile):
        try:
            listID=cls.get_list_id(cls,myfile)
            sql_pos="SELECT PosX_nm  from {0}  WHERE UpdateFilePath='{1}'".format(cls.DATA_LIST_NAME,myfile)
            PosX=cls.execute_sql_fetchone(sql_pos)
            return  PosX
        except Exception as ex:
            print("ERRO---------------get_pos",ex)
    @staticmethod
    def get_pos_Y(cls,myfile):
        try:
            listID=cls.get_list_id(cls,myfile)
            sql_pos="SELECT PosY_nm from {0}  WHERE UpdateFilePath='{1}'".format(cls.DATA_LIST_NAME,myfile)
            PosY=cls.execute_sql_fetchone(sql_pos)
            return  PosY
        except Exception as ex:
            print("ERRO---------------get_pos",ex)

    
    @staticmethod
    def get_size(cls,myfile):
        try:
            listID=cls.get_list_id(cls,myfile)
            sql_range="SELECT SCAN_RANGE from {0} WHERE List_ID={1}".format(cls.IMAGE_INFO_NAME,listID)
            range=cls.execute_sql_fetchone(sql_range)
            return  range
        except Exception as ex:
            print("ERRO---------------get_size",ex)
    
    
    

    @staticmethod
    def get_image_value(cls,myfile,channel="Z_forward"):
        try:
            listID=cls.get_list_id(cls,myfile)
            pix=cls.get_image_pix(cls,myfile)
            sql_image_value="SELECT {0} from {1} WHERE List_ID={2}".format(channel,cls.IMAGE_VALUE_NAME,listID)
            image_blob=cls.execute_sql_fetchone(sql_image_value)
            image=np.frombuffer(image_blob, dtype=float).reshape((pix[0], pix[1]))
            return  image
        except Exception as ex:
            print("ERRO---------------get_image_value",ex)
    
    @staticmethod
    def get_info_id(cls,myfile):
        listID=cls.get_list_id(cls,myfile)
        if myfile.endswith("sxm"):
            select_info_id="SELECT Info_ID FROM {0} WHERE List_ID={1}".format(cls.IMAGE_INFO_NAME,listID)
        elif myfile.endswith("dat"):
            select_info_id="SELECT Info_ID FROM {0} WHERE List_ID={1}".format(cls.SPEC_INFO_NAME,listID)
        elif myfile.endswith("3ds"):
            select_info_id="SELECT Info_ID FROM {0} WHERE List_ID={1}".format(cls.GRID_INFO_NAME,listID)

        info_id=cls.execute_sql_fetchone(select_info_id)
        return  info_id




    def drop_table(self,tableName:str)->None:
        try:
            drop_list_table="DROP TABLE IF EXISTS {}".format(tableName)
            self.execute_sql(drop_list_table)
            print("{0} table is droped".format(tableName))
        except Exception as ex:
            print("ErroMsg",ex)
            print("ERRO"+"{0} table droped failed".format(tableName))


    def creat_table(self,tableName: str,creat_table_sql: str)->None:
        try:
            self.execute_sql(creat_table_sql)
            print("{0} table is created".format(tableName))
        except Exception as ex:
            print("ErroMsg",ex)
            print("ERRO"+"{0} table created failed".format(tableName))
    

    def drop_creat_list_table(self)->None:
        self.drop_table(self.DATA_LIST_NAME)
        self.creat_table(tableName=self.DATA_LIST_NAME,creat_table_sql=self.CREATE_DATA_LIST_SQL)

    def drop_creat_imageInfo_table(self)->None:
        self.drop_table(self.IMAGE_INFO_NAME)
        self.creat_table(tableName=self.IMAGE_INFO_NAME, creat_table_sql=self.CREATE_IMAGE_INFO_SQL)
        
    def drop_creat_imageValue_table(self)->None:
        self.drop_table(self.IMAGE_VALUE_NAME)
        self.creat_table(tableName=self.IMAGE_VALUE_NAME,creat_table_sql=self.CREATE_IMAGE_VALUE_SQL)
        



    def drop_creat_specInfo_table(self)->None:
        self.drop_table(self.SPEC_INFO_NAME)
        self.creat_table(tableName=self.SPEC_INFO_NAME,creat_table_sql=self.CREATE_SPEC_INFO_SQL)
        

    def drop_creat_specValue_table(self)->None:
        self.drop_table(self.SPEC_VALUE_NAME)
        self.creat_table(tableName=self.SPEC_VALUE_NAME,creat_table_sql=self.CREATE_SPEC_VALUE_SQL)
        


         
    
    def drop_creat_GridInfo_table(self)->None:
        self.drop_table(self.GRID_INFO_NAME)
        self.creat_table(tableName=self.GRID_INFO_NAME,creat_table_sql=self.CREATE_GRID_INFO_SQL)
        





    def drop_creat_GridValue_table(self)->None:
        self.drop_table(self.GRID_VALUE_NAME)
        self.creat_table(tableName=self.GRID_VALUE_NAME,creat_table_sql=self.CREATE_GRID_VALUE_SQL)
        

    def insert_table(self,table: str,DATA_LIST: list,STMdateList: list)->None:
        try:
            KEYS=list(DATA_LIST.keys())
            STMdataKeys=list(STMdateList.keys())
            values=[STMdateList[STMdataKey] for STMdataKey in STMdataKeys if STMdataKey in KEYS ]
            key=",".join([STMdataKey for STMdataKey in STMdataKeys if STMdataKey in KEYS ])
            value=",".join(["?"]*len([STMdataKey for STMdataKey in STMdataKeys if STMdataKey in KEYS ]))
            insert="INSERT INTO {}({}) VALUES({})".format(table,key,value)
            self.execute_sql_arg(insert,values)
            print("Insert table is successed")
        except Exception as ex:
            print("ErroMsg",ex)
            print("ERRO"+"Insert table is failed")

            



    def insert_list_table(self,STMdateList:STMDATALIST=STMDATALIST)->None:
        table=self.DATA_LIST_NAME
        DATA_LIST=self.STMDATALIST
        self.insert_table(table,DATA_LIST,STMdateList)
        
    def insert_imageInfo_table(self,STMdateList:STMIMAGEINFO=STMIMAGEINFO)->None:
        table=self.IMAGE_INFO_NAME
        DATA_LIST=self.STMIMAGEINFO
        self.insert_table(table,DATA_LIST,STMdateList)

    def insert_imageValue_table(self,STMdateList:STMIMAGEVALUE=STMIMAGEVALUE)->None:
        table=self.IMAGE_VALUE_NAME
        DATA_LIST=self.STMIMAGEVALUE
        self.insert_table(table,DATA_LIST,STMdateList)

    def insert_specInfo_table(self,STMdateList:STMSPECINFO=STMSPECINFO)->None:
        table=self.SPEC_INFO_NAME
        DATA_LIST=self.STMSPECINFO
        self.insert_table(table,DATA_LIST,STMdateList)

    def insert_specValue_table(self,STMdateList:STMSPECVALUE=STMSPECVALUE)->None:
        table=self.SPEC_VALUE_NAME
        DATA_LIST=self.STMSPECVALUE
        self.insert_table(table,DATA_LIST,STMdateList)
    
    def insert_gridInfo_table(self,STMdateList:STMGRIDINFO=STMGRIDINFO)->None:
        table=self.GRID_INFO_NAME
        DATA_LIST=self.STMGRIDINFO
        self.insert_table(table,DATA_LIST,STMdateList)

    def insert_gridValue_table(self,STMdateList:STMGRIDVALUE=STMGRIDVALUE)->None:
        table=self.GRID_VALUE_NAME
        DATA_LIST=self.STMGRIDVALUE
        self.insert_table(table,DATA_LIST,STMdateList)


class utils:
    def string_to_timestamp(date_string, format_string='%Y-%m-%d %H:%M:%S'):
        try:
            # Parse the date string into a datetime object
            date_obj = datetime.datetime.strptime(date_string, format_string)

            # Convert the datetime object to a timestamp
            timestamp = date_obj.timestamp()
            return timestamp
        except ValueError as e:
            print(f"Error: {e}")
            return None
    def get_platform():
        platforms={
            "linux1":"linux",
            "linux2":"linux",
            "darwin":"OS X",
            "win32":"Windows"
        }
        if platform not in platforms:
            return platform
        return platforms[platform]

class STMdata: 
    def __init__(self,filePath: str,DatabaseName="STMdata.db") -> None:
        self.filePath=filePath
        self.dataList=STMdatabase.STMDATALIST
        self.list_ID=None
        self.TimeStamp=None
        self.info_ID=None
        self.DatabaseName=DatabaseName
        self.posX,self.posY=self.get_pos()

        

    def get_data_list(self)->STMdatabase.STMDATALIST:
        self.dataList["UpdateFilePath"]=self.filePath
        file=[f for f in self.filePath.split(".")]
        filetype=file[-1]
        platform = utils.get_platform()
        if platform=="Windows":
            fileData=[f for f in file[-2].split("\\")]
        else:
            fileData=[f for f in file[-2].split("/")]
        fileName=fileData[-1]
        self.dataList["Name"]=fileName
        self.dataList["Type"]=filetype
        return self.dataList
    
    def get_pos(self):
        databaseName=self.DatabaseName
        try:
            self.posX=STMdatabase.get_pos_X(cls=STMdatabase(databaseName),myfile=self.filePath)
            self.posY=STMdatabase.get_pos_Y(cls=STMdatabase(databaseName),myfile=self.filePath)
            return self.posX,self.posY
        except Exception as ex:
            print("ErroMsg------get_pos",ex)
            print("ERRO---get_pos "+ "the file is not in datalist")

    def get_data_info(self):
        databaseName=self.DatabaseName
        try:
            self.list_ID=STMdatabase.get_list_id(cls=STMdatabase(databaseName),myfile=self.filePath)
            self.TimeStamp=STMdatabase.get_time_stamp(cls=STMdatabase(databaseName),myfile=self.filePath)
        except Exception as ex:
            print("ErroMsg------get_data_info",ex)
            print("ERRO----get_data_info "+"the file is not in datalist")

    def get_data_value(self):
        databaseName=self.DatabaseName
        try:
            self.list_ID=STMdatabase.get_list_id(cls=STMdatabase(databaseName),myfile=self.filePath)
            self.TimeStamp=STMdatabase.get_time_stamp(cls=STMdatabase(databaseName),myfile=self.filePath)
            self.info_ID=STMdatabase.get_info_id(cls=STMdatabase(databaseName),myfile=self.filePath)
        except Exception as ex:
            print("ErroMsg------get_data_value",ex)
            print("ERRO----get_data_info "+"the file is not in datalist")
        
        
        
       

    
class STMimage(STMdata):
    def __init__(self, filePath: str,DatabaseName="STMdata.db") -> None:
        super().__init__(filePath,DatabaseName=DatabaseName)
        self.imageInfo=STMdatabase.STMIMAGEINFO
        self.imageValue=STMdatabase.STMIMAGEVALUE
        self.pix=self.get_pix()
        self.scan_size=self.get_image_size()
        self.scan_range=self.get_image_range()
        self.data=None


    def get_image_range(self):
        try:
            
            self.scan_range=[round(self.posX-self.scan_size[0]/2,3), round(self.posX+self.scan_size[0]/2,3), round(self.posY-self.scan_size[1]/2,3), round(self.posY+self.scan_size[1]/2,3)]
            return self.scan_range
        except Exception as ex:
            print("ErroMsg------get_image_range",ex)
            print("ERRO----get_image_range "+"the file is not in datalist")

    def get_pix(self):
        databaseName=self.DatabaseName
        try:
            self.pix=STMdatabase.get_image_pix(cls=STMdatabase(databaseName),myfile=self.filePath)
            return self.pix
        except Exception as ex:
            print("ErroMsg------get_pix",ex)
            print("ERRO----get_pix "+"the file is not in datalist")

    def get_image_value(self,channel="Z_forward"):
        databaseName=self.DatabaseName
        try:
            image=STMdatabase.get_image_value(cls=STMdatabase(databaseName),myfile=self.filePath,channel=channel)
            return image
        except Exception as ex:
            print("ErroMsg--get_image_value",ex)
            print("ERRO---get_image_value "+"the file is not in datalist")
    


    def get_data_list(self) -> STMdatabase.STMDATALIST:
        format_string='%d.%m.%Y %H:%M:%S'
        SXMfile=pySPM.SXM(self.filePath)
        header=SXMfile.header
        [x_n,y_n]=header['SCAN_RANGE'][0]
        Bias=header['BIAS'][0][0]
        Curr=header['Z-CONTROLLER'][1][3]
        Pos=header['SCAN_OFFSET'][0]
        FilePath=header['SCAN_FILE'][0][0]+header['SCAN_FILE'][0][1]
        REC_Data=header['REC_DATE'][0][0]
        REC_Time=header['REC_TIME'][0][0]
        date_time_s=REC_Data+" "+REC_Time
        timestamp = utils.string_to_timestamp(date_time_s,format_string)
        self.dataList["TimeStamp"]=timestamp
        self.dataList["Date"]=REC_Data
        self.dataList["Time"]=REC_Time
        self.dataList["Bias_V"]=round(float(Bias),2)
        self.dataList["Current_pA"]=round(float(Curr)*1e12,1)
        self.dataList["PosX_nm"]=round(float(Pos[0])*1e9,3)
        self.dataList["PosY_nm"]=round(float(Pos[1])*1e9,3)
        return super().get_data_list()
    
    def get_image_size(self):
        try:
            databaseName=self.DatabaseName
            scan_size=STMdatabase.get_size(cls=STMdatabase(databaseName),myfile=self.filePath)
            self.scan_size=[float(value)*1e9 for value in scan_size.split(" ")]
            
            return self.scan_size
        except Exception as ex:
            print("ErroMsg--get_image_size",ex)
            print("ERRO---get_image_size "+"the file is not in datalist")
    

    def get_data_info(self)->STMdatabase.STMIMAGEINFO:
        super().get_data_info()
        SXMfile=pySPM.SXM(self.filePath)
        header=SXMfile.header
        self.imageInfo["List_ID"]=self.list_ID
        self.imageInfo["TIME_STAMP"]=self.TimeStamp
        imagekeys=list(self.imageInfo.keys())
        raws=""
        cols=""
        try:
            for i,value in enumerate(list(header.values())[:]):
                raws=""
                for raw in value:
                    cols=""
                    for col in raw:
                        if cols!="":
                            cols=cols+" "+col
                        else:
                            cols=col
                    if raws!="":
                        raws=raws+' '+cols
                    else:
                        raws=cols
                      
                    self.imageInfo[imagekeys[i+2]]=raws
        except:
            print("ERRO------- get data information is failed and the file is ",self.filePath)
        finally:
            return  self.imageInfo
        
    def get_data_value(self)->STMdatabase.STMIMAGEVALUE:

        super().get_data_value()
        SXMfile=pySPM.SXM(self.filePath)
        header=SXMfile.header
        self.imageValue["Info_ID"]=self.info_ID
        self.imageValue["List_ID"]=self.list_ID
        self.imageValue["TIME_STAMP"]=self.TimeStamp
        h=header["DATA_INFO"][0]
        i=h.index("Name")
        channels=[]
        for z in header["DATA_INFO"][1:]:
            channels.append(z[i]) 
        STMKeys=["Z","Current","LIY_1_omega"]
     
        
        for channel in channels:
          
            if channel in STMKeys:
                try:
                    image_f=SXMfile.get_channel(channel,direction="forward")
                    image=np.array(image_f.pixels)
                    array_bytes_f = image.tobytes()
                    print(channel+"_forward")
                    self.imageValue[channel+"_forward"]=sqlite3.Binary(array_bytes_f)
                    image_b=SXMfile.get_channel(channel,direction="backward")
                    image=np.array(image_b.pixels)
                    array_bytes_b = image.tobytes()
                    print(channel+"_backward")
                    self.imageValue[channel+"_backward"]=sqlite3.Binary(array_bytes_b)
                
                    
                except:
                    print("ERRO------- get data information is failed and the file is ",self.filePath)
                    
               
        return  self.imageValue
    
class STMspec(STMdata):
    def __init__(self, filePath: str) -> None:
        super().__init__(filePath)
        self.specInfo=STMdatabase.STMSPECINFO
        self.specValue=STMdatabase.STMSPECVALUE


    def get_data_list(self) -> STMdatabase.STMDATALIST:
        format_string='%d.%m.%Y %H:%M:%S'            
        filePath=self.filePath
        Notfound=1
        skiprows=13
        while Notfound:
            df_h=pd.read_csv(filePath,sep="\t",nrows=skiprows)

            dic_key=df_h[df_h.keys()]["Experiment"][skiprows-1]

            if dic_key!= "[DATA]":
                Notfound=1
                skiprows+=1
            else:
                Notfound=0
                df_h=pd.read_csv(filePath,sep="\t",nrows=skiprows)

        file=[f for f in filePath.split(".")]
        filetype=file[-1]
        fileName=[f for f in file[-2].split("\\")][-1]
        self.dataList["Name"]=fileName
        self.dataList["UpdateFilePath"]=self.filePath
        x=df_h["bias spectroscopy"][2]
        y=df_h["bias spectroscopy"][3]
        z=df_h["bias spectroscopy"][4]
        date=df_h["bias spectroscopy"][0]
        [d,t]=[d for d in date.split(" ")]
        date_time_s=d+" "+t
        timestamp = utils.string_to_timestamp(date_time_s,format_string)
        self.dataList["Date"]=d
        self.dataList["Time"]=t
        self.dataList["TimeStamp"]=timestamp
        self.dataList["Type"]=filetype
        self.dataList["PosX_nm"]=round(float(x)*1e9,3)
        self.dataList["PosY_nm"]=round(float(y)*1e9,3)
        Notfound=1
        skiprows=20
        while Notfound:
            df_d=pd.read_table(filePath,sep="\t",skiprows=skiprows)
            Keys=df_d.keys()
            if Keys[0]!= "Bias calc (V)":
                Notfound=1
                skiprows-=1
            else:
                df_d=pd.read_table(filePath,sep="\t",skiprows=skiprows)
                Keys=df_d.keys()
                Notfound=0
                I=df_d[Keys[1]]
                X=np.array(df_d[Keys[0]])        
                Bias=X[0]
                Curr=I[0]
                self.dataList["Bias_V"]=round(float(Bias),2)
                self.dataList["Current_pA"]=round(float(Curr)*1e12,1)
        return super().get_data_list()
    

    def get_data_info(self)->STMdatabase.STMSPECINFO:
        super().get_data_info()
        self.specInfo["List_ID"]=self.list_ID
        self.specInfo["TIME_STAMP"]=self.TimeStamp           
        filePath=self.filePath
        Notfound=1
        skiprows=10
        try:
            while Notfound:
                df_h=pd.read_csv(filePath,sep="\t",nrows=skiprows)
                dic_key=df_h[df_h.keys()]["Experiment"][skiprows-1]
                if dic_key!= "[DATA]":
                    Notfound=1
                    skiprows+=1
                else:
                    Notfound=0
                    df_h=pd.read_csv(filePath,sep="\t",nrows=skiprows)
            Values=df_h["bias spectroscopy"][0:-1]
            imagekeys=list(self.specInfo.keys())
            for i,value in enumerate(Values):
                        
                self.specInfo[imagekeys[i+2]]=value
        except:
            print(self.filePath)
        finally:
            return self.specInfo
    

    def get_data_value(self)->STMdatabase.STMSPECVALUE:

        super().get_data_value()
        skiprows=21
        Notfound=1
        self.specValue["Info_ID"]=self.info_ID
        self.specValue["List_ID"]=self.list_ID
        self.specValue["TIME_STAMP"]=self.TimeStamp
        while Notfound:
            df_d=pd.read_table(self.filePath,sep="\t",skiprows=skiprows)
            Keys=df_d.keys()
            if Keys[0]!= "Bias calc (V)":
                Notfound=1
                skiprows-=1
            else:
                df_d=pd.read_table(self.filePath,sep="\t",skiprows=skiprows)
                channels=list(df_d.keys())
                Notfound=0


        STMSpecKeys=['Bias calc (V)', 'Current (A)',  'LIY 1 omega (A)', 'Current [bwd] (A)',  'LIY 1 omega [bwd] (A)']
        KeySpec={'Bias calc (V)':"Bias", 'Current (A)':"Current_forward",  'LIY 1 omega (A)':"LIY_1_omega_forward", 'Current [bwd] (A)':"Current_backward",  'LIY 1 omega [bwd] (A)':"LIY_1_omega_backward"}
        for channel in channels:
            if channel in STMSpecKeys:
                try:
                    SpecValue=np.array(df_d[channel])
                    array_bytes = SpecValue.tobytes()
                    self.specValue[KeySpec[channel]]= sqlite3.Binary(array_bytes)
                except:
                    pass
        
        return self.specValue




class STMgrid(STMdata):
    
    def __init__(self, filePath: str) -> None:
        super().__init__(filePath)
        self.gridInfo=STMdatabase.STMGRIDINFO
        self.gridValue=STMdatabase.STMGRIDVALUE



    def get_data_list(self) -> STMdatabase.STMDATALIST:

        format_string='%d.%m.%Y %H:%M:%S'
        try:
            grid = nap.read.Grid(self.filePath) 
            sweep=grid._derive_sweep_signal()
            dic_keys = grid._load_data().keys()
            list_data=list(grid._load_data())
            params=grid._load_data()['params']
            head = grid.read_raw_header(byte_offset=745)
            df=pd.DataFrame([x.split(",") for x in head.split("\r\n")])
            Res=[j for j in df[0][0].split("=")]
            Set=[j for j in df[0][1].split(";")]
            Point=[j for j in df[0][8].split("=")]
            Date=[j for j in df[0][12].split("=")]
            DateTime=[j for j in Date[1].split(" ")]
            Recdate=DateTime[0][1:]
            Rectime=DateTime[1][:-1]
            Resxy=[j for j in Res[1].split("x")]
            xpoints=[j for j in Set[0].split("=")]

            Resoltion=[float(Resxy[0][1:]),float(Resxy[1][:-1]),float(Point[1])]
            position=[float(xpoints[1]),float(Set[1])]
            size=[float(Set[2]),float(Set[3])]
            date_time_s=Recdate+" "+Rectime
            timestamp = utils.string_to_timestamp(date_time_s,format_string)
            self.dataList["TimeStamp"]=timestamp
            self.dataList["UpdateFilePath"]=self.filePath
            self.dataList["Date"]=Recdate
            self.dataList["Time"]=Rectime
            self.dataList["Bias_V"]=round(float(0),2)
            self.dataList["Current_pA"]=round(float(0)*1e12,1)
            
            self.dataList["PosX_nm"]=round(float(position[0])*1e9,3)
            self.dataList["PosY_nm"]=round(float(position[1])*1e9,3)
        except:
           
            self.dataList["TimeStamp"]=0
            self.dataList["UpdateFilePath"]=""
            self.dataList["Date"]=0
            self.dataList["Time"]=0
            self.dataList["Bias_V"]=0
            self.dataList["Current_pA"]=0
            self.dataList["Type"]="3ds"
            self.dataList["PosX_nm"]=0
            self.dataList["PosY_nm"]=0
        finally:
            return super().get_data_list()
        

    def get_data_info(self)->STMdatabase.STMGRIDINFO:
        super().get_data_info()
        self.gridInfo["List_ID"]=self.list_ID
        self.gridInfo["TIME_STAMP"]=self.TimeStamp   
        try:
            grid = nap.read.Grid(self.filePath) 
            sweep=grid._derive_sweep_signal()
            dic_keys = grid._load_data().keys()
            list_data=list(grid._load_data())
            params=grid._load_data()['params']
            data=grid._load_data()['LIY 1 omega (A)']
            head = grid.read_raw_header(byte_offset=850)
            df=pd.DataFrame([x.split(",") for x in head.split("\r\n")])
            heads=[]
            for dfi in df[0]:
                if dfi==":HEADER_END:":
                    break
                heads.append(dfi) 
            ovalue=[]
            for hs in heads:
                hvalue=[x.split(",") for x in hs.split("=")]
                ovalue.append(hvalue[1][0])
            imagekeys=list(self.gridInfo.keys())
            for i,value in enumerate(ovalue):
                        
                self.gridInfo[imagekeys[i+2]]=value
        except Exception as ex:
            print("+++Erro------------------------------------------------")
            print("ErroMsg",ex)
            print(self.filePath)
        finally:
            return self.gridInfo
        


    def get_data_value(self)->STMdatabase.STMGRIDVALUE:

        super().get_data_value()
        self.gridValue["Info_ID"]=self.info_ID
        self.gridValue["List_ID"]=self.list_ID
        self.gridValue["TIME_STAMP"]=self.TimeStamp
        
        try:
            grid = nap.read.Grid(self.filePath) 
            sweep=grid._derive_sweep_signal()
            head = grid.read_raw_header(byte_offset=850)
            df=pd.DataFrame([x.split(",") for x in head.split("\r\n")])
            heads=[]
            for dfi in df[0]:
                if dfi==":HEADER_END:":
                    break
                heads.append(dfi)
            ovalue=[]
            for hs in heads:
                hvalue=[x.split(",") for x in hs.split("=")]
                ovalue.append(hvalue[1][0])
            channels=[x.split(",") for x in ovalue[9][1:-1].split(";")]

            STMSpecKeys=['Current (A)', 'LIX 1 omega (A)',  'LIY 1 omega (A)']
            KeySpec={'Current (A)':"Current", 'LIX 1 omega (A)':"LIX_1_omega",  'LIY 1 omega (A)':"LIY_1_omega", 'params':"Para","Bias":"Bias"}
            SpecValue=np.array(grid._load_data()["params"])
            array_bytes = SpecValue.tobytes()
            self.gridValue[KeySpec["params"]]=sqlite3.Binary(array_bytes)
            SpecValue=np.array(sweep)
            array_bytes = SpecValue.tobytes()
            self.gridValue[KeySpec["Bias"]]=sqlite3.Binary(array_bytes)
            for channel in channels:
                key_value= channel[0]
                if key_value in STMSpecKeys:
                    try: 
                        SpecValue=np.array(grid._load_data()[key_value])
                        array_bytes = SpecValue.tobytes()
                        self.gridValue[KeySpec[key_value]]=sqlite3.Binary(array_bytes)
                        
                    except Exception as ex:
                        print("+++Erro------------------------------------------------")
                        print("ErroMsg",ex)
           
        except Exception as ex:
            print("+++Erro------------------------------------------------")
            print("ErroMsg",ex)
            print(self.filePath)
        finally: 
            return self.gridValue

    
        


         

    
    



