import io

from google.cloud import vision
from google.cloud.vision import types

import difflib



class get_all_location:
    def __init__(self):
        self.result = {}
        self.address_val = {}
        self.licence_id = {}
        self.ssn = {}
        self.dict = {}
        self.emp_name = {}
        self.text_val = []
        self.location_json = ''
        self.keys = []
        self.values = []
        self.description = []
        self.earning_headers = ['earnings', 'hours and earnings', 'earnings and hours', 'arnings']
        self.deduction_headers = ['deductions', 'eductions', 'deductions statutory', 'statutory deductions',
                                  'deductions & credits', 'deductions from gross',
                                  'before tax', 'before tax deductions', 'pre tax', 'pre tax deductions',
                                  'pre-tax deductions', 'before-tax deductions',
                                  'after tax', 'after tax deductions', 'after-tax deductions', 'post tax deductions',
                                  'post-tax deductions']
        self.tax_headers = ['taxes', 'withholdings', 'tax deductions']

    def get_data_in_box(self, bounding):
        bounding_x1, bounding_y1 = bounding[0]
        bounding_x2, bounding_y2 = bounding[1]
        min_overlap = 20
        output_values = []
        for key, values in self.result.items():
            # Get bounding box by taking minimum of x and y, maximum of x and y.
            # this will solve problem of rotated texts as well.
            min_x = min(values, key=lambda x: x[0])[0]
            min_y = min(values, key=lambda x: x[1])[1]
            max_x = max(values, key=lambda x: x[0])[0]
            max_y = max(values, key=lambda x: x[1])[1]
            text_area = (max_x - min_x) * (max_y - min_y)
            x_overlap = max(0, min(bounding_x2, max_x) - max(bounding_x1, min_x))
            y_overlap = max(0, min(bounding_y2, max_y) - max(bounding_y1, min_y))
            overlapArea = x_overlap * y_overlap
            if overlapArea > 0 and (overlapArea / text_area) * 100 >= min_overlap:
                output_values.append([(min_x, min_y), (max_x, max_y)])
        return output_values

    def is_float(self, s):
        try:
            if s[-3] == ',':
                k = s.rfind(",")
                s = s[:k] + "." + s[k + 1:]
        except:
            pass
        s = s.replace('B', '8')
        s = s.replace('S', '5')
        s = s.replace(',', '')
        # s = s.replace('$','')
        s = s.replace('-', '')
        s = s.replace('–', '')
        # s = s.replace('*','')
        s = s.replace(' ', '.')
        s = s.replace('.', '', s.count('.') - 1)
        try:
            int(s)
            return False
        except:
            try:
                float(s)
                return s
            except ValueError:
                return False

    def is_float_or_int(self, s):
        try:
            if s[-3] == ',':
                k = s.rfind(",")
                s = s[:k] + "." + s[k + 1:]
        except:
            pass
        s = s.replace('B', '8')
        s = s.replace('S', '5')
        s = s.replace(',', '')
        # s = s.replace('$','')
        # s = s.replace('s','')
        s = s.replace('-', '')
        s = s.replace('–', '')
        # s = s.replace('*','')
        s = s.replace(' ', '.')
        s = s.replace('.', '', s.count('.') - 1)
        try:
            int(s)
            return True
        except:
            try:
                float(s)
                return True
            except ValueError:
                return False

    def rectify_data(self,description,result):
        line_list = []
        line_heights = []
        desc = self.description.description

        """
        #check co-ordinates traversal type, min sum of x+y should be our first co-ordinate
        res = list(self.result)
        print(res[0])
        min_pt = min(enumerate(res[0][1]), key=lambda x: x[1][0]+x[1][1])
        print(min_pt)

        #to be done later
        """

        # sort all words as per y-axis of its first element
        res = sorted(self.result, key=lambda x: x[1][0][1])
        # initialise all values for reading first word of document
        prev_y_start = -100
        prev_y_end = -100
        prev_y_mid = -100
        mod_ht = abs(res[0][1][0][1] - res[0][1][2][1])
        """
        Algorithm to bring all words in one line if it belongs to same line
        It works best on documents which are not slanted.
        1. For each word check if word falls on a new line, 
            i.e. its start-y is at a distance more than 3/4th of current line's start-y
            1A: If YES, start a new line with new start point, end point and 3/4th point
            1B: If NO, add the word to current line
        """
        for key, values in enumerate(res):
            print(key, values)
            if values[1][0][1] < prev_y_mid and abs(prev_y_start - values[1][0][1]) <= mod_ht:
                line_list[-1].append([values[0], values[1]])
            else:
                line_list.append([[values[0], values[1]]])
                prev_y_start = values[1][0][1]
                prev_y_end = values[1][2][1]
                prev_y_mid = int(((prev_y_start + prev_y_end) / 2 + prev_y_end) / 2)
                line_heights.append(abs(prev_y_start - prev_y_end))
                mod_ht = max(line_heights, key=line_heights.count)
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
        for k, line in enumerate(line_list):
            line_list[k] = sorted(line, key=lambda x: x[1][0][0])
            line = line_list[k]
            pop_elements = []
            word_end = 0
            space_width = 0
            for w_index, word in enumerate(line):
                if word[0] in ('$', '|', 'USD', '(', ')', '*'):
                    pop_elements.append(w_index)
                    continue
                # if new word is very close to the previous word
                if abs(word_end - word[1][0][0]) <= space_width:
                    # check word without space
                    d = word_val + word[0]
                    d1 = word_val + ' ' + word[0]
                    if self.is_float_or_int(word_val):
                        if not self.is_float_or_int(word[0]) and word[0] not in (',', '.', '/', '-', '–', '%'):
                            line_list[k][w_index] = word
                            space_width = abs(word[1][0][1] - word[1][2][1]) * 1.5
                            word_end = word[1][2][0]
                            word_val = word[0]
                            prev_index = w_index
                            check_word = word
                            continue
                        if word_val[-1] == '.' and len(word[0]) == 2:
                            space_width = 0
                    if d in desc:
                        line_list[k][prev_index][0] = d
                        line_list[k][prev_index][1] = [check_word[1][0], word[1][1], word[1][2], check_word[1][3]]
                        # remove current word from line list
                        pop_elements.append(w_index)
                        word_val = d
                        word_end = word[1][2][0]
                        continue
                    if d1 in desc:
                        line_list[k][prev_index][0] = d1
                        line_list[k][prev_index][1] = [check_word[1][0], word[1][1], word[1][2], check_word[1][3]]
                        # remove current word from line list
                        space_width = abs(word_end - word[1][0][0]) * 2
                        pop_elements.append(w_index)
                        word_val = d1
                        word_end = word[1][2][0]
                        continue
                    line_list[k][w_index] = word
                    space_width = abs(word[1][0][1] - word[1][2][1]) * 1.5
                    word_end = word[1][2][0]
                    word_val = word[0]
                    prev_index = w_index
                    check_word = word
                else:
                    """
                    if re.search('\b{!?S|s\d+}',word[0]):
                        print('heree')
                        word[0] = word[0].replace('S','')
                        word[0] = word[0].replace('s','')
                    """
                    line_list[k][w_index] = word
                    space_width = abs(word[1][0][1] - word[1][2][1]) * 1.5
                    word_end = word[1][2][0]
                    word_val = word[0]
                    prev_index = w_index
                    check_word = word
            for i in reversed(pop_elements):
                line_list[k].pop(i)
        return line_list

    def get_payslip_amounts(self, lines):
        block_header_flags = self.earning_headers + self.deduction_headers + self.tax_headers + ['information',
                                                                                                 'others',
                                                                                                 'memo information',
                                                                                                 'summary',
                                                                                                 'colleague',
                                                                                                 'employer',
                                                                                                 'net pay distribution',
                                                                                                 'direct deposit distribution',
                                                                                                 'direct deposit information',
                                                                                                 'direct deposit',
                                                                                                 'organizations contribution'
                                                                                                 ]
        # define paytype headers
        general_paytype_headers = ['type', 'description', 'pay type']
        specific_paytype_headers = ['tax', 'earnings', 'pay type']
        paytype_header_flags = general_paytype_headers + specific_paytype_headers

        extra_paytype_headers = ['rate', 'hours', 'hours/units', 'pay rate', 'hours/days']

        # define column headers
        current_col_flags = ['current', 'this period', 'current month', 'current period', 'ratecurrent', 'deductions']
        ytd_col_flags = ['year to date', 'ytd', 'total to date', 'y-t-d', 'year-to-date', 'ytd amount']
        other_col_flags = ['amount', 'earnings']
        column_header_flags = current_col_flags + ytd_col_flags + other_col_flags

        blocks = []
        columns = []
        paytypes = []

        data_blocks = []

        # block list = [word,start-x,start-y,mean-x,word_height,status]
        # column_list = [start-x,start-y,end-x,mean-x,block_id,None,Type,Word Height]

        """
        Algorithm to identify blocks of data
        1. For each line do steps from 2 to 3
        2. Deactivate General Paytype header and current flags
        3. For each word in this line do steps from 4 to 7
        4. Check if word belongs to block headers, if yes do steps 4A to 4C
            4A. Add the block with its details.
            4B: Check if block belongs to any of the column above this block.
                (Column should not be associated to any block and column start-x should be greater than block start-x)
                4B(a): If yes, assign this block to all such columns as describe above and goto step 5
            4C: Check if this block is blocking y-axis of any other block which is active
                4C(a): If yes, assign all columns belonging to that block to this block and de-activate that block
        5. Check if word belongs to paytype headers:
            5A: Check if it blongs to general paytype headers:
                5A(a): If yes, activate general paytype header
        6. Check if word belongs to column header, if yes do steps 6A to 6C
            6A: Determine if it belongs to current or YTD based on current flag
            (When current flag is false, column belongs to Current else YTD)
            6B: if column is blocking some other column, de-activate that column
            6C: check if this column belongs to any block, if yes:
                6C(a): Delete all previous columns belonging to that block and having type(current/ytd) same as new column
                6C(b): Assign column to this block.
        7. If any column is created already, do following steps:
            7A: Check if word is a float value, If yes, look for the column where it may belong and assign it
            7B: Else, store the word as prev word value.
        8. Return data blocks.
        """

        for line in lines:
            g_pt_header = False
            current_flag = False
            for w_index, word in enumerate(line):
                # check if word belongs to block headers
                b = difflib.get_close_matches(word[0].lower(), block_header_flags, cutoff=0.95)
                if b:
                    mean_x = (word[1][0][0] + word[1][1][0]) / 2
                    blocks.append(
                        [word[0], word[1][0][0], word[1][0][1], mean_x, abs(word[1][0][1] - word[1][3][1]), True])
                    block_flag = True
                    # check if there is any column upto 3 lines above which this block can be a part of
                    # that column should have its mean-x after block's mean-x
                    try:
                        for i in range(len(columns)):
                            if columns[i][4] == None:
                                if abs(columns[i][1] - word[1][0][1]) < (3 * columns[i][7]) and (
                                    columns[i][3] - mean_x) > 0:
                                    columns[i][4] = len(blocks) - 1
                                    block_flag = False
                    except:
                        pass

                    if block_flag:
                        # check if block is blocking some other block by using its mean and start x co-ordinates
                        try:
                            mean_diff = min(enumerate([x for x in blocks[0:-1] if x[5] == True]),
                                            key=lambda x: abs(x[1][3] - mean_x))
                            mean_width = mean_diff[1][4] * 1.5
                            if abs(mean_diff[1][3] - mean_x) < mean_width or abs(
                                            mean_diff[1][1] - word[1][0][0]) < mean_width:
                                b_index = blocks.index(mean_diff[1])
                                for i in range(len(columns)):
                                    if columns[i][4] == b_index:
                                        columns[i][4] = len(blocks) - 1
                                        columns[i][5] = None
                                blocks[b_index][5] = False
                        except:
                            pass

                # check if word belongs to paytypes header
                z = difflib.get_close_matches(word[0].lower(), paytype_header_flags, cutoff=0.80)
                if z:
                    paytypes.append([word[0], word[1][0][0], word[1][1][0]])
                    if z[0] in general_paytype_headers:
                        g_pt_header = True

                # check if word belongs to column headers
                c = difflib.get_close_matches(word[0].lower(), column_header_flags, cutoff=0.85)
                if c:
                    mw_factor = 1
                    mean_x = (word[1][0][0] + word[1][1][0]) / 2
                    try:
                        end_x = line[w_index + 1][1][0][0]
                    except:
                        end_x = 0
                    columns.append([word[1][0][0], word[1][0][1], end_x, mean_x, None, None, None,
                                    abs(word[1][0][1] - word[1][3][1])])
                    # check if is of type current or ytd
                    if c[0] in current_col_flags:
                        columns[-1][6] = 'Current'
                    elif c[0] in ytd_col_flags:
                        columns[-1][6] = 'YTD'
                    else:
                        if not current_flag:
                            current_flag = True
                            g_pt_header = False
                            columns[-1][6] = 'Current'
                        else:
                            if g_pt_header:
                                columns[-1][6] = 'Current'
                                g_pt_header = False
                            else:
                                columns[-1][6] = 'YTD'
                        # must deactivate Current or YTD column just above this, increase mw_factor
                        mw_factor = 6

                    # check if it is blocking some other column headers, if yes deactivate that column
                    try:
                        mean_diff = min(enumerate(columns[0:-1]), key=lambda x: abs(x[1][3] - mean_x))
                        mean_width = mean_diff[1][7] * 1.5 * mw_factor
                        if abs(mean_diff[1][3] - mean_x) < mean_width or abs(
                                        mean_diff[1][0] - word[1][0][0]) < mean_width:
                            # columns[mean_diff[0]][6] = False
                            columns.pop(mean_diff[0])
                    except:
                        pass

                    # check the block where this column belongs to,
                    # first check minimum mean_x difference with any block and check its y-distance
                    # look for upto 3 lines of document above this column as per column height
                    try:
                        y_diff = enumerate(
                            [x for x in blocks if x[5] == True and abs(x[2] - word[1][0][1]) < (3 * x[4])])
                        mean_diff = min(y_diff,
                                        key=lambda x: mean_x - x[1][3] if mean_x - x[1][3] >= 0 else float('inf'))
                        b_index = blocks.index(mean_diff[1])
                        # check its y-difference

                        columns[-1][4] = b_index
                        del_columns = []
                        for i, x in enumerate(columns):
                            if x[4] == b_index and x[6] == columns[-1][6]:
                                try:
                                    if prev_x_diff > (x[0] - blocks[b_index][3]):
                                        del_columns.append(i)
                                    else:
                                        del_columns.append(prev_index)
                                        prev_x_diff = x[0] - blocks[b_index][3]
                                        prev_index = i
                                except:
                                    prev_x_diff = x[0] - blocks[b_index][3]
                                    prev_index = i
                        del prev_x_diff
                        for i in reversed(del_columns):
                            columns.pop(i)
                    except:
                        # No blocks have been created yet.
                        pass
                        # check the paytype where this column belongs to

                # if columns are created, start looking for float values
                if columns:
                    val = self.is_float(word[0])
                    if val:
                        for i, e in reversed(list(enumerate(columns))):
                            if word[1][1][0] > columns[i][3] and (word[1][1][0] <= columns[i][2] or columns[i][2] == 0):
                                if columns[i][2] == 0:
                                    if abs(columns[i][3] - word[1][0][0]) <= (3 * columns[i][7] * 1.5):
                                        columns[i][2] = word[1][1][0] + (3 * columns[i][7] * 1.5)
                                    try:
                                        print('-----**-----', prev_word, val, columns[i][6], blocks[columns[i][4]])
                                        data_blocks.append([prev_word, val, columns[i][6], blocks[columns[i][4]][0]])
                                    except:
                                        print('-----**-----', prev_word, val, columns[i][6])
                                        data_blocks.append([prev_word, val, columns[i][6], 'Undefined'])
                                else:
                                    try:
                                        print('-----**-----', prev_word, val, columns[i][6], blocks[columns[i][4]])
                                        data_blocks.append([prev_word, val, columns[i][6], blocks[columns[i][4]][0]])
                                    except:
                                        print('-----**-----', prev_word, val, columns[i][6])
                                        data_blocks.append([prev_word, val, columns[i][6], 'Undefined'])
                                break
                    else:
                        if not self.is_float_or_int(word[0]):
                            prev_word = word[0]

        return data_blocks

    def create_blocks(self, data_blocks):
        net_blocks = ['net pay', 'total net']
        gross_blocks = ['gross pay', 'total gross']
        other_blocks = ['checking ', 'net check', 'savings', 'direct deposit', 'checkng', 'total']
        final_data = {'Net Pay': [], 'Gross Pay': [], 'Earnings': [], 'Deductions': [], 'Taxes': [], 'Others': []}
        prev_word = ''
        prev_block = ''
        for i, db in enumerate(data_blocks):
            x = difflib.get_close_matches(db[0].lower(), net_blocks + gross_blocks + other_blocks, cutoff=0.80)
            if x:
                if x[0] in net_blocks:
                    block_name = 'Net Pay'
                elif x[0] in gross_blocks:
                    block_name = 'Gross Pay'
                else:
                    block_name = 'Others'
            else:
                if db[3].lower() in self.earning_headers:
                    block_name = 'Earnings'
                elif db[3].lower() in self.deduction_headers:
                    block_name = 'Deductions'
                elif db[3].lower() in self.tax_headers:
                    block_name = 'Taxes'
                else:
                    block_name = 'Others'
            if db[2] == 'Current':
                final_data[block_name].append([db[0], db[1], ""])
                prev_word = db[0]
                prev_block = block_name
            else:
                if db[0] == prev_word and block_name == prev_block:
                    final_data[block_name][-1][2] = db[1]
                    prev_word = ''
                    prev_block = ''
                else:
                    final_data[block_name].append([db[0], "", db[1]])
        return final_data

    def get_text(self, path):
        client = vision.ImageAnnotatorClient()
        with io.open(path, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        # if 'Pay Stub' in doc_type:
        # response = client.text_detection(image=image)
        # else:
        response = client.document_text_detection(image=image)
        # texts = response.full_text_annotation
        # response = client.text_detection(image=image)
        texts = response.text_annotations
        self.description = texts[0]
        for text in texts[1:]:
            self.text_val.append(text.description)
            vertices = [(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices]
            self.keys.append(text.description)
            self.values.append(vertices)
        self.result = zip(self.keys, self.values)
        data = " ".join(map(str, self.text_val))
        return data

    def all_location_details(self,path,description,result):
        self.get_text(path)
        lines=self.rectify_data(description,result)
        data_blocks = self.get_payslip_amounts(lines)
        final_data = self.create_blocks(data_blocks)
        return final_data
"""
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False

def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False

        # draw a rectangle around the region of interest
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", image)

image = cv2.imread(sys.argv[1])
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    # if the 'r' key is pressed, reset the selection region
    if key == ord("r"):
        image = clone.copy()

    # if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        break

if len(refPt) == 2:
    x = get_all_location()
    x.get_text(sys.argv[1])
    res = x.get_data_in_box(refPt)
    if not res:
        print('No Text in this region')
    else:
        for val in res:
            cv2.rectangle(image,val[0],val[1],(0,255,255),2)
        cv2.imshow("image", image)
        cv2.waitKey(0)
"""





"""
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False
 
def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping
 
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
 
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False
 
        # draw a rectangle around the region of interest
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", image)

image = cv2.imread(sys.argv[1])
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
 
# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF
 
    # if the 'r' key is pressed, reset the selection region
    if key == ord("r"):
        image = clone.copy()
 
    # if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        break

if len(refPt) == 2:
    x = get_all_location()
    x.get_text(sys.argv[1])
    res = x.get_data_in_box(refPt)
    if not res:
        ##print('No Text in this region')
    else:
        for val in res:
            cv2.rectangle(image,val[0],val[1],(0,255,255),2)
        cv2.imshow("image", image)
        cv2.waitKey(0)
"""


# x = get_all_location()
# x.get_text(sys.argv[1])
#
# lines = x.rectify_data()
# for line in lines:
#     ##print(line)
# blocks = x.get_payslip_amounts(lines)
#lines = sorted(lines, key=getKey)

