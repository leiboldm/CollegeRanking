import pandas
import code

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
    coll_df['score'] = coll_df.apply(lambda row: createScore(row), axis=1)

    top_colleges = coll_df.sort('score', ascending=False)
    rank = 1
    for i, row in top_colleges[:25][['name', 'score']].iterrows():
        print "{} {} {:.2f}".format(str(rank).ljust(2), row['name'].ljust(50), row['score'])
        rank += 1
    code.interact(local=locals())
    

def fillNulls(df, key, defaultValue=None):
    if defaultValue == None: 
        defaultValue = df[key].mean()
    df[key].fillna(defaultValue, inplace=True)

def createScore(row):
    expensesPerStudent = row['TotalExpenses'] / row['Enrollment']

    # calculate admission rate
    if row['ApplicantsTotal'] > 0:
        admissionRate = row['AdmissionsTotal'] / row['ApplicantsTotal']
    else:
        admissionRate = 1
    if admissionRate > 1:
        raise Exception("admission rate invalid for {} {}".format(row['name'], admissionRate))

    # calculate matriculation rate
    if row['AdmissionsTotal'] > 0:
        matriculationRate = row['EnrolledTotal'] / row['AdmissionsTotal']
    else:
        matriculationRate = 0
    if matriculationRate > 1:
        raise Exception("matriculation rate invalid for {} {}".format(row['name'], matriculationRate))

    # calculate 75% average SAT/SAT equivalent
    act75 = 0
    sat75 = row['SATReading75'] + row['SATMath75'] + row['SATWriting75']
    dividend = 0
    if isNaN(sat75):
        sat75 = 0
    else:
        dividend = row['PercentSubmittingSAT']
    if not isNaN(row['ACT75']):
        act75 = ACTtoSAT(row['ACT75'])
        dividend += row['PercentSubmittingACT']
    if dividend == 0:
        dividend = 1
    avgSAT75 = (sat75 * row['PercentSubmittingSAT'] +
                act75 * row['PercentSubmittingACT']) / dividend

    # calculate 25% average SAT/SAT equivalent
    act25 = 0
    sat25 = row['SATReading25'] + row['SATMath25'] + row['SATWriting25']
    dividend = 0
    if isNaN(sat25):
        sat25 = 0
    else:
        dividend = row['PercentSubmittingSAT']
    if not isNaN(row['ACT25']):
        act25 = ACTtoSAT(row['ACT25'])
        dividend += row['PercentSubmittingACT']
    if dividend == 0:
        dividend = 1
    avgSAT25 = (sat25 * row['PercentSubmittingSAT'] + 
                act25 * row['PercentSubmittingACT']) / dividend

    SAT = (avgSAT25 + avgSAT75) / 2
   
    score = (expensesPerStudent / 100
            + (100 / admissionRate)
            + (matriculationRate * 100)
            + (SAT * 1)
            + ((50000 - row['Tuition']) / 100)
            + (100 / row['StudentToFacultyRatio'])
            + ((row['PercentUndergradOutOfState'] + row['PercentUndergradForeign']))
            + (row['PercentUndergrad18-24']) # prioritize youthful schools
            + (50 - abs(50 - row['PercentWomen'])) # prioritize equal gender ratio
            + (row['GraduationRate'])
            + (row['RetentionRate'])
            + (row['ProfessorSalary'] / 10000)
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
