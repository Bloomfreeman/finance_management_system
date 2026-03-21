import RD
import CJ  


global_ls_saving=0
global_cs_saving=0
global_debt_payment=0
def Refresh():
    data = RD.get_data()
    goal= RD.get_goal()
    last_monthly_enty=RD.get_one_data_per_month()
    return data, goal, last_monthly_enty

def callculate(data: list, life_saving_rate: float=0.25, consumption_rate: float=0.50, debt_payment_rate: float=0.10):
    global global_ls_saving, global_cs_saving, global_debt_payment
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
    global_ls_saving,global_cs_saving,global_debt_payment=Lsaved,Csaved,debtpayment
    return Life_saving, Consumption, Operation, debtpayed

def callculate_goal(goal: dict):
    global global_ls_saving, global_cs_saving
    LSgoal=goal['LSgoal']
    CSgoal=goal['CSgoal']
    Life_saving, Consumption= global_ls_saving, global_cs_saving
    LS_percent=(Life_saving/LSgoal)*100 if LSgoal != 0 else 0
    CS_percent=(Consumption/CSgoal)*100 if CSgoal != 0 else 0
    LS_diff=LSgoal-Life_saving
    CS_diff=CSgoal-Consumption
    return LS_diff, CS_diff, LS_percent, CS_percent

def year_long_predictive_data(last_mounth_entry):
    global global_ls_saving, global_cs_saving, global_debt_payment
    ls_saving, cs_saving,debt=last_mounth_entry[-1][1], last_mounth_entry[-1][2], last_mounth_entry[-1][3]
    predicted_ls=[]
    predicted_cs=[]
    debt_left=[]
    for _ in range(7):
        if debt >= 0:
            debt-=global_debt_payment
            ls_saving+=global_ls_saving
            cs_saving+=global_cs_saving
            debt_left.append(debt)
            predicted_ls.append(ls_saving)
            predicted_cs.append(cs_saving)
        else:
            ls_saving+=global_ls_saving
            cs_saving+=(global_cs_saving+debt)
            predicted_ls.append(ls_saving)
            predicted_cs.append(cs_saving)
    return last_mounth_entry, predicted_ls, predicted_cs, debt_left

def Push_data():
    data, goal = Refresh()
    ready_to_push=callculate(data, goal['Life_saving_rate'], goal['consumption_rate'])
    CJ.Update_data(currentLs=ready_to_push[0], currentCs=ready_to_push[1], debt=ready_to_push[3])


if __name__ == "__main__":
    # CJ.update_data(debt=1000)
    # CJ.change_goal(LSgoal=1_000_000, CSgoal=50_000)
    # print(RD.get_One_data_per_mouth())
    # CJ.init_data(LSgoal=1_000_000, CSgoal=50_000, Life_saving_rate=0.25, consumption_rate=0.50, debt_payment_rate=0.10)
    data, goal ,last_monthly_entry= Refresh()
    # print("Data:", data)
    # print("Goal:", goal)
    a=callculate(data, goal['Life_saving_rate'], goal['consumption_rate'], goal['debt_payment_rate'])
    print("Ready to push:", a)
    c=year_long_predictive_data(last_monthly_entry, goal)
    print("Predicted data for the next 6 months:", c)
    # b=callculate_goal(data, goal)
    # print("Goal difference and percentage:", b)