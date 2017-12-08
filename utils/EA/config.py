### General ###
runs = 5
generations = 2000
pop_size = 150
prob_muta = 0.2
prob_cross = 0.0
tour_size = 3
elite_percent = 0.1

### Restart ####
should_restart = True
immigrant_perc = 0.5
restart_generations = 1000


### Cross-Over method (row or block)
cross_over = "block"


### FILES ###
file = ["sudoku_easy_38.txt"]

#30 runs, 100k generations (for each file only with mutation and mutation+block-cross-over)
final_file1 = ["sudoku_easy_38.txt"]
final_file2 = ["sudoku_easy_34.txt"]
final_file3 = ["sudoku_medium_29.txt"]
final_file4 = ["sudoku_difficult_24.txt"]
final_file5 = ["sudoku_super_difficult_24.txt"]
final_file6 = ["sudoku_ai_escarcot.txt"]



### Run multiple FILES at once ### 
test_files = ["sudoku_easy_38.txt",
			"sudoku_medium_30.txt",
			"sudoku_difficult_28.txt",
]

all_files = ["sudoku_easy_38.txt",
			"sudoku_easy_34.txt",
			"sudoku_medium_30.txt",
			"sudoku_medium_29.txt",
			"sudoku_difficult_28.txt",
			"sudoku_difficult_24.txt",
			"sudoku_super_difficult_24.txt",
			"sudoku_super_difficult_22.txt",
			"sudoku_ai_escarcot.txt"
]
