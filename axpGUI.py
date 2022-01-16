#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from tkinter import *
import threading
import os
import sys
import serial
import time

from serial.serialutil import Timeout

glo_req_set_addr = -1
glo_req_set_data = -1
root = Tk()

 
frame1 = Frame(root)

frame2 = Frame(root)
frame2_1 = Frame(frame2)
frame2_2 = Frame(frame2)
frame2_3 = Frame(frame2)

frame3 = Frame(root)
frame4 = Frame(root)
frame5 = Frame(root)
root.title("axp203 studio")

com_select = Entry(frame1)
com_select.pack()

#reg00H
textvar_ACIN_presence = StringVar()
textvar_ACIN_useable = StringVar()
textvar_VBUS_presence = StringVar()
textvar_VBUS_useable = StringVar()
textvar_VBUS_above = StringVar()
textvar_cur_dire = StringVar()
textvar_AC_VB_short = StringVar()
textvar_boot_sources = StringVar()
#reg01H
textvar_OT = StringVar()
textvar_charge = StringVar()
textvar_batt_exist = StringVar()
textvar_batt_activate = StringVar()
textvar_chg_cur_low = StringVar()
#reg02h
textvar_vbus_va = StringVar()
textvar_vbus_ses_ab_va = StringVar()
textvar_ses_end_status = StringVar()
#02..0F:userdataflash
textvar_usrData = StringVar()
#####################################################################################
#reg12Hpoweroutput
textvar_ldo3_en = StringVar()
textvar_dcdc2_en = StringVar()
textvar_ldo4_en = StringVar()
textvar_ld02_en = StringVar()
textvar_dcdc3_en = StringVar()
textvar_exten_en = StringVar()
#23dcdc2outvoltage
textvar_dcdc2_vot = StringVar()
#25dcdc2/ldo3dunamicvoltagescalingparameter
textvar_ldo3_vrc_enabling = StringVar()
textvar_dcdc2_vrc_enabling = StringVar()
textvar_ldo3_vra_vot_rising_slope = StringVar()
textvar_dcdc2_vra_vot_rising_slope = StringVar()
#27dcdc3outvot
textvar_dcdc3_vot = StringVar()
#28ldo2/4outvot
textvar_ldo2_vot = StringVar()
textvar_ldo4_vot = StringVar()
#29ldo3outvot
textvar_ldo3_mode = StringVar()
textvar_ldo3_vout = StringVar()
#30vbus-ipsout-channelmanagement
textvar_vbus_ipsout_path_select = StringVar()
textvar_vbus_vhold_vot_lim = StringVar()
textvar_vhold_set = StringVar()
textvar_vbus_cur_limit = StringVar()
#31voffshutdownvoltage
#????(b3)
textvar_voff_set = StringVar()
#32shutdownsettingbattdetchgledcontr
#poffbit
textvar_shutdown = StringVar()
textvar_batt_mon_en = StringVar()
textvar_chg_led_func = StringVar()
textvar_chg_led_mode = StringVar()
textvar_out_disable_time = StringVar()
textvar_pon_key_time = StringVar()
#####################################################################################
#33chargingcontr1
textvar_chg_enable = StringVar()
textvar_chg_end_vot = StringVar()
textvar_chg_end_cur = StringVar()
textvar_chg_cur_set = StringVar()
#34chargingcontr2
textvar_chg_pcg_timeout = StringVar()
textvar_chg_chg_led = StringVar()
textvar_chg_cc_timeout = StringVar()
#35bckbattchgcontr
textvar_bchg_enable = StringVar()
textvar_bchg_cv_end = StringVar()
textvar_bchg_cc_set = StringVar()

#82 adc enable 1
textvar_batt_vot_adc_en = StringVar()
textvar_batt_cur_adc_en = StringVar()
textvar_acin_vot_adc_en = StringVar()
textvar_acin_cur_adc_en = StringVar()
textvar_vbus_vot_adc_en = StringVar()
textvar_vbus_cur_adc_en = StringVar()
textvar_apss_vot_adc_en = StringVar()
textvar_tsss_vot_adc_en = StringVar()
#83 adc enable 2
textvar_its_adc_en = StringVar()
textvar_gpio0_adc_en = StringVar()
textvar_gpio1_adc_en = StringVar()

textvar_adc_val_acin_vot = StringVar()
textvar_adc_val_acin_cur = StringVar()
textvar_adc_val_vbus_vot = StringVar()
textvar_adc_val_vbus_cur = StringVar()
textvar_adc_val_ts_in = StringVar()
textvar_adc_val_ts_ex = StringVar()
textvar_adc_val_gpio0 = StringVar()
textvar_adc_val_gpio1 = StringVar()
textvar_adc_val_batt_inst_pwr = StringVar()
textvar_adc_val_batt_vot = StringVar()
textvar_adc_val_batt_chg_cur = StringVar()
textvar_adc_val_batt_dsc_cur = StringVar()
textvar_adc_val_ips_vot = StringVar()


#reg 00H
lab_ACIN_presence = Label(frame2_1,textvariable=textvar_ACIN_presence)
lab_ACIN_useable = Label(frame2_1,textvariable=textvar_ACIN_useable)
lab_VBUS_presence = Label(frame2_1,textvariable=textvar_VBUS_presence)
lab_VBUS_useable = Label(frame2_1,textvariable=textvar_VBUS_useable)
lab_VBUS_above = Label(frame2_1,textvariable=textvar_VBUS_above)
lab_cur_dire = Label(frame2_1,textvariable=textvar_cur_dire)
lab_AC_VB_short = Label(frame2_1,textvariable=textvar_AC_VB_short)
lab_boot_sources = Label(frame2_1,textvariable=textvar_boot_sources)
#reg 01H
lab_OT = Label(frame2_1,textvariable=textvar_OT)
lab_charge = Label(frame2_1,textvariable=textvar_charge)
lab_batt_exist = Label(frame2_1,textvariable=textvar_batt_exist)
lab_batt_activate = Label(frame2_1,textvariable=textvar_batt_activate)
lab_chg_cur_low = Label(frame2_1,textvariable=textvar_chg_cur_low)
#reg 02h
lab_vbus_va = Label(frame2_1,textvariable=textvar_vbus_va)
lab_vbus_ses_ab_va = Label(frame2_1,textvariable=textvar_vbus_ses_ab_va)
lab_ses_end_status = Label(frame2_1,textvariable=textvar_ses_end_status)
#02..0F:user data flash
lab_usrData = Label(frame2_1,textvariable=textvar_usrData)
#####################################################################################
#reg12H power output
lab_ldo3_en= Label(frame2_2,textvariable=textvar_ldo3_en)
lab_dcdc2_en= Label(frame2_2,textvariable=textvar_dcdc2_en)
lab_ldo4_en= Label(frame2_2,textvariable=textvar_ldo4_en)
lab_ld02_en= Label(frame2_2,textvariable=textvar_ld02_en)
lab_dcdc3_en= Label(frame2_2,textvariable=textvar_dcdc3_en)
lab_exten_en= Label(frame2_2,textvariable=textvar_exten_en)
#23 dcdc2 out voltage
lab_dcdc2_vot= Label(frame2_2,textvariable=textvar_dcdc2_vot)
#25 dcdc2/ldo3 dunamic voltage scaling parameter
lab_ldo3_vrc_enabling= Label(frame2_2,textvariable=textvar_ldo3_vrc_enabling)
lab_dcdc2_vrc_enabling= Label(frame2_2,textvariable=textvar_dcdc2_vrc_enabling)
lab_ldo3_vra_vot_rising_slope= Label(frame2_2,textvariable=textvar_ldo3_vra_vot_rising_slope)
lab_dcdc2_vra_vot_rising_slope= Label(frame2_2,textvariable=textvar_dcdc2_vra_vot_rising_slope)
#27 dcdc3 out vot
lab_dcdc3_vot= Label(frame2_2,textvariable=textvar_dcdc3_vot)
#28 ldo2/4 out vot
lab_ldo2_vot= Label(frame2_2,textvariable=textvar_ldo2_vot)
lab_ldo4_vot= Label(frame2_2,textvariable=textvar_ldo4_vot)
#29 ldo3 out vot
lab_ldo3_mode= Label(frame2_2,textvariable=textvar_ldo3_mode)
lab_ldo3_vout= Label(frame2_2,textvariable=textvar_ldo3_vout)
#30 vbus-ipsout-channel management
lab_vbus_ipsout_path_select= Label(frame2_2,textvariable=textvar_vbus_ipsout_path_select)
lab_vbus_vhold_vot_lim= Label(frame2_2,textvariable=textvar_vbus_vhold_vot_lim)
lab_vhold_set= Label(frame2_2,textvariable=textvar_vhold_set)
lab_vbus_cur_limit= Label(frame2_2,textvariable=textvar_vbus_cur_limit)
#31 voff shutdown voltage
#????(b3)
lab_voff_set= Label(frame2_2,textvariable=textvar_voff_set)
#32 shutdown setting batt det chgled contr
#poff bit
lab_shutdown= Label(frame2_2,textvariable=textvar_shutdown)
lab_batt_mon_en= Label(frame2_2,textvariable=textvar_batt_mon_en)
lab_chg_led_func= Label(frame2_2,textvariable=textvar_chg_led_func)
lab_chg_led_mode= Label(frame2_2,textvariable=textvar_chg_led_mode)
lab_out_disable_time= Label(frame2_2,textvariable=textvar_out_disable_time)
lab_pon_key_time= Label(frame2_2,textvariable=textvar_pon_key_time)
#####################################################################################
#33 charging contr 1
lab_chg_enable= Label(frame2_3,textvariable=textvar_chg_enable)
lab_chg_end_vot= Label(frame2_3,textvariable=textvar_chg_end_vot)
lab_chg_end_cur= Label(frame2_3,textvariable=textvar_chg_end_cur)
lab_chg_cur_set= Label(frame2_3,textvariable=textvar_chg_cur_set)
#34 charging contr 2
lab_chg_pcg_timeout= Label(frame2_3,textvariable=textvar_chg_pcg_timeout)
lab_chg_chg_led= Label(frame2_3,textvariable=textvar_chg_chg_led)
lab_chg_cc_timeout= Label(frame2_3,textvariable=textvar_chg_cc_timeout)
#35 bck batt chg contr
lab_bchg_enable= Label(frame2_3,textvariable=textvar_bchg_enable)
lab_bchg_cv_end= Label(frame2_3,textvariable=textvar_bchg_cv_end)
lab_bchg_cc_set= Label(frame2_3,textvariable=textvar_bchg_cc_set)

#82 adc enable 1
lab_batt_vot_adc_en= Label(frame2_3,textvariable=textvar_batt_vot_adc_en)
lab_batt_cur_adc_en= Label(frame2_3,textvariable=textvar_batt_cur_adc_en)
lab_acin_vot_adc_en= Label(frame2_3,textvariable=textvar_acin_vot_adc_en)
lab_acin_cur_adc_en= Label(frame2_3,textvariable=textvar_acin_cur_adc_en)
lab_vbus_vot_adc_en= Label(frame2_3,textvariable=textvar_vbus_vot_adc_en)
lab_vbus_cur_adc_en= Label(frame2_3,textvariable=textvar_vbus_cur_adc_en)
lab_apss_vot_adc_en= Label(frame2_3,textvariable=textvar_apss_vot_adc_en)
lab_tsss_vot_adc_en= Label(frame2_3,textvariable=textvar_tsss_vot_adc_en)
#83 adc enable 2
lab_its_adc_en= Label(frame2_3,textvariable=textvar_its_adc_en)
lab_gpio0_adc_en= Label(frame2_3,textvariable=textvar_gpio0_adc_en)
lab_gpio1_adc_en= Label(frame2_3,textvariable=textvar_gpio1_adc_en)


##################################################################################################
#adc data
lab_adc_val_acin_vot = Label(frame3,textvariable=textvar_adc_val_acin_vot)
lab_adc_val_acin_cur = Label(frame3,textvariable=textvar_adc_val_acin_cur)
lab_adc_val_vbus_vot= Label(frame3,textvariable=textvar_adc_val_vbus_vot)
lab_adc_val_vbus_cur = Label(frame3,textvariable=textvar_adc_val_vbus_cur)
lab_adc_val_ts_in = Label(frame3,textvariable=textvar_adc_val_ts_in)
lab_adc_val_ts_ex = Label(frame3,textvariable=textvar_adc_val_ts_ex)
lab_adc_val_gpio0 = Label(frame3,textvariable=textvar_adc_val_gpio0)
lab_adc_val_gpio1 = Label(frame3,textvariable=textvar_adc_val_gpio1)
lab_adc_val_batt_inst_pwr = Label(frame3,textvariable=textvar_adc_val_batt_inst_pwr)
lab_adc_val_batt_vot = Label(frame3,textvariable=textvar_adc_val_batt_vot)
lab_adc_val_batt_chg_cur = Label(frame3,textvariable=textvar_adc_val_batt_chg_cur)
lab_adc_val_batt_dsc_cur = Label(frame3,textvariable=textvar_adc_val_batt_dsc_cur)
lab_adc_val_ips_vot = Label(frame3,textvariable=textvar_adc_val_ips_vot)

textvar_reg_get_adr = StringVar()
textvar_reg_set_adr = StringVar()
textvar_reg_set_dat = StringVar()


ent_reg_n = Entry(frame4,textvariable=textvar_reg_get_adr)
textvar_reg_n_ret = StringVar()
textvar_reg_n_ret.set("read area")
ent_reg_n.pack(side=LEFT)
lab_cm_ret = Label(frame4,textvariable=textvar_reg_n_ret)
lab_cm_ret.pack(side=BOTTOM)

def guiset():
    global glo_req_set_addr
    global glo_req_set_data
    # print("ad  " + textvar_reg_set_adr.get())
    # print("dt  " + textvar_reg_set_dat.get())

    adrstr = str(textvar_reg_set_adr.get())
    adrint = 0
    try:
        adrint=int(adrstr,16)
    except Exception as e:
        print(e)
        pass
    
    datstr = str(textvar_reg_set_dat.get())
    datint = 0
    try:
        datint=int(datstr,16)
    except Exception as e:
        print(e)
        pass
    
    if((adrint >= 0) and (datint >= 0) and (adrint < 0x100) and (datint < 0x100)):
        print("addr:%x   data:%x"%(adrint,datint))
        glo_req_set_addr = adrint
        glo_req_set_data = datint
        pass
    pass


btn_set_regn = Button(frame5,text='addr,data set!',command=guiset)

ent_reg_sn = Entry(frame5,textvariable=textvar_reg_set_adr)
ent_reg_sv = Entry(frame5,textvariable=textvar_reg_set_dat)

textvar_reg_s_ret = StringVar()
textvar_reg_s_ret.set("write area")
btn_set_regn.pack(side=LEFT)
ent_reg_sn.pack(side=LEFT)
ent_reg_sv.pack(side=LEFT)
lab_cs_ret = Label(frame5,textvariable=textvar_reg_s_ret)
lab_cs_ret.pack(side=BOTTOM)


frame1.pack()
frame2.pack()
frame2_1.pack(side=LEFT)
frame2_2.pack(side=LEFT)
frame2_3.pack(side=LEFT)
frame3.pack()
frame4.pack()
frame5.pack()
#reg00H
lab_ACIN_presence.pack()
lab_ACIN_useable.pack()
lab_VBUS_presence.pack()
lab_VBUS_useable.pack()
lab_VBUS_above.pack()
lab_cur_dire.pack()
lab_AC_VB_short.pack()
lab_boot_sources.pack()
#reg01H
lab_OT.pack()
lab_charge.pack()
lab_batt_exist.pack()
lab_batt_activate.pack()
lab_chg_cur_low.pack()
#reg02h
lab_vbus_va.pack()
lab_vbus_ses_ab_va.pack()
lab_ses_end_status.pack()
#02..0F:userdataflash
lab_usrData.pack()
#####################################################################################
#reg12Hpoweroutput
lab_ldo3_en.pack()
lab_dcdc2_en.pack()
lab_ldo4_en.pack()
lab_ld02_en.pack()
lab_dcdc3_en.pack()
lab_exten_en.pack()
#23dcdc2outvoltage
lab_dcdc2_vot.pack()
#25dcdc2/ldo3dunamicvoltagescalingparameter
lab_ldo3_vrc_enabling.pack()
lab_dcdc2_vrc_enabling.pack()
lab_ldo3_vra_vot_rising_slope.pack()
lab_dcdc2_vra_vot_rising_slope.pack()
#27dcdc3outvot
lab_dcdc3_vot.pack()
#28ldo2/4outvot
lab_ldo2_vot.pack()
lab_ldo4_vot.pack()
#29ldo3outvot
lab_ldo3_mode.pack()
lab_ldo3_vout.pack()
#30vbus-ipsout-channelmanagement
lab_vbus_ipsout_path_select.pack()
lab_vbus_vhold_vot_lim.pack()
lab_vhold_set.pack()
lab_vbus_cur_limit.pack()
#31voffshutdownvoltage
#????(b3)
lab_voff_set.pack()
#32shutdownsettingbattdetchgledcontr
#poffbit
lab_shutdown.pack()
lab_batt_mon_en.pack()
lab_chg_led_func.pack()
lab_chg_led_mode.pack()
lab_out_disable_time.pack()
lab_pon_key_time.pack()
#####################################################################################
#33chargingcontr1
lab_chg_enable.pack()
lab_chg_end_vot.pack()
lab_chg_end_cur.pack()
lab_chg_cur_set.pack()
#34chargingcontr2
lab_chg_pcg_timeout.pack()
lab_chg_chg_led.pack()
lab_chg_cc_timeout.pack()
#35bckbattchgcontr
lab_bchg_enable.pack()
lab_bchg_cv_end.pack()
lab_bchg_cc_set.pack()
#####################################################################################
#82 adc enable 1
lab_batt_vot_adc_en.pack()
lab_batt_cur_adc_en.pack()
lab_acin_vot_adc_en.pack()
lab_acin_cur_adc_en.pack()
lab_vbus_vot_adc_en.pack()
lab_vbus_cur_adc_en.pack()
lab_apss_vot_adc_en.pack()
lab_tsss_vot_adc_en.pack()
#83 adc enable 2
lab_its_adc_en.pack()
lab_gpio0_adc_en.pack()
lab_gpio1_adc_en.pack()

#adc data
lab_adc_val_acin_vot.pack()
lab_adc_val_acin_cur.pack()
lab_adc_val_vbus_vot.pack()
lab_adc_val_vbus_cur.pack()
lab_adc_val_ts_in.pack()
lab_adc_val_ts_ex.pack()
lab_adc_val_gpio0.pack()
lab_adc_val_gpio1.pack()
lab_adc_val_batt_inst_pwr.pack()
lab_adc_val_batt_vot.pack()
lab_adc_val_batt_chg_cur.pack()
lab_adc_val_batt_dsc_cur.pack()
lab_adc_val_ips_vot.pack()


def chk(a):
    if(a):
        return 1
    return 0
    pass

def task():
    nctx = 0;
    ser=serial.Serial("COM3",115200,timeout=5)
    print("串口详情参数：", ser)
    while(True):
        pstr = ""
        while(True):
            x = ser.read(1).decode("gbk")
            pstr = pstr + x
            if(x == '\n'):
                break
                pass
            pass
        #print(pstr)
        if(pstr[0] == 'X'):
            print("no conn" + " : " + str(nctx));
            nctx = nctx + 1
            continue
        else:
            nctx = 0
        pass
        hsii = '0x' + pstr[0]  + pstr[1]
        #print(pstr)
        regint = int(hsii,16)
        regstr = str(bin(int(hsii,16))[2:])
        #print(regstr)
        textvar_ACIN_presence.set("ACIN_presence" +" : "+ str(chk(regint & 0b10000000)))
        textvar_ACIN_useable.set("ACIN_useable" +" : "+ str(chk(regint & 0b01000000)))
        textvar_VBUS_presence.set("VBUS_presence" +" : "+ str(chk(regint & 0b00100000)))
        textvar_VBUS_useable.set("VBUS_useable" +" : "+ str(chk(regint & 0b00010000)))
        textvar_VBUS_above.set("VBUS_above" +" : "+ str(chk(regint & 0b00001000)))
        textvar_cur_dire.set("cur_dire" +" : "+ str(chk(regint & 0b00000100)))
        textvar_AC_VB_short.set("AC_VB_short" +" : "+ str(chk(regint & 0b00000010)))
        textvar_boot_sources.set("boot_sources" +" : "+ str(chk(regint & 0b00000001)))
        #reg 01h
        hsii = '0x' + pstr[2]  + pstr[3]
        regint = int(hsii,16)
        regstr = str(bin(int(hsii,16))[2:])
        #print(regstr)
        textvar_OT.set("OT" +" : "+ str(chk(regint & 0b10000000)))
        textvar_charge.set("charge" +" : "+ str(chk(regint & 0b01000000)))
        textvar_batt_exist.set("batt_exist" +" : "+ str(chk(regint & 0b00100000)))
        textvar_batt_activate.set("chg_cur_low" +" : "+ str(chk(regint & 0b00001000)))
        textvar_chg_cur_low.set("cur_dire" +" : "+ str(chk(regint & 0b00000100)))
        regstr=""
        for i in range(14*2):
            regstr = regstr + pstr[4+i]
            pass
        textvar_usrData.set("usrData" + " : " + regstr)
        #reg 12h
        hsii = '0x' + pstr[(0x12) * 2]  + pstr[((0x12) * 2) + 1]
        regint = int(hsii,16)
        regstr = str(bin(int(hsii,16))[2:])
        #print(regstr)
        textvar_ldo3_en.set("ldo3_en" +" : "+ str(chk(regint &   0b01000000)))
        textvar_dcdc2_en.set("dcdc2_en" +" : "+ str(chk(regint & 0b00010000)))
        textvar_ldo4_en.set("ldo4_en" +" : "+ str(chk(regint &   0b00001000)))
        textvar_ld02_en.set("ld02_en" +" : "+ str(chk(regint &   0b00000100)))
        textvar_dcdc3_en.set("dcdc3_en" +" : "+ str(chk(regint & 0b00000010)))
        textvar_exten_en.set("exten_en" +" : "+ str(chk(regint & 0b00000001)))
        #reg 23h
        hsii = '0x' + pstr[(0x23) * 2]  + pstr[((0x23) * 2) + 1]
        regint = int(hsii,16)
        regstr = str(bin(int(hsii,16))[2:])
        #print(regstr)
        textvar_dcdc2_vot.set("dcdc2_voltage" +" : "+ str(((regint & 0b00111111) * 0.025) + 0.7))
        #reg 27h
        hsii = '0x' + pstr[(0x27) * 2]  + pstr[((0x27) * 2) + 1]
        regint = int(hsii,16)
        regstr = str(bin(int(hsii,16))[2:])
        #print(regstr)
        textvar_dcdc3_vot.set("dcdc3_voltage" +" : "+ str(((regint & 0b01111111) * 0.025) + 0.7))
        #reg 28h
        hsii = '0x' + pstr[(0x28) * 2]  + pstr[((0x28) * 2) + 1]
        regint = int(hsii,16)
        regstr = str(bin(int(hsii,16))[2:])
        #print(regstr)
        textvar_ldo2_vot.set("ldo2_vot" +" : "+ str((((regint & 0b11110000)>>4) * 0.1) + 1.8))
        textvar_ldo4_vot.set("ldo4_vot(index)" +" : "+ str((regint & 0b00001111)))
        #reg 29h
        hsii = '0x' + pstr[(0x29) * 2]  + pstr[((0x29) * 2) + 1]
        regint = int(hsii,16)
        regstr = str(bin(int(hsii,16))[2:])
        #print(regstr)
        textvar_ldo3_mode.set("ldo3_mode" +" : "+ str(chk(regint & 0b10000000)))
        textvar_ldo3_vout.set("ldo3_vout" +" : "+ str((((regint & 0b01111111)) * 0.025) + 0.7))
        #reg 33h
        hsii = '0x' + pstr[(0x33) * 2]  + pstr[((0x33) * 2) + 1]
        regint = int(hsii,16)
        regstr = str(bin(int(hsii,16))[2:])
        #print(regstr)
        textvar_chg_enable.set("chg_enable" +" : "+ str(chk(regint &       0b10000000)))
        textvar_chg_end_vot.set("chg_end_vot(index)" +" : "+ str((regint &        0b01100000)>>5))
        textvar_chg_end_cur.set("chg_end_cur" +" : "+ str(chk(regint &     0b00010000)))
        textvar_chg_cur_set.set("chg_cur_set(mA)" +" : "+ str((((regint &  0b00001111)) * 100) + 300))

        #reg 82h
        hsii = '0x' + pstr[(0x82) * 2]  + pstr[((0x82) * 2) + 1]
        regint = int(hsii,16)
        regstr = str(bin(int(hsii,16))[2:])
        #print(regstr)
        textvar_batt_vot_adc_en.set("batt_vot_adc_en" +" : "+ str(chk(regint &   0b10000000)))
        textvar_batt_cur_adc_en.set("batt_cur_adc_en" +" : "+ str(chk(regint &   0b01000000)))
        textvar_acin_vot_adc_en.set("acin_vot_adc_en" +" : "+ str(chk(regint &   0b00100000)))
        textvar_acin_cur_adc_en.set("acin_cur_adc_en" +" : "+ str(chk(regint &   0b00010000)))
        textvar_vbus_vot_adc_en.set("vbus_vot_adc_en" +" : "+ str(chk(regint &   0b00001000)))
        textvar_vbus_cur_adc_en.set("vbus_cur_adc_en" +" : "+ str(chk(regint &   0b00000100)))
        textvar_apss_vot_adc_en.set("apss_vot_adc_en" +" : "+ str(chk(regint &   0b00000010)))
        textvar_tsss_vot_adc_en.set("tsss_vot_adc_en" +" : "+ str(chk(regint &   0b00000001)))

        #reg 83h
        hsii = '0x' + pstr[(0x83) * 2]  + pstr[((0x83) * 2) + 1]
        regint = int(hsii,16)
        regstr = str(bin(int(hsii,16))[2:])
        #print(regstr)
        textvar_its_adc_en.set("its_adc_en" +" : "+ str(chk(regint &       0b10000000)))
        textvar_gpio0_adc_en.set("gpio0_adc_en" +" : "+ str(chk(regint &   0b00001000)))
        textvar_gpio1_adc_en.set("gpio1_adc_en" +" : "+ str(chk(regint &   0b00000100)))

        #56 adc 2Byte
        baseaddr=(0x56) * 2
        hsii = '0x' + pstr[(baseaddr)]  + pstr[(baseaddr) + 1]+ pstr[(baseaddr) + 3]
        regint = int(hsii,16)
        regint = regint * 1.1 #vot lsv = 1.1mv
        textvar_adc_val_acin_vot.set("adc_val_acin_vot" +" : "+ str(regint))
        #58 adc 2Byte
        baseaddr=(0x58) * 2
        hsii = '0x' + pstr[(baseaddr)]  + pstr[(baseaddr) + 1]+ pstr[(baseaddr) + 3]
        regint = int(hsii,16)
        regint = regint * 0.5 #cur lsv = 0.5ma
        textvar_adc_val_acin_cur.set("adc_val_acin_cur" +" : "+ str(regint))
        #5a adc 2Byte
        baseaddr=(0x5a) * 2
        hsii = '0x' + pstr[(baseaddr)]  + pstr[(baseaddr) + 1]+ pstr[(baseaddr) + 3]
        regint = int(hsii,16)
        regint = regint * 1.1 #vot lsv = 1.1mv
        textvar_adc_val_vbus_vot.set("adc_val_vbus_vot" +" : "+ str(regint))
        #5c adc 2Byte
        baseaddr=(0x5c) * 2
        hsii = '0x' + pstr[(baseaddr)]  + pstr[(baseaddr) + 1]+ pstr[(baseaddr) + 3]
        regint = int(hsii,16)
        regint = regint * 0.5 #cur lsv = 0.5ma
        textvar_adc_val_vbus_cur.set("adc_val_vbus_cur" +" : "+ str(regint))
        #5e adc 2Byte
        baseaddr=(0x5e) * 2
        hsii = '0x' + pstr[(baseaddr)]  + pstr[(baseaddr) + 1]+ pstr[(baseaddr) + 3]
        regint = int(hsii,16)
        textvar_adc_val_ts_in.set("adc_val_ts_in" +" : "+ str(regint))
        #62 adc 2Byte
        baseaddr=(0x62) * 2
        hsii = '0x' + pstr[(baseaddr)]  + pstr[(baseaddr) + 1]+ pstr[(baseaddr) + 3]
        regint = int(hsii,16)
        textvar_adc_val_ts_ex.set("adc_val_ts_ex" +" : "+ str(regint))
        #64 adc 2Byte
        baseaddr=(0x64) * 2
        hsii = '0x' + pstr[(baseaddr)]  + pstr[(baseaddr) + 1]+ pstr[(baseaddr) + 3]
        regint = int(hsii,16)
        textvar_adc_val_gpio0.set("adc_val_gpio0" +" : "+ str(regint))
        #66 adc 2Byte
        baseaddr=(0x66) * 2
        hsii = '0x' + pstr[(baseaddr)]  + pstr[(baseaddr) + 1]+ pstr[(baseaddr) + 3]
        regint = int(hsii,16)
        textvar_adc_val_gpio1.set("adc_val_gpio1" +" : "+ str(regint))
        #70 adc 3Byte
        baseaddr=(0x70) * 2
        hsii = '0x' + pstr[(baseaddr)]  + pstr[(baseaddr) + 1]+ pstr[(baseaddr) + 2]+ pstr[(baseaddr) + 3]+ pstr[(baseaddr) + 4]+ pstr[(baseaddr) + 5]
        regint = int(hsii,16)
        textvar_adc_val_batt_inst_pwr.set("adc_val_batt_inst_pwr" +" : "+ str(regint))
        #78 adc 2Byte
        baseaddr=(0x78) * 2
        hsii = '0x' + pstr[(baseaddr)]  + pstr[(baseaddr) + 1]+ pstr[(baseaddr) + 3]
        regint = int(hsii,16)
        regint = regint * 1.1 #vot lsv = 1.1mv
        textvar_adc_val_batt_vot.set("adc_val_batt_vot" +" : "+ str(regint))
        #7a adc 2Byte
        baseaddr=(0x7a) * 2
        hsii = '0x' + pstr[(baseaddr)]  + pstr[(baseaddr) + 1]+ pstr[(baseaddr) + 3]
        regint = int(hsii,16)
        regint = regint * 0.5 #cur lsv = 0.5ma
        textvar_adc_val_batt_chg_cur.set("adc_val_batt_chg_cur" +" : "+ str(regint))
        #7c adc 2Byte
        baseaddr=(0x7c) * 2
        hsii = '0x' + pstr[(baseaddr)]  + pstr[(baseaddr) + 1]
        regint = int(hsii,16)<<5
        h7chsii = '0x' + pstr[(baseaddr)+2]  + pstr[(baseaddr) + 3]
        h7cregint = int(h7chsii,16) & 0b00011111
        regint = regint | h7cregint
        regint = regint * 0.5 #cur lsv = 0.5ma
        textvar_adc_val_batt_dsc_cur.set("adc_val_batt_dsc_cur" +" : "+ str(regint))
        #7e adc 2Byte
        baseaddr=(0x7e) * 2
        hsii = '0x' + pstr[(baseaddr)]  + pstr[(baseaddr) + 1]+ pstr[(baseaddr) + 3]
        regint = int(hsii,16)
        regint = regint * 1.1 #vot lsv = 1.1mv
        textvar_adc_val_ips_vot.set("adc_val_ips_vot" +" : "+ str(regint))



        #get_reg
        a = str(textvar_reg_get_adr.get())
        b = 0

        try:
            b=int(a,16)
        except Exception as e:
            pass
            #print(e)
        
        
        if(b > 0xff):
            b = 0xff

        varhex="0x%02x"%b
        b = b * 2
        hsii = '0x' + pstr[(b)]  + pstr[(b) + 1]
        textvar_reg_n_ret.set(varhex + " is " + hsii)


        global glo_req_set_addr
        global glo_req_set_data
        if(glo_req_set_data >= 0 and glo_req_set_addr >= 0):
            #print("w ad:%X   dt:%x"%(glo_req_set_addr,glo_req_set_data))
            textvar_reg_s_ret.set("write addr:%02x data:%02x"%(glo_req_set_addr,glo_req_set_data))
            writestr = "Q%03d%03dZ"%(glo_req_set_addr,glo_req_set_data)
            #print(writestr)
            #writefunc
            # 写数据
            result=ser.write(writestr.encode("gbk"))
            print("写总字节数:",result)
            pass


        glo_req_set_addr = -1
        glo_req_set_data = -1

    pass
pass

th = threading.Thread(target=task)
th.daemon = 1
th.start()

 
root.mainloop()
