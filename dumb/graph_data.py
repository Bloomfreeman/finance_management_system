import callculate as CL
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

try:
    import mplcursors
except ImportError:
    mplcursors = None

#imported data
data,goal,last_monthly_entry=CL.Refresh()
Life_saving, Consumption, Operation, debtpayed=CL.callculate(data)

#time
current_time = datetime.now()

def graph_for_the_past():
    global last_monthly_entry
    wage=[row[0] for row in last_monthly_entry[-6:]]
    ls_saving=[row[1] for row in last_monthly_entry[-6:]]
    cs_saving=[row[2] for row in last_monthly_entry[-6:]]
    date=[row[4] for row in last_monthly_entry[-6:]]
    
    return date, ls_saving, cs_saving


def graph_by_month():
    global current_time, last_monthly_entry,goal
    predicted_ls, predicted_cs, debt_left,last_month_entry=CL.year_long_predictive_data(last_monthly_entry)
    inmonthls=inmonthcs=inmonthdb=None
    if goal['LSgoal'] in predicted_ls:
        inmonthls=predicted_ls.index(goal['LSgoal'])
    if goal['CSgoal'] in predicted_cs:
        inmonthcs=predicted_cs.index(goal['CSgoal'])
    if 0 >= debt_left[-1]:
        inmonthdb=len(debt_left)-1
    the_end_of_mounth=(12-int(current_time.strftime("%m")))+1
    months = [current_time + relativedelta(months=i) for i in range(the_end_of_mounth)]
    Clean_months=[month.strftime("%Y-%m") for month in months]
    ls_monthly_prepared_month=Clean_months[:the_end_of_mounth]
    # dt_graph=line_graph(ls_monthly_prepared_month[:len(debt_left[:the_end_of_mounth])], debt_left[:the_end_of_mounth])
    return ls_monthly_prepared_month,predicted_ls[:the_end_of_mounth],predicted_cs[:the_end_of_mounth],debt_left[:the_end_of_mounth]

def graph_by_year(needed_year=30):
    global current_time, Ypredicted_ls, goal
    the_end_of_year=(needed_year-int(current_time.strftime("%y")))+1
    Ypredicted_ls, Ypredicted_cs, Ydebt_left=CL.years_long_predictive_data(the_end_of_year)
    # inyearls=inyearcs=inyeardb=None
    # if goal['LSgoal'] in Ypredicted_ls:
    #     inyearls=Ypredicted_ls.index(goal['LSgoal'])
    # if goal['CSgoal'] in Ypredicted_cs:
    #     inyearcs=Ypredicted_cs.index(goal['CSgoal'])
    # if 0 >= Ydebt_left[-1]:
    #     inyeardb=len(Ydebt_left)-1

    years = [current_time + relativedelta(years=i) for i in range(the_end_of_year)]
    Clean_years=[year.strftime("%Y") for year in years]
    ls_monthly_prepared_month=Clean_years[:the_end_of_year]
    
    return ls_monthly_prepared_month[:the_end_of_year], Ypredicted_cs[:the_end_of_year], Ypredicted_ls[:the_end_of_year]

def goal_bar():
    global goal, last_monthly_entry
    LS_diff, CS_diff, LS_percent, CS_percent=CL.callculate_goal(goal, last_monthly_entry)

    return LS_diff, CS_diff, LS_percent, CS_percent,goal['LSgoal'], goal['CSgoal']


if __name__ == "__main__":
    # b=graph_by_month()
    # print(b)
    # a=graph_by_year(30)
    # print(a)
    c=graph_by_month()
    print(c)