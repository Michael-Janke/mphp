#%%
from utils.DataLoader import DataLoader
from validation.GridSearch import GridSearch

print("Imported modules")

dataLoader = DataLoader("dataset4")
print("data loaded")

#%%
healthy = dataLoader.getData(["healthy"], ["THCA","LUAD"])
sick = dataLoader.getData(["sick"], ["THCA","LUAD"])
data = dataLoader.getData(["sick", "healthy"], ["THCA","LUAD"])

grid_search = GridSearch(sick, healthy, data)
print("got combined data")

#%%
#### ALL AT ONCE ####
table = grid_search.get_table_all_at_once()
print("table creation done")

grid_search.save_table_to_disk(table, "grid_search_all_at_once")
print("saved table to file")

# %%
#### ONE VS REST ####
table = grid_search.get_table_one_vs_rest()
print("table creation done")

grid_search.save_table_to_disk(table, "grid_search_one_vs_rest")
print("saved table to file")