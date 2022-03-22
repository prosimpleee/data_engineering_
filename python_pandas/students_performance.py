import pandas as pd

with open(r'StudentsPerformance.csv', 'r', encoding='utf-8') as students_file:
    file = pd.read_csv(students_file)
    # Columns rename
    df = file.rename(columns={'reading score': 'reading_score',
                              'writing score': 'writing_score',
                              'parental level of education': 'degree',
                              'test preparation course': 'status',
                              'math score': 'math_score'})

    # Mean values of score by degree 
    print(df.groupby('degree', as_index=False).aggregate({'math_score': 'mean',
                                                          'reading_score': 'mean',
                                                          'writing_score': 'mean'})
                                              .sort_values(['math_score',
                                                          'reading_score',
                                                          'writing_score'])
                                              .round(2))

    # For testing
    print(df.groupby('degree').mean()
            .sort_values(['math_score',
                          'reading_score',
                          'writing_score']))

    # If I want to see only high school degree
    print(df.query('degree == "high school"').groupby('degree', as_index=False)
            .aggregate({'math_score': 'mean',
                     'reading_score': 'mean',
                     'writing_score': 'mean'})
            .sort_values(['math_score',
                          'reading_score',
                          'writing_score'])
            .round(2))

    # Count of students by status & gender
    print(df.query('status == "completed"')
            .groupby('gender')
            .aggregate({'gender': 'count'}))


