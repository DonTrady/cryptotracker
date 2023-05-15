from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

def create_tab2(tab_widget):
    tab2 = QWidget()
    layout2 = QVBoxLayout(tab2)
    web = QWebEngineView()
    html = """
    <!DOCTYPE html>
    <html>
    <body>
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
        <div id="tradingview_1234"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
    new TradingView.widget(
    {
    "width": 980,
    "height": 610,
    "symbol": "BINANCE:ETHUSDT",
    "interval": "M",
    "timezone": "Etc/UTC",
    "theme": "light",
    "style": "1",
    "locale": "en",
    "toolbar_bg": "#f1f3f6",
    "enable_publishing": false,
    "allow_symbol_change": true,
    "container_id": "tradingview_1234"
    }
    );
    </script>
</div>
<!-- TradingView Widget END -->
</body>
</html>
"""
    web.setHtml(html)
    layout2.addWidget(web)
    tab_widget.addTab(tab2, "Chart")
