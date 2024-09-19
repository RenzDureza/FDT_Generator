import pandas as pd
import math
from statistics import mode, StatisticsError

def generateFDT(data, numberOfClasses):
    minData = min(data)
    maxData = max(data)

    dataRange = maxData - minData

    classWidth = math.ceil(dataRange / numberOfClasses)

    classLimits = []
    lowerLimit = minData
    for i in range(numberOfClasses):
        upperLimit = lowerLimit + classWidth - 1
        classLimits.append((lowerLimit, upperLimit))
        lowerLimit = upperLimit + 1

    frequency = [0] * numberOfClasses
    for value in data:
        for i, (lower, upper) in enumerate(classLimits):
            if lower <= value <= upper:
                frequency[i] += 1
                break

    classBounderies = [(lower - 0.5, upper + 0.5) for lower, upper in classLimits]
    classMarks = [(lower + upper) / 2 for lower, upper in classLimits]
    cf = [sum(frequency[:i+1]) for i in range(numberOfClasses)]

    fdt = pd.DataFrame({
        'Class Limits': [f"{lower} - {upper}" for lower, upper in classLimits],
        'Class Boundaries': [f"{lower:.1f} - {upper:.1f}" for lower, upper in classBounderies],
        'Frequency': frequency,
        'Cumulative Frequency': cf,
        'Classmark': classMarks
    })

    total_observations = sum(frequency)
    mean = sum(f * x for f, x in zip(frequency, classMarks)) / total_observations
    
    median_class_index = next(i for i, cf in enumerate(cf) if cf >= total_observations / 2)
    L = classBounderies[median_class_index][0]
    CF = cf[median_class_index - 1] if median_class_index > 0 else 0
    f = frequency[median_class_index]
    w = classWidth
    median = L + ((total_observations / 2 - CF) / f) * w
    
    try:
        modal_class_index = frequency.index(max(frequency))
        L = classBounderies[modal_class_index][0]
        f1 = frequency[modal_class_index]
        f0 = frequency[modal_class_index - 1] if modal_class_index > 0 else 0
        f2 = frequency[modal_class_index + 1] if modal_class_index < numberOfClasses - 1 else 0
        mode = L + ((f1 - f0) / (2 * f1 - f0 - f2)) * w
    except StatisticsError:
        mode = "No unique mode"
    
    stats = pd.DataFrame({
        'Mean': [mean],
        'Median': [median],
        'Mode': [mode]
    })

    return fdt, stats

def main():
    data = input("Enter the data here(use comma ',' to separate the data): ")
    numberOfClasses = int(input("Enter number of classes: "))

    data = list(map(int, data.replace(' ', '').split(',')))

    table, stats = generateFDT(data, numberOfClasses)
    print("\nFrequency Distribution Table:")
    print(table.to_string(index=False))

    print("\nStatistics: ")
    print(stats.to_string(index=False))

if __name__ == "__main__":
    main()    