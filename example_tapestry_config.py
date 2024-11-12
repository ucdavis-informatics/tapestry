"""
Example tdap config.py file
"""
logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'file': {
            'class': 'logging.Formatter',
            'format': '$asctime :: $module ($lineno) :: $levelname :: $message',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '$',
        },
        'console': {
            'class': 'logging.Formatter',
            'format': '$asctime :: $module ($lineno) :: $levelname :: $message',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '$',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'log/tdap.log',
            'mode': 'a+',
            'formatter': 'file'
        }
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        },
    },
}

tdap_configs = {
#################################################################################
#################################################################################
#################################################################################
# Test run for Clarity backends
#################################################################################
#################################################################################
#################################################################################
    "dev_clarity": {
        "alert_email":"awriedl@ucdavis.edu",
        # dotenv file location
        "dotenv_file_path":".env",
        # period
        "period":"H",
        # data source secrets
        "databases":{
            "clarity": {
                "type":"btss",
                "btss_secret_title":"clart4_svc_tdap", # Clartity test 4
                "sess_limit" : 4,
                "query_window_start" : 0,
                "query_window_end" : 24,
                "dest":False
            },
            
            "tdap_dm":{
                "type":"btss",
                "btss_secret_title":"edm_srv_tdap",
                "dest":True
            }
        },
        "tables":{
            "matrix_table_name":"dev_clarity_matrix"
        },        
        # concepts
        "concepts":{
            "creat": {
                "conceptproperties": {
                    "originid": "101,1604,2142,1230000101,1230001604,1230002142",
                    "origindatatype": "numeric",
                    "origintype": "labrslt",
                    "desttable": "dev_clarity_matrix",
                    "fillmethod": "forwardfill",
                    "fillwithnormalmode" : "n",
                    "filltimetonormal" : "0",
                    "fillnormalvalue" : "unk",
                    "cleanvals":"n",
                    "minval":0,
                    "maxval":100
                }
            },
            "clcm": {
                "conceptproperties": {
                    "originid": "95,1230000095",
                    "origindatatype": "numeric",
                    "origintype": "labrslt",
                    "desttable": "dev_clarity_matrix",
                    "fillmethod": "forwardfill",
                    "fillwithnormalmode" : "n",
                    "filltimetonormal" : "0",
                    "fillnormalvalue" : "unk",
                    "cleanvals":"n",
                    "minval":0,
                    "maxval":100
                }
            },
            "hgb": {
                "conceptproperties": {
                    "originid": "236,2520,1230000236,1230002520",
                    "origindatatype": "numeric",
                    "origintype": "labrslt",
                    "desttable": "dev_clarity_matrix",
                    "fillmethod": "forwardfill",
                    "fillwithnormalmode" : "n",
                    "filltimetonormal" : "0",
                    "fillnormalvalue" : "unk",
                    "cleanvals":"n",
                    "minval":0,
                    "maxval":100
                }
            },            
            "o2dev": {
                "conceptproperties": {
                    "originid": "'805370'",
                    "origindatatype": "string",
                    "origintype": "flowsheet",
                    "desttable": "dev_clarity_matrix",
                    "fillmethod": "forwardfill",
                    "fillwithnormalmode" : "n",
                    "filltimetonormal" : "0",
                    "fillnormalvalue" : "unk",
                    "cleanvals":"n",
                    "minval":0,
                    "maxval":100
                }
            },
            "bp": {
                "conceptproperties": {
                    "originid": "'5'",
                    "origindatatype": "string",
                    "origintype": "flowsheet",
                    "desttable": "dev_clarity_matrix",
                    "fillmethod": "forwardfill",
                    "fillwithnormalmode" : "n",
                    "filltimetonormal" : "0",
                    "fillnormalvalue" : "unk",
                    "cleanvals":"n",
                    "minval":0,
                    "maxval":100

                },
            },
        },

        "ts_features_config": {
            "window_len": 4,
            "window_type": "blackman",
            "fill_val": 0,
            "group_level": 0,
            "peak_order": 2,
            "peak_suffix": "_peak",
            "cp_model": "l2",
            "cp_min_size": 2,
            "cp_jump": 1,
            "cp_pen": 10,
            "cp_suffix": "_cp"
        },

        # extensions (may reference a data source in code)
        "extensions":{},
        # derivations
        "derivations":{},
        # cleanups
        "cleanups":{}

        # process specific extensions (optional)

    },

#################################################################################
#################################################################################
#################################################################################
# test run for OMOP backends
#################################################################################
#################################################################################
#################################################################################
"dev_omop":{
    ###############################
    # custom pcd tdap variables
    ###############################
    "alert_email":"awriedl@ucdavis.edu",
    "pre_2014_drop_or_correct": "correct",
    "period":"H",

    "tables":{
        "matrix_table_name":"dev_omop_matrix"
    }, 
    #############################################
    # standard TDAP config items
    #############################################
    # data source secrets
    "databases":{
        "omop": {
            "type":"btss",
            "btss_secret_title":"testomopsql01_uchdw_omop_srv_cdi3",
            "sess_limit" : 25,
            "query_window_start" : 0,
            "query_window_end" : 24,
            "dest":False
        },
        "tdap_dm":{
                "type":"btss",
                "btss_secret_title":"edm_srv_tdap",
                "dest":True
            }
    },       

    "ts_features_config": {
        "window_len": 4,
        "window_type": "blackman",
        "fill_val": 0,
        "group_level": 0,
        "peak_order": 2,
        "peak_suffix": "_peak",
        "cp_model": "l2",
        "cp_min_size": 2,
        "cp_jump": 1,
        "cp_pen": 10,
        "cp_suffix": "_cp"
    },
    # concepts
    "concepts":{
        
        # "38176-4,36916-5,38176-4"
        "testmsr": {
            "conceptproperties": {
                "originid":[3034860,3034597],
                "origindatatype": "numeric",
                "origintype": "measurement",
                "desttable": "dev_omop_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },
        "testdx": {
            "conceptproperties": {
                "originid":[45596549, 35207173, 35211350],
                "origindatatype": "string",
                "origintype": "condition_occurrence",
                "desttable": "dev_omop_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },

        "testrx": {
            "conceptproperties": {
                "originid":[40164897, 36250141],
                "origindatatype": "string",
                "origintype": "drug_exposure",
                "desttable": "dev_omop_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },

        "testproc": {
            "conceptproperties": {
                "originid":[4133311,762510],
                "origindatatype": "string",
                "origintype": "procedure_occurrence",
                "desttable": "dev_omop_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },

        "testobs": {
            "conceptproperties": {
                "originid":[4353936],
                "origindatatype": "numberic",
                "origintype": "observation",
                "desttable": "dev_omop_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        }
        
    },

    "extensions":{},
    "derivations":{},
    "cleanups":{},   

} ,


#################################################################################
#################################################################################
#################################################################################
# PCD example config
# uses clarity backend
# primarily used in a seperate repo
#################################################################################
#################################################################################
#################################################################################
"pcd":{
    ###############################
    # custom pcd tdap variables
    ###############################
    "pre_2014_drop_or_correct": "correct",
    "period":"W",

    "tables":{
        # screen set tables
        "screen_set_table_name":"pcd_screen_set",
        
        # fast lanes tables
        "fast_lane_table_name":"pcd_fast_lane",

        # TDAP tables
        "patient_table_name":"pcd_patient_level",
        "matrix_table_name":"pcd_matrices",
        "dx_phases_table_name":"pcd_disease_phases",
        "dx_states_table_name":"pcd_states",
        "mm_algos_table_name":"pcd_mm_algos",
        "pcd_enc_table_name":"pcd_enc",
        "pcd_enc_reasons_table_name":"pcd_enc_reasons",

        # custom data tables
        "treatment_plan_table_name":"pcd_tx_plan",
        "take_home_meds_table_name":"pcd_tx_take_home",
        "notes_table_name":"pcd_notes",
        
        # PCD predictions tables
        "pcd_pred_table_name":"pcd_predictions",
        "mm_enc_table_name":"pcd_mm_encounters",  

        # pcd exclusions tables
        "exclusions_table_name":"pcd_exclusions"
    }, 
    #############################################
    # standard TDAP config items
    #############################################
    # data source secrets
    "databases":{
        "clarity": {
            "type":"vault",
            "vault_path":"cdi3/db/clart4/srv_cdi3",
            # "type":"btss",
            # "btss_secret_title":"clart4",
            "sess_limit" : 6,
            "query_window_start" : 0,
            "query_window_end" : 24,
            "dest":False
        },
        # a custom extension db
        "cdi3dsudb":{
            "type":"vault",
            "vault_path":"cdi3/db/testdsudwsql01",
            # "type":"btss",
            # "btss_secret_title":"testdsusql01",
            "dest":True
        },
        "redcap_pcd_reg":{
            "type":"vault",
            "vault_path":"cdi3/projects/pcd/pcd_de_api_key",
            "dest":False
        },
        "redcap_young_mm":{
            "type":"vault",
            "vault_path":"cdi3/projects/pcd/young_mm_api_key",
            "dest":False
        },
        "nomad":{
            "type":"vault",
            "vault_path":"ri/db/mongodb/notesdb_tls",
            "dest":False
        }
    },       

    "ts_features_config": {
        "window_len": 4,
        "window_type": "blackman",
        "fill_val": 0,
        "group_level": 0,
        "peak_order": 2,
        "peak_suffix": "_peak",
        "cp_model": "l2",
        "cp_min_size": 2,
        "cp_jump": 1,
        "cp_pen": 10,
        "cp_suffix": "_cp"
    },

    "exclusions": {
        "waldenstroms": {"cnext_search_string":"wald", "dx_id_list":[91132, 463913]},
        "cmml": {"cnext_search_string":"chronic myelomonocytic leukemia", "dx_id_list":[314381, 521045]},
        "leukemia": {"cnext_search_string":"myeloid leukemia", "dx_id_list":[1279634, 142235, 2083, 528570, 525517]}
    },

    # extensions (may reference a data source in code)
    "extensions":{
        "cdi3sql_pcd":{
            "include":True,
            "module":"ext_cdi3_custom_pcd",
            "config":{
                "ds_key":"cdi3dsudb", # references key earlier in file
                "roll_window_size":12,
                "roll_min_periods":1
            }
        },
        "enc_vitals":{
            "include":True,
            "module":"ext_enc_vitals",
            "config":{
                "vital_filter_cols":["contact_date","bp_systolic", "bp_diastolic", "temperature", "pulse", "weight", "height", "respirations"]
            }
        },
        "enc_in_person_events":{
            "include":True,
            "module":"ext_enc_in_person_events",
            "config":{
                "in_person_filter_cols":["contact_date","staff_resource"],
                "rolling_periods":4,
                "min_periods":1
            }
        },
        "mm_bmbx_bill_events":{
            "include":False,
            "module":"ext_bill_events",
            "config":{
                "ds_key":"clarity",
                "icd9_str_list":["203.00","203.01","203.02"],
                "icd10_str_list":["C90.00","C90.01","C90.02"],
                "bmbx_cpt_codes":["38220", "38221","88305"]
            }
        }
    },
    # derivations
    "derivations":{
        "kl_ratio":{
            "include":True,
            "module":"derivation_kl_ratio",
            "config":{
                "required_cols":["kapalr_ord_num_value_mean", "lmdalr_ord_num_value_mean"]
            }
        },
        "creat_clearance":{
            "include":True,
            "module":"derivation_creat_clearance",
            "config":{
                "required_cols":["enc_weight_mean","creat_ord_num_value_mean"]
            }
        },
        "num_dc":{
            "include":False,
            "module":"derivation_num_dc",
            "config":{
                "required_cols":["hgb_ord_num_value_min","clcm_ord_num_value_max",
                "creat_ord_num_value_max","creat_clearance","kl_ratio"]
            }
        },
        # NOTE: PCD Gates/mm_pub_algod MUST run as the last derivations
        "pcd_gates":{
            "include":True,
            "module":"derivation_pcd_gates",
            "config":{
                "required_cols":["hgb_ord_num_value_min","clcm_ord_num_value_max","creat_ord_num_value_max","creat_clearance",
                "monoclonal_spike_count","monoclonal_spike_count_roll","cd138_val_low_range_max","cd138_val_high_range_max","pc_positive_studies","kl_ratio"],
                "pcd_disease_dict_list" : [
                    {"disease_col":"symptomatic_mm","phase_col":"symptomatic_mm_phase"}
                    ,{"disease_col":"smm1","phase_col":"smm1_phase"}
                    ,{"disease_col":"smm2","phase_col":"smm2_phase"}
                    ,{"disease_col":"txe_mm","phase_col":"txe_mm_phase"}
                    ,{"disease_col":"mgus","phase_col":"mgus_phase"}
                    ,{"disease_col":"eod_mgus","phase_col":"eod_mgus_phase"}
                    ,{"disease_col":"eod_only","phase_col":"eod_only_phase"}
                    ,{"disease_col":"smm3dge","phase_col":"smm3dge_phase"}
                ]
            }
        },
        "mm_pub_algos":{
            "include":False,
            "module":"derivation_brandenburg_princic_v2",
            "config":{
                "required_cols":[
                    "mm_bill_dx_count","mm_bill_dx_first","mm_bill_dx_last","mm_bill_dx_icd9_list","mm_bill_dx_icd10_list","mm_bill_dx_native"
                    ,"mm_bill_bmbx_native", "bmbx_native"
                    ,"iglbalr_native", "iglbglr_native", "iglbmlr_native","kapalr_native", "lmdalr_native", "klratlr_native",
                    "peplr_native", "pepulr_native",
                    "imnfxserlr_native","imnfxurlr_native",
                    "bonesrvord_native"],
                "bmbx_cols":["mm_bill_bmbx_native", "bmbx_native"],
                "basic_test_cols":["iglbalr_native", "iglbglr_native", "iglbmlr_native","kapalr_native", "lmdalr_native", "klratlr_native",
                                    "peplr_native", "pepulr_native",
                                    "imnfxserlr_native","imnfxurlr_native",
                                    "bonesrvord_native"],
                "diagnostic_time_box_days":2555
            }
        } 
    },
    
    "cleanups":{},

    # concepts
    "concepts":{
        "pcd_edx": {
            "conceptproperties": {
                "originid": "1408659,1021234,225155,225156,90564,90566,182862,163858,163861,163916,89177,89178,89179,191341,184381,184381,191697,200933,117178,117182,117077,178518,178518,178519,178519,116721,178789,120258,236653,106519,105916,105917,91132,91134,71688,71689,71690,71691,71692,71699,71710,71711,91676,91680,91681,92031,93224,93227,93660,93662,78317,2641,2643,2644,277858,150630,247159,263008,291519,291554,247269,247271,247273,66201,274122,274123,274126,274127,111397,111404,248176,248000,278056,256180,267210,2056,2057,2059,2060,145160,281421,145850,227144,195312,195313,195318,2380,227844,227845,209903,233910,195864,107401,228720,228757,397010,397010,397475,397508,397515,397516,401815,401816,404043,402025,403198,314440,314441,314442,294692,312386,299108,299109,360669,360669,301246,356284,351209,294520,295025,295025,300177,314419,314435,455860,464989,419231,419231,419263,419263,423448,419297,419297,896519,1180713,1192555,1180286,1181245,1435651,1339773,451550,1278997,452814,452815,452816,452817,451438,1284901,1521448,1187479,1409388,1379216,1411543,1411543,1292469,1292469,1413743,1408659,1346546,1531119,1531162,1523449,463684,1539527,1539528,1539670,1539671,1419240,191697,178518,178519,200933,90564,90566,116721,177106,201678,117178,117182,117077,182862,220471,191341,198908,198909,191071,130608,184381,89176,89177,89178,89179,1018783,206477,1019618,206475,206476,1019314,163858,163861,163916,206897,206898,225155,225156,1021234,1021133,957598,195864,198115,198116,228720,228757,143974,209898,209903,209951,209952,217473,2380,210335,227844,227845,105916,105917,105598,227144,153443,78317,2641,2643,2644,196379,120258,10149,106519,195313,189651,236653,178789,103603,91132,91134,71688,71689,71690,71691,71692,71695,71696,71699,71704,71710,71711,91676,91680,91681,107401,92031,227326,93224,93227,93660,93662,281421,291519,291554,314419,314435,277858,314440,314441,314442,290176,301246,308622,294520,300177,295025,295025,294692,278056,312386,299108,299109,299110,294785,294788,294792,294793,267210,294170,307254,257489,150630,145850,111397,111397,111404,248176,248000,263008,256180,66201,236477,99379,99381,99382,99386,254589,149604,149605,274122,274123,274126,274127,247159,233910,2054,2055,2056,2057,2059,2060,247269,247271,247273,145160,148492,257488,422647,410587,419231,1520384,403198,419263,419297,401815,401816,404043,360669,350479,353231,356284,351209,402025,397010,397475,325178,325179,397508,397515,397516,332295,999323,450203,431273,423448,424499,425476,428568,1025928,1166229,1166544,1166547,1027017,1026896,896519,1203800,1187285,1187286,900458,1171515,1177504,1180063,1180087,1180108,1180129,1180145,1180210,1180966,1181245,1199233,1171319,1171330,1179173,1179182,1179338,1179397,1179101,1179105,1180815,1180861,1179279,1179292,1179404,1179459,898845,1181397,1180032,1179678,1180782,1180806,1179691,1292469,1179732,1179734,1190447,1181561,1179779,1199914,1192948,1179890,1179924,1179946,1182769,1193097,1182752,1192699,1193132,1185799,1186865,1169694,1180666,1185990,1187322,1169972,1192260,1187492,1187395,1169547,1170132,1192555,1192464,1187405,1187238,1187436,1187467,1187479,1170367,1180681,1180713,1180457,1180493,1180495,1180512,1180582,1170556,1170566,1169470,1180162,1180164,1180269,1180302,1180304,1296833,451438,1427511,451550,1419240,452814,452815,452816,452817,1296656,1194529,1411543,1408551,1247868,1247869,1339773,1278997,1277348,1277730,1279666,1521448,1277735,1277744,1277745,1281359,1264013,1379216,1284901,1284901,1409388,1539670,1539671,1346546,1430918,1430920,1430921,1533470,1539527,1539528,1347024,1538435",
                "origindatatype": "numeric",
                "origintype": "enc_dx",
                "desttable": "pytdap_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode": "n",
                "filltimetonormal": "0",
                "fillnormalvalue": "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100,
                "include_inverse":False
            }
        },
        "kapalr": {
            "conceptproperties": {
                "originid": "959,1230000959,3031,3801,1230003801, 1230105663",
                "origindatatype": "numeric",
                "origintype": "labrslt",
                "desttable": "pytdap_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },
        "lmdalr": {
            "conceptproperties": {
                "originid": "962,1230000962,3032,3802,1230003802, 1230105669",
                "origindatatype": "numeric",
                "origintype": "labrslt",
                "desttable": "pytdap_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },
        "klratlr": {
            "conceptproperties": {
                "originid": "960,3033,3803,1230003803,1230000960",
                "origindatatype": "numeric",
                "origintype": "labrslt",
                "desttable": "pytdap_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },
        "creat": {
            "conceptproperties": {
                "originid": "101,1604,2142,1230000101,1230001604,1230002142",
                "origindatatype": "numeric",
                "origintype": "labrslt",
                "desttable": "pytdap_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },
        "clcm": {
            "conceptproperties": {
                "originid": "95,1230000095",
                "origindatatype": "numeric",
                "origintype": "labrslt",
                "desttable": "pytdap_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },
        "hgb": {
            "conceptproperties": {
                "originid": "236,2520,1230000236,1230002520",
                "origindatatype": "numeric",
                "origintype": "labrslt",
                "desttable": "pytdap_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },            
        "iglbalr": {
            "conceptproperties": {
                "originid": "462,2375, 1230002375",
                "origindatatype": "numeric",
                "origintype": "labrslt",
                "desttable": "pytdap_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },

        "iglbglr": {
            "conceptproperties": {
                "originid": "464,1065,2376, 1230002376",
                "origindatatype": "numeric",
                "origintype": "labrslt",
                "desttable": "pytdap_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },
        "iglbmlr": {
            "conceptproperties": {
                "originid": "465,2377,1230002377",
                "origindatatype": "numeric",
                "origintype": "labrslt",
                "desttable": "pytdap_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },
        "peplr": {
            "conceptproperties": {
                "originid": "506,1230000506",
                "origindatatype": "numeric",
                "origintype": "labrslt",
                "desttable": "pytdap_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },
        "pepulr": {
            "conceptproperties": {
                "originid": "507,1230004610",
                "origindatatype": "numeric",
                "origintype": "labrslt",
                "desttable": "pytdap_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },

        "imnfxserlr": {
            "conceptproperties": {
                "originid": "2374,1230002374",
                "origindatatype": "numeric",
                "origintype": "labrslt",
                "desttable": "pytdap_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },
        "imnfxurlr": {
            "conceptproperties": {
                "originid": "3192,1230003192",
                "origindatatype": "numeric",
                "origintype": "labrslt",
                "desttable": "pytdap_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        },
        "bonesrvord": {
            "conceptproperties": {
                "originid": "33370,33371",
                "origindatatype": "string",
                "origintype": "ordproc",
                "desttable": "pytdap_matrix",
                "fillmethod": "forwardfill",
                "fillwithnormalmode" : "n",
                "filltimetonormal" : "0",
                "fillnormalvalue" : "unk",
                "cleanvals":"n",
                "minval":0,
                "maxval":100
            }
        }
        
    }    

}    
}
