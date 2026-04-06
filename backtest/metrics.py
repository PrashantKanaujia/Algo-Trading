from backtest.engine import run_backtest

l=[]
for i in range(0,50):
    l.append(run_backtest(i))

print(l)
print(max(l))

# cd=20to30