import webview

import graph_data   # compiled .pyd

class API:
    def get_total(self):
        return graph_data.goal_bar()

api = API()

webview.create_window(
    "FinanceFlow",
    "index.html",
    js_api=api,
    width=1600,
    height=900
)

webview.start()