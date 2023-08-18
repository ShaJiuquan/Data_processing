import sqlite3


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
    STMIMAGEINFO= {"List_ID":1,"TIME_STAMP":100,"NANONIS_VERSION":"SiC001",
              "REC_DATE":"","REC_TIME":"","REC_TEMP":290,"ACQ_TIME":20.0,
              "SCAN_PIXELS":512,"SCAN_FILE":"","SCAN_TIME":30.0,"SCAN_RANGE":20,
              "SCAN_OFFSET":"","SCAN_ANGLE":10.0,"SCAN_DIR":'up',"Time":'09:09:29',
              "BIAS": 2.5,"Z_CONTROLLER": "","COMMENT":"SXM","Session_Path":"",
              "SW_Version":"","UI_Release":"","RT_Release":"","RT_Frequency":"",
              "Signals_Oversampling":"","Animations_Period":"","Indicators_Period":"",
              "Measurements_Period":"","DATA_INFO":""}
    STMIMAGEVALUE={"Info_ID":1,"List_ID":1,"TIME_STAMP":1,"Z_forward":"",
                  "Z_backward" :"","Current_forward":"","LIY_1_omega_forward":"",
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
                                            REFERENCES STMSpecInfo (List_ID) 
                                                ON DELETE CASCADE 
                                                ON UPDATE NO ACTION         
                                        FOREIGN KEY (Info_ID) 
                                            REFERENCES STMSpecInfo(Info_ID) 
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
            print("SUCCESS---------"+sql)
        except Exception as ex:
            print("ErroMsg-----",ex)
            print("ERRO-------"+sql)



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
            



    def insert_list_table(self,STMdateList:list=STMDATALIST)->None:
        table=self.DATA_LIST_NAME
        DATA_LIST=self.STMDATALIST
        self.insert_table(table,DATA_LIST,STMdateList)
        
    def insert_imageInfo_table(self,STMdateList:list=STMIMAGEINFO)->None:
        table=self.IMAGE_INFO_NAME
        DATA_LIST=self.STMIMAGEINFO
        self.insert_table(table,DATA_LIST,STMdateList)

    def insert_imageValue_table(self,STMdateList:list=STMIMAGEVALUE)->None:
        table=self.IMAGE_VALUE_NAME
        DATA_LIST=self.STMIMAGEVALUE
        self.insert_table(table,DATA_LIST,STMdateList)

    def insert_specInfo_table(self,STMdateList:list=STMSPECINFO)->None:
        table=self.SPEC_INFO_NAME
        DATA_LIST=self.STMSPECINFO
        self.insert_table(table,DATA_LIST,STMdateList)

    def insert_specValue_table(self,STMdateList:list=STMSPECVALUE)->None:
        table=self.SPEC_VALUE_NAME
        DATA_LIST=self.STMSPECVALUE
        self.insert_table(table,DATA_LIST,STMdateList)
    
    def insert_gridInfo_table(self,STMdateList:list=STMGRIDINFO)->None:
        table=self.GRID_INFO_NAME
        DATA_LIST=self.STMGRIDINFO
        self.insert_table(table,DATA_LIST,STMdateList)
    



