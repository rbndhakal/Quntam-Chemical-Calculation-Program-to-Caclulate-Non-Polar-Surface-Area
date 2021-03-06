import os
import sys
import pandas as pd
def main():
        print("******************************************************")
        print("*                                                    *")
        print("*       CS-NPSA CALCULATION PROGRAM Vers. 1.0        *")
        print("*                                                    *")
        print("*                   Rabin Dhakal                     *")
        print("*                                                    *")
        print("*             Texas Tech University                  *")
        print("*                                                    *")
        print("******************************************************")
        print("\n\nTHIS PROGRAM CALCULATES THE NON POLAR SURFACE AREA\nFROM THE OUTPUT FILE GENERATED BY TURBOMOLE")
        print("THE OUTPUT OF THIS PROGRAM IS GENERATED IN TEXT FILE")

        out_source = True
        while out_source == True:
            print("\nEnter source of output to be analyzed: Turbomole or ORCA")
            Program=str(input())
            if Program =='Turbomole':
                test_file = True
                out_source = False
                while test_file == True:
                    print("\nEnter file name")
                    x=str(input())
                    test_file=False
                    try:
                        f = open(x,'r')
                    except EnvironmentError as e:
                        print("The file doesnot exist!\n")
                        test_file = True
                    line_num = 0
                    search_phrase = "$segment_information"
                    for line in f.readlines():
                        line_num += 1
                        if line.find(search_phrase) >= 0:
                            break


                    data = pd.read_csv(x,skiprows=line_num,comment='#',float_precision='round_trip', header=None, delim_whitespace=True)

                    print("Enter the value of threshold:")
                    threshold_loop = True
                    while threshold_loop == True:
                        threshold =input()
                        threshold= float(threshold)
                        if abs(threshold) > 0.1 :
                            print("Enter the value less than 0.1")
                            threshold_loop = True
                        else:
                            threshold_loop = False


                    data_new = data.iloc[:,[1,5,6,7]]  #getting required data from turbomole output
                    data_new.columns = ['atoms','charge','area','Tm_charge_per_area']

                    temp0 = data_new[abs(data_new['charge'])<threshold]
                    npsa0 = temp0.sum()
                    ser0 = pd.Series(npsa0)

                    all_data_sum = data_new.sum()   #taking output from Tmole data
                    ser1 = pd.Series(all_data_sum)

                    temp1 = data_new[abs(data_new['Tm_charge_per_area'])<threshold]
                    npsa1 = temp1.sum()    #NPSA calculation applying threshold on each segments
                    ser2 = pd.Series(npsa1)


                    y = data_new.groupby("atoms").sum() #grouping data for new method of calculation of NPSA
                    Sum_y = y.sum()
                    ser3 = pd.Series(Sum_y)

                    temp2 = y[abs(y['charge'])<threshold]


                    npsa4 = temp2.sum()
                    ser5 = pd.Series(npsa4)

                    y['charge_per_area'] = y['charge'] / y['area']
                    temp =y[abs(y['charge_per_area']<threshold)]
                    npsa2 = temp.sum()

                    ser4 = pd.Series(npsa2)

                    print("\nThe value of NPSA with threshold {} is : {} ".format(threshold,ser2[2]) , file = open("npsa.txt","a"))

                    print("\nThe value of total area is :{} ".format(ser1[2]) , file = open("npsa.txt","a"))

                    pd.set_option("display.max_rows", None, "display.max_column", None)

                    print("\nUnits:\n      Charge : e\n      Area : A^2\n      charge per area : e/A^2\n      threshold : e/A^2\n" ,                                   file=open("npsa.txt","a"))

                    print("\nThe calculated charge and area of  atoms are given below :\n " , file = open("npsa.txt","a"))

                    print("\n        charge     area     charge per area", file = open("npsa.txt","a"))

                    del y['Tm_charge_per_area']

                    y.columns = [''] * len(y.columns)

                    print(y, file=open("npsa.txt","a"))



            elif Program == 'ORCA':
                out_source = False
                test_file = True
                while test_file == True:
                    print("\nEnter file name")
                    x=str(input())
                    test_file=False
                    try:
                        f = open(x,'r')
                    except EnvironmentError as e:
                        print("The file doesnot exist!\n")
                        test_file = True
                    line_num = 0
                    search_phrase = "# SURFACE POINTS"
                    for line in f.readlines():
                        line_num += 1
                        if line.find(search_phrase) >= 0:
                            break


                    data = pd.read_csv(x,skiprows=line_num+2,comment='#',float_precision='round_trip', header=None, delim_whitespace=True)

                    print("Enter the value of threshold:")
                    threshold_loop = True
                    while threshold_loop == True:
                        threshold =input()
                        threshold= float(threshold)
                        if abs(threshold) > 0.1 :
                            print("Enter the value less than 0.1")
                            threshold_loop = True
                        else:
                            threshold_loop = False


                    data_new = data.iloc[:,[3,4,5,6]]  #getting required data from turbomole output
                    data_new.columns = ['area','potential','charge','atoms']
                    data_new['area'] = data_new['area']*0.2800285609

                    all_data_sum = data_new.sum()   #taking output from orca data
                    ser1 = pd.Series(all_data_sum)

                    data_new['charge_per_area'] = data_new.apply(lambda row: row.charge / row.area, axis=1)

                    temp1 = data_new[abs(data_new['charge_per_area'])<threshold]
                    npsa1 = temp1.sum()    #NPSA calculation applying threshold on each segments
                    ser2 = pd.Series(npsa1)

                    y = data_new.groupby("atoms").sum() #grouping data based on atoms


                    print("\nThe value of NPSA with threshold {} is : {} ".format(threshold,ser2[0]) , file = open("npsa.txt","a"))

                    print("\nThe value of total area is :{} ".format(ser1[0]) , file = open("npsa.txt","a"))

                    pd.set_option("display.max_rows", None, "display.max_column", None)

                    print("\nUnits:\n      Charge : e\n      Area : A^2\n      charge per area : e/A^2\n      threshold : e/A^2\n" , file=open("npsa.txt","a"))

                    print("\nThe calculated charge and area of  atoms are given below :\n" , file = open("npsa.txt","a"))

                    print("\n         area      charge  charge per area", file = open("npsa.txt","a"))

                    del y['potential']

                    y.columns = [''] * len(y.columns)

                    print(y, file=open("npsa.txt","a"))


            else:
                print("\nYou have entered wrong source program name")
                out_source = True




if __name__ == "__main__":

            main()