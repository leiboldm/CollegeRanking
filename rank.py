import pandas

def main():
    coll_df = pandas.read_csv("collegeDataV2.csv")
    fillNulls(coll_df, "ProfessorSalary")
    fillNulls(coll_df, "PercentUndergradForeign")
    fillNulls(coll_df, "PercentUndergradOutOfState")
    fillNulls(coll_df, "PercentUndergradInState")
    fillNulls(coll_df, "PercentUndergrad18-24")
    fillNulls(coll_df, "GraduationRate")
    fillNulls(coll_df, "RetentionRate")
    fillNulls(coll_df, "Tuition", defaultValue=0) # military academies are free
    fillNulls(coll_df, "Endowment")
    coll_df['ExpensesPerStudent'] = coll_df.apply(lambda row: createExpensesPerStudent(row), axis=1)
    coll_df['MatriculationRate'] = coll_df.apply(lambda row: createMatriculationRate(row), axis=1)
    coll_df['AdmissionRate'] = coll_df.apply(lambda row: createAdmissionRate(row), axis=1)
    coll_df['SAT75Equiv'] = coll_df.apply(lambda row: createSATEquiv(row, '75'), axis=1)
    coll_df['SAT25Equiv'] = coll_df.apply(lambda row: createSATEquiv(row, '25'), axis=1)
    coll_df['score'] = coll_df.apply(lambda row: createScore(row), axis=1)

    top_colleges = coll_df.sort('score', ascending=False)
    max_score = max(top_colleges['score'].tolist())
    top_colleges['score'] = top_colleges.apply(lambda row: normalizeScore(row, max_score), axis=1)
    top_colleges['rank'] = range(1, top_colleges.shape[0] + 1)

    for i, row in top_colleges[:50][['rank', 'name', 'score']].iterrows():
        print "{} {} {:.2f}".format(str(row['rank']).ljust(2),
                                     row['name'].ljust(50), row['score'])

    columns = ['rank', 'name', 'score', 'AdmissionRate', 'MatriculationRate', 
                'SAT75Equiv', 'SAT25Equiv',
                'GraduationRate', 'RetentionRate', 'Tuition', 
                'ExpensesPerStudent', 'ProfessorSalary',
                'PercentUndergradOutOfState', 'PercentUndergradForeign', 'PercentWomen',
                'PercentUndergrad18-24', 'StudentToFacultyRatio', 'Enrollment', 
                'FulltimeUndergradEnrollment']

    output_headers = ['Rank', 'University Name', 'Score', 'Admission %', 'Matriculation %',
                    'SAT (75%)', 'SAT (25%)', 'Graduation % (6 year)', 'Retention %',
                    'Tuition ($)', 'Budget per Student ($)', 'Average Professor Salary ($)',
                    '% of Undergrad from out of state', '% of Undergrad foreign',
                    '% women', '% of Undergrad 18-24 years old',
                    'Student to Faculty Ratio', 'Total Enrollment', 
                    'Fulltime Undergrad Enrollment']

    # a list of the columns to output to a csv file in a tuple with the
    # column's display formatting
    columns_headers = [
        ('rank', 'Rank'), 
        ('name', 'University Name'), 
        ('score', 'Score'), 
        ('AdmissionRate', 'Admission %'), 
        ('MatriculationRate', 'Matriculation %'), 
        ('SAT75Equiv', 'SAT (75%)'), 
        ('SAT25Equiv', 'SAT (25%)'), 
        ('GraduationRate', 'Graduation % (6 year)'), 
        ('RetentionRate', 'Retention %'), 
        ('Tuition', 'Tuition ($)'), 
        ('ExpensesPerStudent', 'Budget per Student ($)'), 
        ('ProfessorSalary', 'Average Professor Salary ($)'), 
        ('PercentUndergradOutOfState', '% of Undergrad from out of state'), 
        ('PercentUndergradForeign', '% of Undergrad foreign'), 
        ('PercentWomen', '% women'), 
        ('PercentUndergrad18-24', '% of Undergrad 18-24 years old'), 
        ('StudentToFacultyRatio', 'Student to Faculty Ratio'), 
        ('Enrollment', 'Total Enrollment'), 
        ('FulltimeUndergradEnrollment', 'Fulltime Undergrad Enrollment')]

    columns = [x[0] for x in columns_headers]
    output_headers = [x[1] for x in columns_headers]
    top_colleges = top_colleges[columns]
    top_colleges.columns = output_headers
    with open("top_colleges.csv", "w") as f:
        top_colleges.to_csv(f, columns=output_headers, index=False, float_format="%.1f") 

def normalizeScore(row, max_score):
    return row['score'] * 100 / max_score
    
def fillNulls(df, key, defaultValue=None):
    if defaultValue == None: 
        defaultValue = df[key].mean()
    df[key].fillna(defaultValue, inplace=True)

def createExpensesPerStudent(row):
    return row['TotalExpenses'] / row['Enrollment'] 

# calculate admission rate
def createAdmissionRate(row):
    if row['ApplicantsTotal'] > 0:
        return (row['AdmissionsTotal'] / row['ApplicantsTotal']) * 100
    else:
        return 100

# calculate matriculation rate
def createMatriculationRate(row):
    if row['AdmissionsTotal'] > 0:
        return (row['EnrolledTotal'] / row['AdmissionsTotal']) * 100
    else:
        return 0

# Take SAT and ACT data for the percentile (either '25' or '75')
# and create a 2400 SAT score by adding up all the SAT subjects
# and by converting ACT scores to SAT scores, create SAT equivalent by
# averaging the two scores weighting by the percent of students submitting each test
def createSATEquiv(row, percentile): 
    act = 0
    sat = row['SATReading' + percentile] + row['SATMath' + percentile]
    if isNaN(row['SATWriting' + percentile]):
        sat = sat * 3/2
    else:
        sat += row['SATMath' + percentile]
    
    divisor = 0
    if isNaN(sat):
        sat = 0
        row['PercentSubmittingSAT'] = 0
    else:
        divisor = row['PercentSubmittingSAT']

    if not isNaN(row['ACT' + percentile]):
        act = ACTtoSAT(row['ACT' + percentile])
        divisor += row['PercentSubmittingACT']
    else:
        row['PercentSubmittingACT'] = 0

    if divisor == 0:
        divisor = 1
    avgSAT = (sat * row['PercentSubmittingSAT'] +
                act * row['PercentSubmittingACT']) / divisor

    if avgSAT == 0:
        # if the school doesn't report data, assume it has a terrible average SAT
        avgSAT = 1100
    return int(avgSAT)

def createScore(row):
    score = (row['ExpensesPerStudent']
            + (100000 / row['AdmissionRate'])
            + (row['MatriculationRate'] * 250)
            + (row['SAT25Equiv'] * 50)
            + (row['SAT75Equiv'] * 50)
            - row['Tuition']
            + (10000 / row['StudentToFacultyRatio'])
            + (500 * (row['PercentUndergradOutOfState'] + row['PercentUndergradForeign']))
            + (500 * row['PercentUndergrad18-24']) # prioritize youthful schools
            + (1000 * (50 - abs(50 - row['PercentWomen']))) # prioritize equal gender ratio
            + (200 * row['GraduationRate'])
            + (200 * row['RetentionRate'])
            + (row['ProfessorSalary'] / 100)
            + (200 * (row['Enrollment'] ** 0.5))
            )
    return score

def isNaN(val):
    return not (val == val)

# convert ACT to SAT (2400), from blog.prepscholar.com/act-to-sat-conversion
def ACTtoSAT(actScore):
    if actScore > 36 or actScore < 0:
        raise Exception("ACT score invalid: {}".format(actScore))
    if actScore < 11:
        return 600
    mapping = {
        11: 780,
        12: 870,
        13: 950,
        14: 1020,
        15: 1100,
        16: 1170,
        17: 1230,
        18: 1290,
        19: 1350,
        20: 1410,
        21: 1470,
        22: 1530,
        23: 1590,
        24: 1650,
        25: 1710,
        26: 1770,
        27: 1820,
        28: 1880,
        29: 1940,
        30: 2000,
        31: 2060,
        32: 2120,
        33: 2180,
        34: 2250,
        35: 2330,
        36: 2390 
    }
    return mapping[actScore]

if __name__ == "__main__":
    main()
