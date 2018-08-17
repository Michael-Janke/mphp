from datetime import datetime

from utils.DataLoader import DataLoader
from validation.GridSearch import GridSearch


if __name__ == '__main__':

    start = datetime.now()

    print("Imported modules", flush=True)

    dataLoader = DataLoader("dataset4")
    print("data loaded", flush=True)

    healthy = dataLoader.getData(["healthy"], ["all"], excluded_cancer_types = ["CESC"])
    sick = dataLoader.getData(["sick"], ["all"], excluded_cancer_types = ["CESC"])
    data = dataLoader.getData(["sick", "healthy"], ["all"], excluded_cancer_types = ["CESC"])

    print(data.labels)
    print(any(["CESC" in label for label in data.labels]))

    grid_search = GridSearch(sick, healthy, data, "results/test.csv")
    print("got combined data", flush=True)

    grid_search.get_table_all_at_once()
    print("table creation done", flush=True)

    #grid_search.save_table_to_disk(table, "chi²")
    print("saved table to file", flush=True)

    """table = grid_search.get_table_one_vs_rest()
    print("table creation done", flush=True)

    grid_search.save_table_to_disk(table, "grid_search_one_vs_rest_big")
    print("saved table to file", flush=True)"""

    print(datetime.now() - start)
