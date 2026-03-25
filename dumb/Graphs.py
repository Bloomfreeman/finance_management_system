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

data,goal,last_monthly_entry=CL.Refresh()
CL.callculate(data)
last_mounth_entry, predicted_ls, predicted_cs, debt_left=CL.year_long_predictive_data(last_monthly_entry)


current_time = datetime.now()
the_end_of_mounth=(12-int(current_time.strftime("%m")))+1
months = [current_time + relativedelta(months=i) for i in range(the_end_of_mounth)]
Clean_months=[month.strftime("%Y-%m") for month in months]
ls_monthly_prepared_month=Clean_months[:the_end_of_mounth]
ls_monthly_prepared_data = predicted_ls[:the_end_of_mounth]

def graph_by_month():
    global ls_monthly_prepared_data,Clean_months
    fig = Figure(figsize=(5,4), dpi=100)
    ax= fig.add_subplot(111)

    x=Clean_months
    y=ls_monthly_prepared_data

    ax.plot(x,y)
    ax.set_title('Graph by month')
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


if __name__ == "__main__":
    root =tk.Tk()
    root.title("Graph Example")

    fig=graph_by_month()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both",expand=True)

    root.mainloop()