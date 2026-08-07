import RD
import CJ  


global_ls_saving=0
global_cs_saving=0
global_debt_payment=0
is_set=False
def Refresh():
    data = RD.get_data()
    goal= RD.get_goal()
    last_monthly_enty=RD.get_one_data_per_month()
    return data, goal, last_monthly_enty

def callculate(data: list, life_saving_rate: float=0.25, consumption_rate: float=0.50, debt_payment_rate: float=0.10,get_me_row=False):
    global global_ls_saving, global_cs_saving, global_debt_payment, is_set
    wage = data[-1][0]
    currentLs = data[-1][1]
    currentCs = data[-1][2]
    debt = data[-1][3]
    Lsaved=wage*life_saving_rate
    Csaved_without_debt=wage*consumption_rate
    if debt > 0:
        if Csaved_without_debt*debt_payment_rate > debt:
            Csaved=Csaved_without_debt-debt
        else:
            Csaved=Csaved_without_debt*(1-debt_payment_rate)
    else:
        Csaved=Csaved_without_debt

    debtpayment=Csaved_without_debt-Csaved
    debtpayed=debt-debtpayment
    if life_saving_rate + consumption_rate == 1:
        raise ValueError("You can't save 100% of your wage, you need to consume something.")

    Life_saving=currentLs+Lsaved
    Consumption=currentCs+Csaved
    Operation=wage-(Lsaved+Csaved_without_debt)
    global_ls_saving,global_cs_saving,global_debt_payment,is_set=Lsaved,Csaved,debtpayment,True
    if get_me_row:
        return wage,Lsaved, Csaved, debtpayment,Operation
    return Life_saving, Consumption, Operation, debtpayed

def callculate_goal(goal: dict, last_monthly_entry):
    LSgoal=goal['LSgoal']
    CSgoal=goal['CSgoal']
    LS_percent=(last_monthly_entry[-1][1]/LSgoal)*100 if LSgoal != 0 else 0
    CS_percent=(last_monthly_entry[-1][2]/CSgoal)*100 if CSgoal != 0 else 0
    LS_diff=LSgoal-last_monthly_entry[-1][1]
    CS_diff=CSgoal-last_monthly_entry[-1][2]
    return LS_diff, CS_diff, LS_percent, CS_percent

def year_long_predictive_data(last_mounth_entry):
    global global_ls_saving, global_cs_saving, global_debt_payment, is_set
    if not is_set:
        raise ValueError("Important callculation parameters are not set. Please run the callculate function first to set the global variables.")
    ls_saving, cs_saving,debt=last_mounth_entry[-1][1], last_mounth_entry[-1][2], last_mounth_entry[-1][3]
    predicted_ls=[]
    predicted_cs=[]
    debt_left=[]
    for _ in range(13):
        if debt > 0:
            debt-=global_debt_payment
            ls_saving+=global_ls_saving
            cs_saving+=global_cs_saving
            debt_left.append(debt)
            predicted_ls.append(ls_saving)
            predicted_cs.append(cs_saving)
        else:
            ls_saving+=global_ls_saving
            cs_saving+=(global_cs_saving+global_debt_payment)
            predicted_ls.append(ls_saving)
            predicted_cs.append(cs_saving)
    return predicted_ls, predicted_cs, debt_left,last_mounth_entry

def years_long_predictive_data( years=5):
    predicted_Lss, predicted_Css, debt_Lefts,last_monthly_entry=year_long_predictive_data(RD.get_one_data_per_month())
    ls_saving, cs_saving,debt=last_monthly_entry[-1][1], last_monthly_entry[-1][2], last_monthly_entry[-1][3]
    ls_diff=predicted_Lss[-1]-last_monthly_entry[-1][1]
    cs_diff=predicted_Css[-1]-last_monthly_entry[-1][2]
    debt_diff=last_monthly_entry[-1][3]-debt_Lefts[-1]
    predicted_ls=[]
    predicted_cs=[]
    debt_left=[]
    for _ in range(years):
        if debt > 0 and debt_diff <= debt:
            debt-=debt_diff
            ls_saving+=ls_diff
            cs_saving+=cs_diff
            debt_left.append(debt)
            predicted_ls.append(ls_saving)
            predicted_cs.append(cs_saving)
        else:
            ls_saving+=ls_diff
            cs_saving+=(cs_diff+debt_diff)
            predicted_ls.append(ls_saving)
            predicted_cs.append(cs_saving)
    
    return predicted_ls, predicted_cs, debt_left


def Push_data():
    data, goal,last_monthly_entry = Refresh()
    ready_to_push=callculate(data, goal['Life_saving_rate'], goal['consumption_rate'], goal['debt_payment_rate'],get_me_row=False)
    CJ.update_data(currentLs=ready_to_push[0], currentCs=ready_to_push[1], debt=ready_to_push[3])


if __name__ == "__main__":
    # CJ.update_data(debt=1000)
    # CJ.change_goal(LSgoal=1_000_000, CSgoal=50_000)
    # print(RD.get_One_data_per_mouth())
    # CJ.init_data(LSgoal=1_000_000, CSgoal=50_000, Life_saving_rate=0.25, consumption_rate=0.50, debt_payment_rate=0.10)
    data, goal ,last_monthly_entry= Refresh()
    # print("Data:", data)
    # print("Goal:", goal)
    a=callculate(data, goal['Life_saving_rate'], goal['consumption_rate'], goal['debt_payment_rate'])
    # print("Ready to push:", a)
    c=year_long_predictive_data(last_monthly_entry)
    print("Predicted data for the next 6 months:", c)
    # b=callculate_goal(data, goal)
    # print("Goal difference and percentage:", b)
    d=years_long_predictive_data(10)
    print("Predicted data for the next 10 years:", d)