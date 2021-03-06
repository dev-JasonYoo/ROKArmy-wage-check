#!/usr/bin/env python3.7
'''
Input: 
'ipdae'(the date of recruitment)

Ouptut:
'junyuk'(the date of discharging)
'total_days'(the number of days of entire service)
'first_and_last'(the list of significants dates: 'ipdae', the first and last days of each rank, and 'junyuk')
'days'(the list of the number of days during each rank)
'months'(the list of months during the service in the format of 'YYYY-MM')
'monthly_wage'(the actual final output: the list of monthly wages calculated by 'ipdae' and 'wage')

Constant:
'wage': two dimentional list of wages of corresponding years and ranks

Function:
'timedel2int(timedelta)'
'first_day_month(a_day)'
'last_day_month(a_day)'
'month2wage(value_in_month_list)'
'rankis(value_in_month_list)'
'month2wage_list(month_list)'
'''

from  dateutil.relativedelta import *
import datetime
import calendar

def main(response,jn23,jn34):
    global ipdae, junyuk, total_days, first_and_last, wage, months, monthly_wage, jinnu23, jinnu34, prmt12, prmt23, prmt34
#   ipdae = datetime.date.fromisoformat(input("입대일을 YYYY-MM-DD 형식으로 입력해주세요\n"))
    ipdae = datetime.date.fromisoformat(response)
    junyuk = ipdae+relativedelta(years=+1,months=+6,days=-1)
    total_days = str(junyuk - ipdae).split(',')[0]
    jinnu23 = int(float(jn23))
    jinnu34 = int(float(jn34))
    
    prmt12 = 3
    prmt23 = prmt12 + 6 + jinnu23    #or = 9 + jinnu23
    prmt34 = prmt23 + 6 + jinnu34    #or = 15 + jinnu23 + jinnu34 

    print("전역일은 {}입니다.".format(junyuk))
    print("총 복무일은 {}일입니다\n".format(total_days[:-5]))


    #first_and_last: the list contains significant dates(ipdae day, first and last days of each rank, and junyuk day)
    #should be edited to consider promotion failed
    last_day1 = last_day_month(ipdae + relativedelta(months=+2))

    first_day2 = last_day1 + relativedelta(days=+1)
    last_day2 = last_day_month(ipdae + relativedelta(months=+8+jinnu23))

    first_day3 = last_day2 + relativedelta(days=+1)
    last_day3 = last_day_month(ipdae + relativedelta(months=+14+jinnu23+jinnu34))

    first_day4 = last_day3 + relativedelta(days=+1)

    first_and_last = [ipdae, last_day1, first_day2, last_day2, first_day3, last_day3, first_day4, junyuk]

    # days[i] : Total service days as a private(이병, i=0), priavte first class(일병, i=1), specialist(상병, i=2), and coporal(병장, i=4).
    days = [0 for i in range(8)]

    for v0 in range(0, 8, 2) :
        days[v0//2] = first_and_last[v0+1] - first_and_last[v0]

    for i in range(8) :
        print(first_and_last[i])

    #wage[year][rank]: wage of each rank during each year
    #year: a number of year after 2019
    #ex) 2021 --> i=2
    #rank: monthly wage of each rank
    #rank=0 --> priavate(이병), j=1 --> priavte first class(일병), j=2 --> specialist(상병), j=3 --> corporal(병장)
    wage=[]
    wage.append([306100, 331300, 366200, 405700]) # wage[0]: 2019
    wage.append([408100, 441700, 488200, 540900]) # wage[1]: 2020
    wage.append([459100, 496900, 549200, 608500]) # wage[2]: 2021
    wage.append([510100, 552100, 610200, 676100]) # wage[3]: 2022
    wage.append([544600, 593000, 655700, 726100]) # wage[4]: 2023 estimated
    wage.append([631100, 687200, 759800, 841400]) # wage[5]: 2024 estimated
    wage.append([722300, 786500, 869600, 963000]) # wage[6]: 2025 estimated

    print(wage)

    months = [str(ipdae + relativedelta(month=i))[:-3] for v0 in range(19)]

    #months[i]: Each element is a i-th month during the service in the for mat of 'YYYY-MM'.
    months = [str(ipdae + relativedelta(months=i))[:-3] for i in range(19)]

    print(months)
    monthly_wage = []
    month2wage_list(months)
    
    print(monthly_wage)
    print("The sum is ", sum(monthly_wage))
    print (monthly_wage)

    f = open("/ROKArmy-wage-check/ROKArmy-wage-check/templates/result.html", 'r')
    result = f.read()
    
    return result.format(junyuk, total_days[:-5], first_and_last[0], first_and_last[1], first_and_last[2], first_and_last[3], first_and_last[4], first_and_last[5], first_and_last[6], first_and_last[7], wage, months, sum(monthly_wage), monthly_wage)



#---------------------------Below are component functions for 'main()' function.---------------------------


#A function that changes 'timedelta' object in the format of '%d days, 0:00:00 into int type which only contains the number of days.
def timedel2int(timedelta) :
    return int(str(timedelta)[:-14])

#A function that returns datetime object of the first day of the input month.
def first_day_month(a_day) :
    a_day = a_day.replace(day=1)
    return a_day

#A function that returns datetime object of the last day of the input month.
def last_day_month(a_day) :
    a_day = a_day.replace(day=calendar.monthrange(a_day.year,a_day.month)[1])
    return a_day

#month2wage_list(month_list): gets a list of the month during service and appends a wage of each input month to 'monthly_wage'
def month2wage_list(month_list) :
    
    global monthly_wage
    monthly_wage=[]
    
    for i in range(len(month_list)):
        if i==0 :
            proportion = ((int(str(last_day_month(ipdae) - ipdae)[:2]))+1)/int(str(last_day_month(ipdae))[-2:])
            monthly_wage.append(proportion * month2wage(month_list[i]))
        elif i==18 :
            proportion = ((int(str(junyuk - first_day_month(junyuk))[:2]))+1)/int(str(last_day_month(junyuk))[-2:])
            monthly_wage.append(proportion * month2wage(month_list[i]))
        else :
            monthly_wage.append(month2wage(month_list[i]))

#month2wage(value_in_month_list): returns corresponding wage of input month(depending on a year and rank)
def month2wage(value_in_month_list) :
    year = int(value_in_month_list[:4])-2019
    rank = rankis(value_in_month_list)
    return wage[year][rank]

#rankis(value_in_month_list): determines a rank corresponding to the input month
def rankis(value_in_month_list) :
    index = months.index(value_in_month_list)
    
    if 0<=index<prmt12 :
        return 0
    if prmt12<=index<prmt23 :
        return 1
    if prmt23<=index<prmt34 :
        return 2
    if prmt34<=index<=18 :
        return 3
