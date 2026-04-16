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
    wage_graph=line_graph(date, wage)
    ls_graph=line_graph(date, ls_saving)
    cs_graph=line_graph(date, cs_saving)
    return wage_graph, ls_graph, cs_graph


def graph_by_month():
    global current_time, last_monthly_entry,goal
    predicted_ls, predicted_cs, debt_left=CL.year_long_predictive_data(last_monthly_entry)
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
    ls_graph=line_graph(ls_monthly_prepared_month, predicted_ls[:the_end_of_mounth])
    cs_graph=line_graph(ls_monthly_prepared_month, predicted_cs[:the_end_of_mounth])
    dt_graph=line_graph(ls_monthly_prepared_month[:len(debt_left[:the_end_of_mounth])], debt_left[:the_end_of_mounth])
    return ls_graph, cs_graph, dt_graph, inmonthls, inmonthcs, inmonthdb

def graph_by_year(needed_year):
    global current_time, Ypredicted_ls, goal
    the_end_of_year=(needed_year-int(current_time.strftime("%y")))+1
    Ypredicted_ls, Ypredicted_cs, Ydebt_left=CL.years_long_predictive_data(the_end_of_year)
    inyearls=inyearcs=inyeardb=None
    if goal['LSgoal'] in Ypredicted_ls:
        inyearls=Ypredicted_ls.index(goal['LSgoal'])
    if goal['CSgoal'] in Ypredicted_cs:
        inyearcs=Ypredicted_cs.index(goal['CSgoal'])
    if 0 >= Ydebt_left[-1]:
        inyeardb=len(Ydebt_left)-1

    years = [current_time + relativedelta(years=i) for i in range(the_end_of_year)]
    Clean_years=[year.strftime("%Y") for year in years]
    ls_monthly_prepared_month=Clean_years[:the_end_of_year]
    ls_graph=line_graph(ls_monthly_prepared_month, Ypredicted_ls[:the_end_of_year])
    cs_graph=line_graph(ls_monthly_prepared_month, Ypredicted_cs[:the_end_of_year])
    return ls_graph, cs_graph, inyearls, inyearcs, inyeardb

def goal_bar(width, height):
    global goal, last_monthly_entry
    LS_diff, CS_diff, LS_percent, CS_percent=CL.callculate_goal(goal, last_monthly_entry)
    ls_bar=upward_bar(LS_percent,width, height)
    cs_bar=upward_bar(CS_percent,width, height)
    return ls_bar, cs_bar, LS_diff, CS_diff


def line_graph(x,data):
    fig = Figure(figsize=(5,4), dpi=100)
    ax= fig.add_subplot(111)

    x=x
    y=data

    ax.plot(x,y)
    ax.set_title('Predicted Savings Over Time')
    ax.set_xlabel('Month')
    ax.set_ylabel('Value')
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation=45)  # Rotate x-axis labels for better readability
    ax.grid(True)  # Add grid

    # Add hover tooltips if mplcursors is available
    if mplcursors:
        cursor = mplcursors.cursor(ax, hover=True)
        @cursor.connect("add")
        def on_add(sel):
            idx = int(sel.target[0])  # Index of the data point
            month_label = x[idx] if idx < len(x) else "N/A"
            y_val = sel.target[1]
            sel.annotation.set_text(f'Month: {month_label}\nValue: {y_val:.2f}')

    return fig

def upward_bar(persentage=None,width=50, height=200):
    if persentage is None:
        raise ValueError("Percentage value is required to create the bar.")

    canvas_width = width
    canvas_height = height
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='black')
    if persentage <= 40:
        color='red'
    elif persentage <=75:
        color='yellow'
    elif persentage >75:
        color='purple'

    fill_rect = canvas.create_rectangle(0, canvas_height, canvas_width, canvas_height, fill=color)
    text = canvas.create_text(canvas_width/2, canvas_height/2, text=f"{persentage:.1f}%", fill="white", font=("Arial", 8))
    progress =persentage
    fill_height=(progress/100)*canvas_height
    canvas.coords(fill_rect, 0, canvas_height-fill_height, canvas_width, canvas_height)
    return canvas

if __name__ == "__main__":
    root =tk.Tk()
    root.title("Graph Example")
    a,b,c,d=goal_bar(50,50)
    a.pack(side="left", padx=10)
    b.pack(side="right", padx=10)
    # fig,fi,f,a,b,c=graph_by_month()
    # print(a,b,c)
    # canvas = FigureCanvasTkAgg(f, master=root)
    # canvas.draw()
    # canvas.get_tk_widget().pack(fill="both",expand=True)
    root.mainloop()
    