response={
	'application_id': '2585',
	'upload_document_id': 4836,
	'processed_path': 'e:\\iDocufy\\NodeCode\\Server_side\\modules\\document/../../uploads/2585/processed',
	'file_path': '/uploads/2585/uploaded/1517812032292Paystub1.jpg',
	'doc_id': '6',
	'fields': [{
		'name': 'gross_pay',
		'id': 35
	}, {
		'name': 'net_pay',
		'id': 36
		
	}, {
		'name': 'pay_frequency',
		'id': 25
		
	}, {
		'name': 'employer_city',
		'id': 38
		
	}, {
		'name': 'employer_state',
		'id': 39
		
	}, {
		'name': 'position',
		'id': 40
		
	}, {
		'name': 'mi',
		'id': 7

	}, {
		'name': 'employee_name',
		'id': 10
		
	}, {
		'name': 'employee_number',
		'id': 12
		
	}, {
		'name': 'tax1',
		'id': 13
		
	}, {
		'name': 'employer_name',
		'id': 14
		
	}, {
		'name': 'employer/company_code',
		'id': 15
		
	}, {
		'name': 'pay_period_start_date',
		'id': 16
		
	}, {
		'name': 'pay_period_end_date',
		'id': 17
		
	}, {
		'name': 'pay_date',
		'id': 18
		
	}, {
		'name': 'tax2',
		'id': 19
		
	}, {
		'name': 'tax3',
		'id': 20
		
	}, {
		'name': 'tax4',
		'id': 21
		
	}, {
		'name': 'tax5',
		'id': 22
		
	}, {
		'name': 'tax6',
		'id': 23
		
	}, {
		'name': 'tax7',
		'id': 24
		
	}, {
		'name': 'tax8',
		'id': 26

	}, {
		'name': 'tax9',
		'id': 27
		
	}, {
		'name': 'tax10',
		'id': 28
		
	}, {
		'name': 'state_unemployment',
		'id': 29
		
	}, {
		'name': 'regular1',
		'id': 30
		
	}, {
		'name': 'employment_start_date',
		'id': 37
		
	}, {
		'name': 'regular3',
		'id': 41
		
	}, {
		'name': 'regular4',
		'id': 42
		
	}, {
		'name': 'regular5',
		'id': 43
		
	}, {
		'name': 'regular6',
		'id': 44
		
	}, {
		'name': 'regular7',
		'id': 45
		
	}, {
		'name': 'regular8',
		'id': 46
		
	}, {
		'name': 'regular9',
		'id': 47
		
	}, {
		'name': 'regular10',
		'id': 48
		
	}, {
		'name': 'other1',
		'id': 49
		
	}, {
		'name': 'other2',
		'id': 50
		
	}, {
		'name': 'other3',
		'id': 51
		
	}, {
		'name': 'other4',
		'id': 52
		
	}, {
		'name': 'other5',
		'id': 53
		
	}, {
		'name': 'other6',
		'id': 54
		
	}, {
		'name': 'other7',
		'id': 55
		
	}, {
		'name': 'other8',
		'id': 56
		
	}, {
		'name': 'other9',
		'id': 57
		
	}, {
		'name': 'other10',
		'id': 58
		
	}]
}
value={'Regular': ['Earnings', '10,364.38', '185,351.32', 0], 'Dependent Gt': ['Other', '-0.55', '6.05', 0], 'Bonus': ['Earnings', None, '56,422.00', 0], 'Deferral Bonus': ['Earnings', None, '52,253.00', 0], 'Gross Pay': ['Gross Pay', '10,364.93', '294,032.37', 0], 'Mctswa': ['Other', '10,364.38', None, 1],'w2Grp': ['Other', '22.40', '274.50', 1], 'Federal Income Tax': ['Deductions', '-2,479.55', '56,757.83', 0], '401K Elig Wages': ['Other', '10,364.38','241,773.32', 1], 'Medicare Tax': ['Deductions', '-150.08', '3,466.72', 0], '401K Match': ['Other', '310.93', '7,253.20', 1], 'Medicare Surtax': ['Deductions', '-93.14', '351.75', 0], '401K Safe Harbo': ['Other', '310.93', None, 1], 'NY State Income Tax': ['Deductions', '-657.96', '16,667.91', 0], 'NY SUI/SDI Tax': ['Other', '-1.30', '23.40', 0], 'Social Security Tax': ['Deductions', None, '7,886.40', 0], 'Fsa-Medical': ['Other', '-37.50', None, 0], '*': ['Other', None, '14,506.36', 0], '401K': ['Other', '-621.86', None, 0], 'Trip Commuter': ['Other', None, '2,295.00', 0], 'Net Pay': ['Net Pay','6.322.99', None, 0], 'Savings': ['Other', '-6, 322.99', None, 0], 'Net Check': ['Other', '0.00', None, 0], '': ['Other', None, '2000', 0], 'Advice number:': ['Other', '00000390064', None, 1], 'XXXX XXXX': ['Other', None, '6,322.99', 1]}

earnings,current_earnings,ytd_earnings=[],[],[]
gross_net_values=list(value.values())
pays_keys=list(value.keys())
for i in range(len(gross_net_values)):
    if 'Earnings' in gross_net_values[i]:
        earnings.append(pays_keys[i])
        current_earnings.append(gross_net_values[i][1])
        ytd_earnings.append(gross_net_values[i][2])
print(earnings)
j=0
print(len(earnings))
for i in range(len(response['fields'])):
        if 'regular' in response['fields'][i]['name']:
            if j<len(earnings):
                print(i)
                response['fields'][i]['alias'] = earnings[j]
                response['fields'][i]['field_value_original'] = current_earnings[j]
                response['fields'][i]['optional'] = ytd_earnings[j]
                j=j+1
                pass
            # else:
            #     response['fields'][i]['alias'] = ''
            #     response['fields'][i]['field_value_original'] = ''
            #     response['fields'][i]['optional'] = ''
print(response)