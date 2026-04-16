import webview

import graph_data   # compiled .pyd
import callculate as cl
class API:
    def goal_data(self):
        return graph_data.goal_bar()
    
    def graph_by_year(self):
        return graph_data.graph_by_year(35)
    
    def graph_for_the_past(self):
        return graph_data.graph_for_the_past()
    def refresh(self):
        return cl.Refresh()
    def call(self):
        data, goal ,last_monthly_entry= cl.Refresh()
        wage,Lsaved, Csaved, debtpayment, operation=cl.callculate(data, goal['Life_saving_rate'], goal['consumption_rate'], goal['debt_payment_rate'],get_me_row=True)
        return wage,Lsaved, Csaved, debtpayment, operation

api = API()

webview.create_window(
    "FinanceFlow",
    "index.html",
    js_api=api,
    width=1600,
    height=900
)

webview.start()