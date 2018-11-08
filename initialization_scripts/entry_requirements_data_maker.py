import pandas as pd

dress_code, price, age = [], [], []

for i in range(0, 192):
    dress_code += ["Smart Casual","Trendy Casual", "Black & White","Clubwear","Casual"]
    for i in range(0, 80):
        age += list(range(18, 30))
        for i in range(0, 60):
            price += map(lambda x: str(x)+"$", list(range(20, 100, 5)))

df = pd.DataFrame(data={'dress_code': dress_code,\
                        'price': price,\
                        'age': age}).drop_duplicates()
df = df.assign(requirements_id=list(range(len(df)))) # Add artist_id column
df.to_csv("../static/datasets/entry_requirements.csv",sep=",",header=True, index=False)