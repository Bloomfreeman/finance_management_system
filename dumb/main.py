import webview
import CJ

#I'm too lazy to fix it properly so we'er stick with this for now
if CJ.table_exists("Cd.db","users"):
    pass
else:
    CJ.create_data()
    CJ.Put_data(1000,1000,1000,0)
    CJ.Put_data(1000,1000,1000,0)
import graph_data   # compiled .pyd
import callculate as cl

class API:
    def goal_data(self):
        return graph_data.goal_bar()
    
    def graph_by_year(self):
        return graph_data.graph_by_year(35)
    def graph_by_month(self):
        return graph_data.graph_by_month()
    
    def graph_for_the_past(self):
        return graph_data.graph_for_the_past()
    def refresh(self):
        return cl.Refresh()
    def call(self):
        data, goal ,last_monthly_entry= cl.Refresh()
        wage,Lsaved, Csaved, debtpayment, operation=cl.callculate(data, goal['Life_saving_rate'], goal['consumption_rate'], goal['debt_payment_rate'],get_me_row=True)
        Life_saving, Consumption, Operation, debtpayed=cl.callculate(data, goal['Life_saving_rate'], goal['consumption_rate'], goal['debt_payment_rate'],get_me_row=False)
        return wage,Lsaved, Csaved, debtpayment, operation, Life_saving, Consumption
    def update_json(self,LSgoal: float=None, CSgoal: float=None, Life_saving_rate: float=None, consumption_rate: float=None, debt_payment_rate: float=None):
        CJ.change_goal(LSgoal=LSgoal, CSgoal=CSgoal, Life_saving_rate=Life_saving_rate, consumption_rate=consumption_rate, debt_payment_rate=debt_payment_rate)
    def update_Data(self,wage: float=None, currentLs: float=None, currentCs: float=None, debt: float=None):
        CJ.update_data(wage=wage, currentLs=currentLs, currentCs=currentCs, debt=debt)
    def save(self):
        cl.Push_data()
        graph_data.data,graph_data.goal,graph_data.last_monthly_entry=cl.Refresh()

api = API()

webview.create_window(
    "FinanceFlow",
    "index.html",
    js_api=api,
    width=1600,
    height=900
)

# webview.start(debug=True)
webview.start()