if __name__ == '__main__':

    # Download data if it is unavailable.
    import pandas as pd

    A_office = pd.read_xml('A_office_data.xml')
    B_office = pd.read_xml('B_office_data.xml')
    hr_data = pd.read_xml('hr_data.xml')

    A_office['combine'] = "A" + A_office['employee_office_id'].astype(str)
    B_office['combine'] = "B" + B_office['employee_office_id'].astype(str)
    hr_data['combine'] = hr_data['employee_id']

    A_office = A_office.set_index('combine')
    B_office = B_office.set_index('combine')
    hr_data = hr_data.set_index('combine')

    # print(list(A_office.index))
    # print(list(B_office.index))
    # print(list(hr_data.index))

    combine_AB=pd.concat([A_office,B_office])
    combine_all= combine_AB.merge(hr_data,right_index=True,left_index=True)
    combine_all=combine_all.drop(columns=['employee_office_id','employee_id'])
    combine_all=combine_all.sort_index()

    # print(list(combine_all.index))
    # print(list(combine_all.columns))

    combine_all.sort_values(by=['average_monthly_hours'],ascending=False)
    name=combine_all['Department'].tolist()
    # print(name[:10])

    combine_query=combine_all.query('Department=="IT" and salary=="low"')
    lst=combine_query['number_project']
    # print(lst.sum())

    # Employee_ID=['A4','B7064','A3033']

    selected=combine_all.loc[['A4','B7064','A3033'],['last_evaluation','satisfaction_level']]
    # print(selected.values.tolist())

    def count_bigger_5(serie):
        return(serie>5).sum()

    # combine_all=combine_all.groupby(['left']).agg({'number_project': ['median',count_bigger_5],
    #                                     'time_spend_company':['mean','median'],
    #                                    'Work_accident':'mean','last_evaluation':['mean','std']})
    # print(round(combine_all,2).to_dict())

    pivot_table=combine_all.pivot_table(index='Department', columns=['left','salary'],
                                        values='average_monthly_hours',aggfunc='median')

    pivot_table_2=combine_all.pivot_table(index='time_spend_company',columns='promotion_last_5years',
                                          values=['satisfaction_level','last_evaluation'],aggfunc=['max','mean','min'])

    request=pivot_table[(pivot_table[(0.0, 'high')] <= pivot_table[(0.0, 'medium')]) &
                            (pivot_table[(1.0, 'low')] <= pivot_table[(1.0, 'high')])]

    request_2=pivot_table_2[(pivot_table_2[('mean','last_evaluation', 0.0)] >= pivot_table_2[('mean','last_evaluation',
                                                                                                1.0)])]
    print(round(request,2).to_dict())
    print(round(request_2,2).to_dict())


















