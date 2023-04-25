import main

print('GymBro Test is Working!')
winston_stats = main.GymBroStats(135, 5)
print(f'Max: {winston_stats.max}')
print(f'Weight Array: {winston_stats.weight_array}')
print(f'Rep Array: {winston_stats.rep_array}')
print(f'Reps and Corresponding Weights: {dict(zip(winston_stats.rep_array, winston_stats.weight_array))}')