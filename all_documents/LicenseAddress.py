import re

"""
Changelog

## [1.0] - 2018-04-01
Entire functionality is encapsulated in a new class.
It takes input as the text of license with its co-ordinates and provides output as 
name and address.

## [0.2] - 2018-03-29
Line Algorithm is used for getting data

## [0.1] - 2018-03-19
Implemented address identification method based on co-ordinates
"""

class LicenseAddress:
    def __init__(self):
        self.result={}
        self.description = []

    def get_data_in_box(self,bounding,lines):
        bounding_x1, bounding_y1 = bounding[0]
        bounding_x2, bounding_y2 = bounding[1]
        min_overlap = 40
        output_values = []
        for l_index,line in enumerate(lines):
            for key,values in enumerate(line):
                #Get bounding box by taking minimum of x and y, maximum of x and y.
                #this will solve problem of rotated texts as well.
                min_x = min(values[1], key = lambda x: x[0])[0]
                min_y = min(values[1], key = lambda x: x[1])[1]
                max_x = max(values[1], key = lambda x: x[0])[0]
                max_y = max(values[1], key = lambda x: x[1])[1]
                text_area = (max_x - min_x) * (max_y - min_y)
                x_overlap = max(0, min(bounding_x2, max_x) - max(bounding_x1, min_x))
                y_overlap = max(0, min(bounding_y2, max_y) - max(bounding_y1, min_y))
                overlapArea = x_overlap * y_overlap
                if overlapArea > 0 and (overlapArea/text_area)*100 >= min_overlap:
                    output_values.append([values[0],values[1],l_index])
        return output_values

    def rectify_data(self,pa_points,mode_slant,mode_height):

        state_lines = []
        line_list = []
        line_heights = []
        desc = self.description.description

        #sort all words as per y-axis of its first element
        res = sorted(self.result, key=lambda x: x[1][0][1])
        
        mode_slant = mode_slant+round(mode_height/3)
        #initialise all values for reading first word of document
        prev_y_start = -100
        prev_y_end = -100
        prev_y_mid = -100
        mod_ht = abs(res[0][1][0][1] - res[0][1][2][1])
        
        max_height = mode_height * 2.5
        min_height = mode_height * 0.5
        # if re.search(r'(!?OH|IA)',state_lines[0][0]):
        #     new_line_multiplier = 0.5
        # else:
        new_line_multiplier = 0.5

        """
        Algorithm to bring all words in one line if it belongs to same line
        It works best on documents which are not slanted.
        1. For each word check if word falls on a new line, 
            i.e. its start-y is at a distance more than 3/4th of current line's start-y
            1A: If YES, start a new line with new start point, end point and 3/4th point
            1B: If NO, add the word to current line
        """
        for key, values in enumerate(res):

            #print(values)
            #check if word size is greater than mode height of all words
            if abs(values[1][0][1] - values[1][3][1]) > max_height or abs(values[1][0][1] - values[1][3][1]) < min_height:
                #print('Rejected word ',values)
                continue
            if abs(values[1][0][1] - values[1][1][1]) > mode_slant:
                #print('Rejected word because of improper alignment',values)
                continue
            if values[1][0][1] < prev_y_mid and abs(prev_y_start-values[1][0][1]) <= mod_ht:
                line_list[-1].append([values[0],values[1]])
            else:
                line_list.append([[values[0],values[1]]])
                prev_y_start = values[1][1][1]
                prev_y_end = values[1][2][1]
                #prev_y_mid = int(((prev_y_start + prev_y_end) / 2 + prev_y_end)/2)
                prev_y_mid = prev_y_start + round((prev_y_end-prev_y_start) * new_line_multiplier)
                line_heights.append(abs(prev_y_start-prev_y_end))
                mod_ht = max(line_heights,key=line_heights.count)
            if values in pa_points:
                #print('we are adding state line')
                state_lines.append([values,len(line_list)-1])
        """
        ALgorithm to sort each line as per its x-axis co-ordinate and also to merge words as per document
        1. For each line do steps 2 to 6:
        2. Sort the line w.r.to start-x of each word on line
        3. For each word on line do steps 4 to 5:
        4. Check if word falls under specific word such as $,|,USD
            4A: If YES, add the word to pop-elements list and continue to next word. (To discard them later)
        5. Check if new word is very close to the previous word,
            i.e. distance between two words is less than max space width
            5A: If YES, check if both word are float or both are characters
                5AA: If No, then add new word as a seperate word
                5AB: If YES, then check if combined word with or without spaces 
                    is present in description given by Google API, and merge the word accordingly.
                5AC: If word doesn't fall in any of above category, add it as a separate word.
            5B: If NO, add the new word a separate word.
        6. For each element in pop-elements list traversed in reverse:
            Remove the element from line. 
            (These words are either merged with some other words or are specific words to be discarded)
        """
        space_lists = []
        decimal_value = False
        height_wise_multiplier = 1.5
        space_wise_multiplier = 2.75
        
        for k,line in enumerate(line_list):
            line_list[k] = sorted(line, key=lambda x: x[1][0][0])
            line = line_list[k]
            pop_elements = []
            word_end = -100
            space_width = 0

            if len(space_lists) > 5:
                general_space_width = int(sum(space_lists[-5:])/5)
            else:
                general_space_width = 100

            for w_index,word in enumerate(line):
                if word[0] in ('$','|','USD','(',')','=','>',':'):
                    pop_elements.append(w_index)
                    continue
                #if new word is very close to the previous word
                if abs(word_end - word[1][0][0]) <= space_width:
                    #check word without space
                    d = word_val + word[0]
                    d1 = word_val + ' ' + word[0]
                    if d in desc:
                        line_list[k][prev_index][0] = d
                        line_list[k][prev_index][1] = [check_word[1][0],word[1][1],word[1][2],check_word[1][3]]
                        #remove current word from line list
                        pop_elements.append(w_index)
                        word_val = d
                        word_end = word[1][2][0]
                        continue
                    if d1 in desc:
                        line_list[k][prev_index][0] = d1
                        line_list[k][prev_index][1] = [check_word[1][0],word[1][1],word[1][2],check_word[1][3]]
                        #remove current word from line list
                        pop_elements.append(w_index)
                        space_width = abs(word_end - word[1][0][0]) * space_wise_multiplier
                        space_lists.append(space_width)
                        word_val = d1
                        word_end = word[1][2][0]
                        continue
                    line_list[k][w_index] = word
                    if general_space_width < (abs(word[1][0][1] - word[1][2][1]) * height_wise_multiplier):
                        space_width = general_space_width
                    else:
                        space_width = abs(word[1][0][1] - word[1][2][1]) * height_wise_multiplier
                    word_end = word[1][2][0]
                    word_val = word[0]
                    prev_index = w_index
                    check_word = word
                else:            
                    line_list[k][w_index] = word
                    if general_space_width < (abs(word[1][0][1] - word[1][2][1]) * height_wise_multiplier):
                        space_width = general_space_width
                    else:
                        space_width = abs(word[1][0][1] - word[1][2][1]) * height_wise_multiplier
                    word_end = word[1][2][0]
                    word_val = word[0]
                    prev_index = w_index
                    check_word = word
            for i in reversed(pop_elements):
                line_list[k].pop(i)
        return line_list,state_lines

    def get_address_lines(self,lines,state_lines):
        all_addresses = []
        for sl in state_lines:
            #print('State Line is:',sl)
            state_name = sl[0][0]
            sc_vertices = vertices = sl[0][1]
            on_left = 8
            on_right = 5
            state_word = [x for x in lines[sl[1]] if state_name+',' in x[0] or state_name+' ' in x[0] or state_name+'.' in x[0]]
            if state_word:
                vertices = state_word[0][1]
                on_left = 2
                on_right = 2
                w_index =lines[sl[1]].index(state_word[0])
                if w_index != 0:
                    prev_word = lines[sl[1]][w_index-1]
                    if abs(abs(vertices[0][1]-vertices[3][1]) - abs(prev_word[1][0][1] - prev_word[1][3][1])) < 3:
                        #print('expanding vertices')
                        vertices[0] = lines[sl[1]][w_index-1][1][0]
                        vertices[3] = lines[sl[1]][w_index-1][1][3]
                        lines[sl[1]][w_index] = [prev_word[0] + ' ' + lines[sl[1]][w_index][0],vertices]
            #print(state_word)
            #print(lines[sl[1]])
            text_height = (vertices[0][1] - vertices[3][1])
            height = round(text_height * 8)

            third_pt_y = vertices[2][1] + (on_right * (sc_vertices[2][1]-sc_vertices[3][1]))
            third_pt_x = vertices[2][0] + (on_right * (sc_vertices[2][0]-sc_vertices[3][0]))
            # print('TP',third_pt_x,third_pt_y)
            last_pt_y = vertices[3][1] + round(on_left * (sc_vertices[3][1] - sc_vertices[2][1]))
            last_pt_x = vertices[3][0] + round(on_left * (sc_vertices[3][0] - sc_vertices[2][0]))
            # print('LP',last_pt_x,last_pt_y)
            first_pt_y = vertices[0][1] + round(on_left * (sc_vertices[0][1] - sc_vertices[1][1]))
            first_pt_x = vertices[0][0] + round(on_left * (sc_vertices[0][0] - sc_vertices[1][0]))
            first_pt_y += height
            # print('FP',first_pt_x,first_pt_y)
            second_pt_y = vertices[1][1] + (on_right * (sc_vertices[1][1] - sc_vertices[0][1]))
            second_pt_x = vertices[1][0] + (on_right * (sc_vertices[1][0] - sc_vertices[0][0]))
            second_pt_y += height
            # print('SP',second_pt_x,second_pt_y)
            if len(state_lines) > 1 and first_pt_y < 0:
                continue
            data_box = self.get_data_in_box([(first_pt_x,first_pt_y),(third_pt_x,third_pt_y)],lines)
            if data_box:
                status,details = self.extract_address(data_box,state_name)
            else:
                continue
            if not status:
                pass
            else:
                all_addresses.append(details)
        # print(all_addresses)
        return all_addresses

    def extract_address(self,data_box,state_name):
        output = {'name':[]}
        if len(data_box) < 2:
            return False,[]

        prev_line_number = -1
        address_lines = []

        #convert data of multiple lines into joined words form in each line
        for db in reversed(data_box):
            if db[2] != prev_line_number:
                address_lines.append([db])
                a_height = abs(db[1][0][1] - db[1][3][1]) * 2
                prev_line_number = db[2]
                prev_start_x = db[1][0][0]
            else:
                if abs(db[1][1][0] - prev_start_x) < a_height:
                    address_lines[-1][-1][0] = db[0] + ' ' + address_lines[-1][-1][0]
                    address_lines[-1][-1][1][0] = db[1][0]
                    address_lines[-1][-1][1][3] = db[1][3]
                    prev_start_x = db[1][0][0]
                else:
                    address_lines[-1].insert(0,db)
                    prev_start_x = db[1][0][0]
        if not address_lines:
            return
        
        start_x = False
        start_y = False
        address_found = False
        name_started = False
        name_line_completed = 0
        if state_name=='PA':
            total_name_lines = 1
        elif state_name=='MD':
            total_name_lines = 3
        elif state_name=='VA':
            total_name_lines = 3
        else:
            total_name_lines = 2

        for i,db in enumerate(address_lines):
            if not start_x:
                #look for word having state name, this should be the last line of our address
                for j,al in enumerate(db):
                    if state_name in al[0]:
                        output['address'] = [al[0]]
                        start_x = al[1][0][0]
                        start_y = al[1][0][1]
                        # print('found start_x',start_x)
                        a_height = abs(al[1][0][1] - al[1][3][1]) * 4
                        print('height is ',a_height)
                        end_x = al[1][2][0]
                        break
                continue

            min_diff = min(enumerate(db),key = lambda x: abs(x[1][1][0][0] - start_x))
            #print(min_diff,start_x)
            if abs(min_diff[1][1][0][0] - start_x) < a_height:
                if not address_found:
                    match_check = re.findall(r'((!?\d+)\s[A-Za-z]+)|([A-Za-z]+\s(!?\d+))|\d+',min_diff[1][0])
                    if match_check:
                        # print('Address line 2 finalized by first regex')
                        output['address'].insert(0,min_diff[1][0])
                        start_y = min_diff[1][1][0][1]
                        address_found = True
                    #check if third line is also address line
                    else:
                        try:                            
                            min_diff_1 = min(enumerate(db[i+1]),key = lambda x: abs(x[1][1][0][0] - start_x))
                            match_check_1 = re.findall(r'((!?\d+)\s[A-Za-z]+)|([A-Za-z]+\s(!?\d+))|\d+',min_diff_1[1][0])
                            if match_check_1 and abs(min_diff_1[1][1][0][0] - start_x) < a_height:
                                # print('2nd and 3rd Address Lines Finalized')
                                output['address'].insert(0,min_diff[1][0])
                                output['address'].insert(0,min_diff_1[1][0])
                                start_y = min_diff_1[1][1][0][1]
                                address_found = True
                            else:
                                #it might be a name line
                                output['name'].insert(0,min_diff_1[1][0])
                                print('Found a name line')
                                name_line_completed += 1
                                name_started = True
                                address_found = True
                        except:
                            pass
                elif not name_started:
                    match_check = re.findall(r'((!?\d+)\s[A-Za-z]+)|([A-Za-z]+\s(!?\d+))|\d+',min_diff[1][0])
                    if match_check:
                        output['address'].insert(0,min_diff[1][0])
                        #print('Address line 3 finalized')
                    else:
                        output['name'].insert(0,min_diff[1][0])
                        #print('Found a name line')
                        name_line_completed += 1
                    name_started = True
                elif name_line_completed < total_name_lines:
                    output['name'].insert(0,min_diff[1][0])
                    #print('Found another name line')
                    name_line_completed += 1
                if name_line_completed == total_name_lines:
                    break
            else:
                #print('This word is out of box range')
                #now there is no chance for getting address, check if we can get name
                if i>2:
                    address_found = True
        #print(output)
        return True,output

    def fetch(self,mode_slant,mode_height,points,locr_obj):
        self.description = locr_obj.description
        self.result = locr_obj.result

        #convert raw data into line-wise structured data
        lines,state_lines = self.rectify_data(points,mode_slant,mode_height)
        #
        # for line in lines:
        #     print(line)

        address_details = []
        if state_lines:
            address_details = self.get_address_lines(lines,state_lines)
        #print(address_details)
        return address_details