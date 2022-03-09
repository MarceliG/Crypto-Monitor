from download_data import DataMonitor

btc = DataMonitor().GetCurrentData()

print(btc['time'].iloc[-1])