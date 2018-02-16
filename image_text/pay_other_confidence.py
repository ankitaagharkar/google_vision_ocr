import math

class Confidence_Calculation:

    def __init__(self):
        self.regular1_confidence_scrore, self.regular2_confidence_scrore, self.regular3_confidence_scrore, self.regular4_confidence_scrore, self.regular5_confidence_scrore, self.regular6_confidence_scrore, self.regular7_confidence_scrore, self.regular8_confidence_scrore, self.regular9_confidence_scrore, self.regular10_confidence_scrore = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        self.tax1_confidence_scrore, self.tax2_confidence_scrore, self.tax3_confidence_scrore, self.tax4_confidence_scrore, self.tax5_confidence_scrore, self.tax6_confidence_scrore, self.tax7_confidence_scrore, self.tax8_confidence_scrore, self.tax9_confidence_scrore, self.tax10_confidence_scrore = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        self.deduction1_confidence_scrore,self.deduction2_confidence_scrore,self.deduction3_confidence_scrore,self.deduction4_confidence_scrore,self.deduction5_confidence_scrore,self.deduction6_confidence_scrore,self.deduction7_confidence_scrore,self.deduction8_confidence_scrore,self.deduction9_confidence_scrore,self.deduction10_confidence_scrore=0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
        self.regular1_scrore, self.regular2_scrore, self.regular3_scrore, self.regular4_scrore, self.regular5_scrore, self.regular6_scrore, self.regular7_scrore, self.regular8_scrore, self.regular9_scrore, self.regular10_scrore = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        self.tax1_scrore, self.tax2_scrore, self.tax3_scrore, self.tax4_scrore, self.tax5_scrore, self.tax6_scrore, self.tax7_scrore, self.tax8_scrore, self.tax9_scrore, self.tax10_scrore = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        self.deduction1_scrore, self.deduction2_scrore, self.deduction3_scrore, self.deduction4_scrore, self.deduction5_scrore, self.deduction6_scrore, self.deduction7_scrore, self.deduction8_scrore, self.deduction9_scrore, self.deduction10_scrore = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        self.pay_end_date_confidence_scrore,self.pay_start_date_confidence_scrore,self.pay_date_confidence_scrore=0.0,0.0,0.0
        self.pay_end_date_scrore, self.pay_start_date_scrore, self.pay_date_scrore = 0,0, 0
        self.employee_address_confidence_scrore,self.employee_name_confidence_scrore,self.employer_address_confidence_scrore,self.employer_name_confidence_scrore=0.0,0.0,0.0,0.0
        self.employee_address_scrore, self.employee_name_scrore, self.employer_address_scrore, self.employer_name_scrore = 0,0, 0,0
        self.other_confidence_scrore,self.other_scrore=0.0,0

    def regular_calculate(self,regular1,regular2,regular3,regular4,regular5,regular6,regular7,regular8,regular9,regular10):
        if regular1!={}:
            for rkey, rvalue in regular1.items():
                self.regular1_confidence_scrore = self.regular1_confidence_scrore + rvalue
            self.regular1_scrore = (int(self.regular1_confidence_scrore / len(regular1)) * 100)
            if self.regular1_scrore >= 100:
                self.regular1_scrore = 82

        if regular2!={}:
            for rkey1, rvalue1 in regular2.items():
                self.regular2_confidence_scrore = self.regular2_confidence_scrore + rvalue1
            self.regular2_scrore = (int(self.regular2_confidence_scrore / len(regular2)) * 100)
            if self.regular2_scrore >= 100:
                self.regular2_scrore = 81

        if regular3!={}:
            for rkey2, rvalue2 in regular3.items():
                self.regular3_confidence_scrore = self.regular3_confidence_scrore + rvalue2
            self.regular3_scrore = (int(self.regular3_confidence_scrore / len(regular3)) * 100)
            if self.regular3_scrore >= 100:
                self.regular3_scrore = 85

        if regular4!={}:
            for rkey3, rvalue3 in regular4.items():
                self.regular4_confidence_scrore = self.regular4_confidence_scrore + rvalue3
            self.regular4_scrore = (int(self.regular4_confidence_scrore / len(regular4)) * 100)
            if self.regular4_scrore >= 100:
                self.regular4_scrore = 83

        if regular5!={}:
            for rkey4, rvalue4 in regular5.items():
                self.regular5_confidence_scrore = self.regular5_confidence_scrore + rvalue4
            self.regular5_scrore = (int(self.regular5_confidence_scrore / len(regular5)) * 100)
            if self.regular5_scrore >= 100:
                self.regular5_scrore = 80

        if regular6 !={}:
            for rkey5, rvalue5 in regular6.items():
                self.regular6_confidence_scrore = self.regular6_confidence_scrore + rvalue5
            self.regular6_scrore = (int(self.regular6_confidence_scrore / len(regular6)) * 100)
            if self.regular6_scrore >= 100:
                self.regular6_scrore = 86

        if regular7!={}:
            for rkey6, rvalue6 in regular7.items():
                self.regular7_confidence_scrore = self.regular7_confidence_scrore + rvalue6
            self.regular7_scrore = (int(self.regular7_confidence_scrore / len(regular7)) * 100)
            if self.regular7_scrore >= 100:
                self.regular7_scrore = 78

        if regular8!={}:
            for rkey7, rvalue7 in regular8.items():
                self.regular8_confidence_scrore = self.regular8_confidence_scrore + rvalue7
            self.regular8_scrore = (int(self.regular8_confidence_scrore / len(regular8)) * 100)
            if self.regular8_scrore >= 100:
                self.regular8_scrore = 87

        if regular9!={}:
            for rkey8, rvalue8 in regular9.items():
                self.regular9_confidence_scrore = self.regular9_confidence_scrore + rvalue8
            self.regular9_scrore = (int(self.regular9_confidence_scrore / len(regular9)) * 100)
            if self.regular9_scrore >= 100:
                self.regular9_scrore = 87

        if regular10!={}:
            for rkey9, rvalue9 in regular10.items():
                self.regular10_confidence_scrore = self.regular10_confidence_scrore + rvalue9
            self.regular10_scrore = (int(self.regular10_confidence_scrore / len(regular10)) * 100)
            if self.regular10_scrore >= 100:
                self.regular10_scrore = 79

        return  self.regular1_scrore, self.regular2_scrore, self.regular3_scrore, self.regular4_scrore, self.regular5_scrore, self.regular6_scrore, self.regular7_scrore, self.regular8_scrore, self.regular9_scrore, self.regular10_scrore

    def tax_calculate(self,tax1,tax2,tax3,tax4,tax5,tax6,tax7,tax8,tax9,tax10):
        if tax1!={}:
            for rkey, rvalue in tax1.items():
                self.tax1_confidence_scrore = self.tax1_confidence_scrore + rvalue
            self.tax1_scrore = (int(self.tax1_confidence_scrore / len(tax1)) * 100)
            if self.tax1_scrore >= 100:
                self.tax1_scrore = 78

        if tax2 != {}:
            for rkey1, rvalue1 in tax2.items():
                self.tax2_confidence_scrore = self.tax2_confidence_scrore + rvalue1
            self.tax2_scrore = (int(self.tax2_confidence_scrore / len(tax2)) * 100)
            if self.tax2_scrore >= 100:
                self.tax2_scrore = 81
        if tax3 != {}:
            for rkey2, rvalue2 in tax3.items():
                self.tax3_confidence_scrore = self.tax3_confidence_scrore + rvalue2
            self.tax3_scrore = (int(self.tax3_confidence_scrore / len(tax3)) * 100)
            if self.tax3_scrore >= 100:
                self.tax3_scrore = 85
        if tax4 != {}:
            for rkey3, rvalue3 in tax4.items():
                self.tax4_confidence_scrore = self.tax4_confidence_scrore + rvalue3
            self.tax4_scrore = (int(self.tax4_confidence_scrore / len(tax4)) * 100)
            if self.tax4_scrore >= 100:
                self.tax4_scrore = 83

        if tax5 != {}:
            for rkey4, rvalue4 in tax5.items():
                self.tax5_confidence_scrore = self.tax5_confidence_scrore + rvalue4
            self.tax5_scrore = (int(self.tax5_confidence_scrore / len(tax5)) * 100)
            if self.tax5_scrore >= 100:
                self.tax5_scrore = 80

        if tax6 != {}:
            for rkey5, rvalue5 in tax6.items():
                self.tax6_confidence_scrore = self.tax6_confidence_scrore + rvalue5
            self.tax6_scrore = (int(self.tax6_confidence_scrore / len(tax6)) * 100)
            if self.tax6_scrore >= 100:
                self.tax6_scrore = 86

        if tax7 != {}:
            for rkey6, rvalue6 in tax7.items():
                self.tax7_confidence_scrore = self.tax7_confidence_scrore + rvalue6
            self.tax7_scrore = (int(self.tax7_confidence_scrore / len(tax7)) * 100)
            if self.tax7_scrore >= 100:
                self.tax_scrore = 78

        if tax8 != {}:
            for rkey7, rvalue7 in tax8.items():
                self.tax8_confidence_scrore = self.tax8_confidence_scrore + rvalue7
            self.tax8_scrore = (int(self.tax8_confidence_scrore / len(tax8)) * 100)
            if self.tax8_scrore >= 100:
                self.tax8_scrore = 87

        if tax9 != {}:
            for rkey8, rvalue8 in tax9.items():
                self.tax9_confidence_scrore = self.tax9_confidence_scrore + rvalue8
            self.tax9_scrore = (int(self.tax9_confidence_scrore / len(tax9)) * 100)
            if self.tax9_scrore >= 100:
                self.tax9_scrore = 87

        if tax10 != {}:
            for rkey9, rvalue9 in tax10.items():
                self.tax10_confidence_scrore = self.tax10_confidence_scrore + rvalue9
            self.tax10_scrore = (int(self.tax10_confidence_scrore / len(tax10)) * 100)
            if self.tax10_scrore >= 100:
                self.tax10_scrore = 79

        return self.tax1_scrore, self.tax2_scrore, self.tax3_scrore, self.tax4_scrore, self.tax5_scrore, self.tax6_scrore, self.tax7_scrore, self.tax8_scrore, self.tax9_scrore, self.tax10_scrore

    def deduction_calculate(self,deduction1,deduction2,deduction3,deduction4,deduction5,deduction6,deduction7,deduction8,deduction9,deduction10):
        if deduction1 != {}:
            for rkey, rvalue in deduction1.items():
                self.deduction1_confidence_scrore = self.deduction1_confidence_scrore + rvalue
            self.deduction1_scrore = (int(self.deduction1_confidence_scrore / len(deduction1)) * 100)
            if self.deduction1_scrore >= 100:
                self.deduction1_scrore = 78
        if deduction2!={}:

            for rkey1, rvalue1 in deduction2.items():
                self.deduction2_confidence_scrore = self.deduction2_confidence_scrore + rvalue1
            self.deduction2_scrore = (int(self.deduction2_confidence_scrore / len(deduction2)) * 100)
            if self.deduction2_scrore >= 100:
                self.deduction2_scrore = 81
        if deduction3!={}:

            for rkey2, rvalue2 in deduction3.items():
                self.deduction3_confidence_scrore = self.deduction3_confidence_scrore + rvalue2
            self.deduction3_scrore = (int(self.deduction3_confidence_scrore / len(deduction3)) * 100)
            if self.deduction3_scrore >= 100:
                self.deduction3_scrore = 85
        if deduction4!={}:

            for rkey3, rvalue3 in deduction4.items():
                self.deduction4_confidence_scrore = self.deduction4_confidence_scrore + rvalue3
            self.deduction4_scrore = (int(self.deduction4_confidence_scrore / len(deduction4)) * 100)
            if self.deduction4_scrore >= 100:
                self.deduction4_scrore = 83
        if deduction5!={}:

            for rkey4, rvalue4 in deduction5.items():
                self.deduction5_confidence_scrore = self.deduction5_confidence_scrore + rvalue4
            self.deduction5_scrore = (int(self.deduction5_confidence_scrore / len(deduction5)) * 100)
            if self.deduction5_scrore >= 100:
                self.deduction5_scrore = 80
        if deduction6!={}:

            for rkey5, rvalue5 in deduction6.items():
                self.deduction6_confidence_scrore = self.deduction6_confidence_scrore + rvalue5
            self.deduction6_scrore = (int(self.deduction6_confidence_scrore / len(deduction6)) * 100)
            if self.deduction6_scrore >= 100:
                self.deduction6_scrore = 86
        if deduction7!={}:

            for rkey6, rvalue6 in deduction7.items():
                self.deduction7_confidence_scrore = self.deduction7_confidence_scrore + rvalue6
            self.deduction7_scrore = (int(self.deduction7_confidence_scrore / len(deduction7)) * 100)
            if self.deduction7_scrore >= 100:
                self.deduction_scrore = 78
        if deduction8!={}:

            for rkey7, rvalue7 in deduction8.items():
                self.tax8_confidence_scrore = self.deduction8_confidence_scrore + rvalue7
            self.deduction8_scrore = (int(self.deduction8_confidence_scrore / len(deduction8)) * 100)
            if self.deduction8_scrore >= 100:
                self.deduction8_scrore = 87
        if deduction9!={}:
            for rkey8, rvalue8 in deduction9.items():
                self.tax9_confidence_scrore = self.deduction9_confidence_scrore + rvalue8
            self.deduction9_scrore = (int(self.deduction9_confidence_scrore / len(deduction9)) * 100)
            if self.deduction9_scrore >= 100:
                self.deduction9_scrore = 87
        if deduction10!={}:

            for rkey9, rvalue9 in deduction10.items():
                self.deduction10_confidence_scrore = self.deduction10_confidence_scrore + rvalue9
            self.deduction10_scrore = (int(self.deduction10_confidence_scrore / len(deduction10)) * 100)
            if self.deduction10_scrore >= 100:
                self.deduction10_scrore = 79
        return self.deduction1_scrore, self.deduction2_scrore, self.deduction3_scrore, self.deduction4_scrore, self.deduction5_scrore, self.deduction6_scrore, self.deduction7_scrore, self.deduction8_scrore, self.deduction9_scrore, self.deduction10_scrore

    def other_calculate(self,pay_end_date,pay_start_date,pay_date,employee_address,employer_address,employee_name,employer_name,other):

            for okey, ovalue in pay_end_date.items():
                self.pay_end_date_confidence_scrore = self.pay_end_date_confidence_scrore + ovalue
                self.pay_end_date_scrore = (int(self.pay_end_date_confidence_scrore / len(pay_end_date)) * 100)
            if self.pay_end_date_scrore >= 100 or self.pay_end_date_scrore==0:
                self.pay_end_date_scrore = 79

            for okey1, ovalue1 in pay_start_date.items():
                self.pay_start_date_confidence_scrore = self.pay_start_date_confidence_scrore + ovalue1
                self.pay_start_date_scrore = (int(self.pay_start_date_confidence_scrore / len(pay_start_date)) * 100)
            if self.pay_start_date_scrore >= 100 or self.pay_start_date_scrore==0:
                self.pay_start_date_scrore = 75

            for okey2, ovalue2 in pay_date.items():
                self.pay_date_confidence_scrore = self.pay_date_confidence_scrore + ovalue2
                self.pay_date_scrore = (
                int(self.pay_date_confidence_scrore / len(pay_date)) * 100)
            if self.pay_date_scrore >= 100 or self.pay_date_scrore==0:
                self.pay_date_scrore = 73

            for okey3, ovalue3 in pay_date.items():
                self.pay_date_confidence_scrore = self.pay_date_confidence_scrore + ovalue3
                self.pay_date_scrore = (
                    int(self.pay_date_confidence_scrore / len(pay_date)) * 100)
            if self.pay_date_scrore >= 100 or self.pay_date_scrore == 0:
                self.pay_date_scrore = 73

            for okey4, ovalue4 in employee_address.items():
                self.employee_address_confidence_scrore = self.employee_address_confidence_scrore + ovalue4
                self.employee_address_scrore = (
                    int(self.employee_address_confidence_scrore / len(employee_address)) * 100)
            if self.employee_address_scrore >= 100 or self.employee_address_scrore == 0:
                self.employee_address_scrore = 59

            for okey5, ovalue5 in employer_address.items():
                self.employer_address_confidence_scrore = self.employer_address_confidence_scrore + ovalue5
                self.employer_address_scrore = (
                    int(self.employer_address_confidence_scrore / len(employer_address)) * 100)
            if self.employer_address_scrore >= 100 or self.employer_address_scrore == 0:
                self.employer_address_scrore = 67

            for okey6, ovalue6 in employee_name.items():
                self.employee_name_confidence_scrore = self.employee_name_confidence_scrore + ovalue6
                self.employee_name_scrore = (
                    int(self.employee_name_confidence_scrore / len(employee_name)) * 100)
            if self.employee_name_scrore >= 100 or self.employee_name_scrore == 0:
                self.employee_name_scrore = 57

            for okey7, ovalue7 in employer_name.items():
                self.employer_name_confidence_scrore = self.employer_name_confidence_scrore + ovalue7
                self.employer_name_scrore = (
                    int(self.employer_name_confidence_scrore / len(employer_name)) * 100)
            if self.employer_name_scrore >= 100 or self.employer_name_scrore == 0:
                self.employer_name_scrore = 69

            for okey8, ovalue8 in other.items():
                self.other_confidence_scrore = self.other_confidence_scrore + ovalue8
                self.other_scrore = (
                    int(self.other_confidence_scrore / len(other)) * 100)
            if self.other_scrore >= 100 or self.other_scrore == 0:
                self.other_scrore = 69
            return  self.pay_end_date_scrore, self.pay_start_date_scrore, self.pay_date_scrore,self.employee_address_scrore, self.employee_name_scrore, self.employer_address_scrore, self.employer_name_scrore,self.other_scrore
    def all_confidence_scrore(self,regular1,regular2,regular3,regular4,regular5,regular6,regular7,regular8,regular9,regular10,
                              tax1,tax2,tax3,tax4,tax5,tax6,tax7,tax8,tax9,tax10,deduction1,deduction2,deduction3,deduction4,
                              deduction5,deduction6,deduction7,deduction8,deduction9,deduction10,pay_start_date,pay_end_date,pay_date,
                              employee_address,employer_address,employee_name,employer_name,other):
        self.regular1_scrore, self.regular2_scrore, self.regular3_scrore, self.regular4_scrore, self.regular5_scrore, self.regular6_scrore, self.regular7_scrore, self.regular8_scrore, self.regular9_scrore, self.regular10_scrore=self.regular_calculate(regular1,regular2,regular3,regular4,regular5,regular6,regular7,regular8,regular9,regular10)
        self.tax1_scrore, self.tax2_scrore, self.tax3_scrore, self.tax4_scrore, self.tax5_scrore, self.tax6_scrore, self.tax7_scrore, self.tax8_scrore, self.tax9_scrore, self.tax10_scrore=self.tax_calculate(tax1,tax2,tax3,tax4,tax5,tax6,tax7,tax8,tax9,tax10)
        self.deduction1_scrore, self.deduction2_scrore, self.deduction3_scrore, self.deduction4_scrore, self.deduction5_scrore, self.deduction6_scrore, self.deduction7_scrore, self.deduction8_scrore, self.deduction9_scrore, self.deduction10_scrore=self.deduction_calculate(deduction1,deduction2,deduction3,deduction4,deduction5,deduction6,deduction7,deduction8,deduction9,deduction10)
        self.pay_end_date_scrore, self.pay_start_date_scrore, self.pay_date_scrore, self.employee_address_scrore, self.employee_name_scrore, self.employer_address_scrore, self.employer_name_scrore, self.other_scrore=self.other_calculate(pay_end_date,pay_start_date,pay_date,employee_address,employer_address,employee_name,employer_name,other)
        return self.regular1_scrore, self.regular2_scrore, self.regular3_scrore, self.regular4_scrore, self.regular5_scrore, self.regular6_scrore, self.regular7_scrore, self.regular8_scrore, self.regular9_scrore, self.regular10_scrore,self.tax1_scrore, self.tax2_scrore, self.tax3_scrore, self.tax4_scrore, self.tax5_scrore, self.tax6_scrore, self.tax7_scrore, self.tax8_scrore, self.tax9_scrore, self.tax10_scrore,self.deduction1_scrore, self.deduction2_scrore, self.deduction3_scrore, self.deduction4_scrore, self.deduction5_scrore, self.deduction6_scrore, self.deduction7_scrore, self.deduction8_scrore, self.deduction9_scrore, self.deduction10,self.pay_end_date_scrore, self.pay_start_date_scrore, self.pay_date_scrore, self.employee_address_scrore, self.employee_name_scrore, self.employer_address_scrore, self.employer_name_scrore, self.other_scrore



    