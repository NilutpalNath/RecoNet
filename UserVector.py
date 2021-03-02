import numpy as np
import pandas as pd

from torch.utils.data import Dataset
from torchvision import transforms

class UserVector(Dataset):
    def __init__(self, age, gender, uratings):
        if age<11:
            self.age=2
        elif age<16:
            self.age=3
        elif age<20:
            self.age=4
        else:
            self.age=5

        if gender.lower() == 'male':
            self.gender = 0
        else:
            self.gender = 1

        self.data = pd.read_csv("inputFormater.csv")
        self.data.loc[0, 'Gender'] = self.gender
        self.data.loc[0, 'Category'+str(self.age)] = 1

        self.columns = list(self.data.columns)

        self.aniId_to_ind = pd.Series(data=range(len(self.columns)), index=self.columns)

        for aniId in uratings.keys():
            self.data.loc[0, str(aniId)] = uratings[aniId]
        self.data.fillna(0, inplace=True)

        self.data = self.data.iloc[:,:]

        self.transform =  transforms.Compose([transforms.ToTensor()])

        self.data = self.transform(np.array(self.data))

    def __len__(self):
        return len(self.data[0])

    def __getitem__(self, ind):
        user_vector = self.data.data[0][ind]
        return user_vector

    def get_anime_id(self, ind):
        return int(self.columns[ind])

    def anime_to_index(self):
        return self.aniId_to_ind
