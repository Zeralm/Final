import pandas as pd
import storage
import datetime
import os

u = os.listdir("C:/Users/DAVID/Desktop/Box")
true_length = 0
lengths = []
for kw in range(len(u)):
    data = pd.read_csv(os.path.join("C:/Users/DAVID/Desktop/Box", u[kw]))
    true_length += len(data)
    lengths.append(len(data))
    dates = pd.Series(data["Accepted at"])
    for r in range(len(data["Accepted at"])):
        
        dates[r] = datetime.datetime.strptime(data["Accepted at"].iloc[r][0:10],"%Y-%m-%d").date()
    data["Accepted at"] = dates
    k = data.loc[:,["Company","Filing","Industry","State","City","Money raised","Offered for sale","Accepted at"]].values
    storage.add_fundings(k)
    print("{}% completed loading".format(round(kw/len(u)*100,2)))
#storage.add_fundings(k[2])
print("True length of inputs: {}".format(true_length))
