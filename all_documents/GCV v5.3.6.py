import io
import json
import re
import os
import datetime
import cv2
import numpy as np
import requests
from google.cloud import vision
from google.cloud.vision import types
import sys
import difflib
from PIL import Image, ExifTags
import xml.etree.ElementTree as ElementTree
import subprocess
import copy

"""
Changelog
    ## [5.3.5] - 2018-04-25
    ### Changed
    - Col_word logic in rectify_data function, now only word with spaces will be used
        to check column words and that too with double checks.

    ## [5.3.5] - 2018-04-24
    ### Added
    - Logic to update other tables, to show best versions of Earnings, Pre, Post, Taxes 
        in ADP.
    - Added logic to ignore multiple tables of same block in a single pdf. It will stop reading other 
        values once total of a block is found at the end of block.

    ### Changed
    - Check Gross, Net function, now calculating net pay current and ytd based on table values
    - Logic of end_x for a column, next word must be column to define end_x of a column
    - Logic of space_wise space_width, minimum difference between two words should be 3 pixels,
        for it to be calculated through space_wise_multiplier
    - Logic of block to column assignment, if a block has to be assigned columns from 
        above it, each type should be assigned only once.
    - Regex for finding dates
    - Logic of next word in col_word search, block headers won't be considered anymore.
    - Data Box first point calculation

    ## [5.3.4] - 2018-04-19
    ### Added
    - Logic to check block headers in rectify_data function.

    ### Changed
    - Logic of pay component identification, check if current word is closer to 'description'
    - Net pay can be read from 'net pay distribution' block if net pay not specified.
    - Logic of blocking columns, if both conflicting block headers are deduction blocks, 
        we must assign previous block's columns to new block.
    - 'description' and 'pay type' added in pay_components list.

    ## [5.3.3] - 2018-04-18
    ### Added
    - Method to append multi page pdf into single image
    - Type of None column headers

    ### Changed
    - Few minor changes in address retrieval.
    - Logic in rectify data, where if a new word is added it will be checked against column headers

    ## [5.3.2] - 2018-04-16
    ### Changed
    - Address retrieval method has been changed as it is used in Licence OCR.
        Now license of three lines can also be detected using our method.

    ## [5.3.1] - 2018-04-12
    ### Changed
    - Logic of identify pay component, now using only those components for comparison
        which have found at least one value

    ## [5.3] - 2018-04-11
    ### Added
    - Logic to identify payment components based on various factors, such as if value found,
        if next line has got the component, if there is some noise between components and its 
        values, etc.

    ## [5.2.1.1] - 2018-04-06
    ### Removed
    - All print statements, only few important are kept for checking log.

    ## [5.2.1] - 2018-04-05
    ### Added
    - Logic to reject words based on mode_height and improper alignment
    - Logic to prevent words if they are detected more than once

    ### Changed
    - Logic for combining digits
    - Logic of updating Net Pay and Gross Pay in ADP paystubs. 
    - Method of finding pre and post types in deductions, removed an extra if which 
        would have taken more time than the other method.

    ## [5.2] - 2018-04-03
    ### Added
    - Logic to change co-ordinates when image is supposed to be rotated

    ### Changed
    - Method of reading image, now all images shall be read direxctly from bytes content,'
        instead of PIL.
    - Space Wise multiplier reduced to 2 from 2.25

    ### Removed
    - Logic of rotating image on the basis of camera orientation.

    ## [5.1.2] - 2018-03-30
    ### Added
    - Logic to remove words that are larger than normal text in entire paystub.
    - Function to remove dotted band in ADP paystubs when gross pay and net pay
        are not identified properly.

    ### Changed
    - Logic of is_float function
    - Space wise multiplier in highly compressed text
    - Rotation now done using 

    ## [5.1.1] - 2018-03-26
    ### Changed
    - Made changes in col header and block header types as required in generated xml

    ## [5.1] - 2018-03-25
    ### Added
    - Function to check type of data in data val pair
    - Method to look for hybrid data value pair, that will be avaialble in generic structure
    - Class to identify address in paystub
    - Added main method.

    ### Changed
    - Method to identify state name, now using difflib in it.
    - Changed all headers to accommodate changes made in xml which is being generated automatically.
    - Logic to delete column when it is blocking other column.

    ## [5.0] - 2018-03-20
    ### Added
    - Function to identify paystub type based on lookups texts which are added in 
        structure files.

    ### Changed
    - Get structure moved into class, class name and invocation method also changed
        so as to make it easier for integration.

    ## [4.4] - 2018-03-20
    ### Added
    - Added new rule of Is TaxType header defined, would be used for deductions tables
    which has Pre / Post or B/A defined in values itself.
    - Method to determine Gross Pay, if gross pay is not provided, instead total of earnings
    is provided.

    ### Changed
    - Updated entire method of create blocks to work as per new method of pre/post deduction
        identification.
    - Updated Identify pay component method to resolve bugs

    ## [4.3.3] - 2018-03-14
    ### Added
    - Method to convert all amount values to final float type as required
    - Method to determine text compression and search words from lines based on compression 
        level.
    - Added 'Federal Taxable Wages' and 'Total Gross Earnings' in other and gross columns rspectively

    ### Changed
    - Logic of Net Pay and Gross Pay in final output, if more than one rows found in these
        types, we shall finalize only one (preferably having Current and YTD both values)
        and display it in final output.

    ## [4.3.2] - 2018-03-13
    ### Added
    - Method to read vertical data value pair
    - Added method to read values of rules.
    - Logic to identify tables which has headers, in this case no old columns of blocking
        blocks are inherited in new block
    - Logic to ignore values if block is deactivated
    - Method to read values as per data dictionary definitions

    ### Changed
    - Logic of block identification in find_col_sequence method,
        now we use block end-x instead of mean-x
    - Paystub struct file, changes in data_val and data_dict

    ### Removed
    - Method to read 'is star pre tax', now any rule can be read using check_rule method
    - Delete col sequence logic

    ## [4.3.1] - 2018-03-12
    ### Added
    - Method to determine paystub type based on filename
    - Added '=' and '>' in ignore characters list
    - Added ':' character as end of word, useful to read data in data_val pairs

    ### Changed 
    - Method to make space_width zero in rectify_data, now if next word is also part of 
        previous word which is a column header we must include that
    - Changed method to define end of horizontal table, now we shall look at values line
        to define end of table. [tab_width method failed in few cases]

    ## [4.3] - 2018-03-09
    ### Added
    - Method to finalise block based on given block name in col sequence function,
        if seq_found is having confidence > 75, then only we refer block name
    - 'Your federal taxable....' text in ignore words
    - Data Dictionary which can be used to fetch data of summary or other general data

    ### Changed
    - Logic to identify total of some block.
    - Now column header can also be payment component
    - Logic to delete columns based on blocking words, now any string containing 
        digits cannot delete column.

    ## [4.2] - 2018-03-07
    ### Added
    - Function to identify values from horizontal table and add them to data blocks
    - Function to identify key-value pair of data as given in structure.
    - Function to create all_headers from structure based on given type

    ### Changed
    - Paytype identifying block, it is now used just for general paytype identification
    - Logic of structure reading, now for every paystub by default generic structure
        will be loaded, and if specific structure is provided, it will update all_headers
        as per specific structure.
    - Data blocks output for empty value changed from None to ''

    ## [4.1] - 2018-03-05
    ### Added
    - Rules in paystub structures. for e.g. we can define whether star is used 
        for pre-tax or not
    - If a pay component name is equal to its block name we consider that as Total of that block
    - Function to identify whether paystub has got star value as pre-tax deductions

    ### Changed 
    - Improved log comments to understand execution flow in a better way
    - Resolved bug of check_flag in find_sequence function

    ## [4.0] - 2018-03-01
    ### Added
    - Method to read pasytub based on given structure as per XML
    - Method to calculate Total of Earnings, Deductions (Pre & Post), Taxes
    - Method to read 'Rate' and 'Hour' from paystub
    - Signs '-' and '–' is added to ignore signs list

    ### Changed
    - Create final data method has been changed to accomodate 'rate' and 'hour' values in it
    - Column end in column headers are now calculated so as to check if next word is a part of respective
        column or if it is a new column header

    ## [3.3.1] - 2018-02-26
    ### Added
    - Added few values in tax headers and current, ytd col headers
    - Block name now to be identified as per block header values


    ## [3.3] - 2018-02-23
    ### Added
    - Logic to delete column if it is being blocked by any text apart from header flags.
    - Logic to stop word, when word belonging to column column headers are found in line algorithm. 
        [Current and YTD column detection is very important for this algorithm]
    - Curent column flags added in initialisation function.
    - Added 'voluntary deductions','other deductions' as types of deduction headers
    - Added 'taxable earnings', 'earnings period' as types of earnings headers
    - Added 'pay distribution' in types of other headers
    - Added new Block Names in final output 'Pre Tax Deductions','Post Tax Deductions'
    - Logic to identify deduction type such as 'Pre' or 'Post' based on given block header or if word / value contains * in it.

    ### Changed
    - space width distance between two words increased from 2.5X to 2.75X
    - Delete column-block mapping logic is updated, where first number of columns are counted,
        If there are 1+ columns:
        First preference will be given to columns that are placed below block headers. 
        [Note: y-distance should be greater than block's start-y plus half of block header height]
        If no such column found, find the nearest column column but not the overlapping column
    - Block blocking logic is changed, now it works on following idea:
        First try to search for a block that is near to its mean and block it
        If no such block found, for the nearest block check if new block is in between mean of block and its respective current column mean
        If any of above is true, change all columns from previous block to new block
    - Categorized deduction headers into three parts: Normal, Pre and Post

    ### Removed
    - Block Name 'Deductions' from final outputs

    ## [3.2.1] - 2018-02-21
    ### Changed
    - number of words to be considered for first general space width from 9 to 5
    - space width distance between two words increased from 2.25X to 2.5X
    - Delete column-block mapping logic is updated, such as there can be multiple columns of same type to 
        same block, if and only if columns names are similar. (To resolve issue of Blocks having data in 1+ parts)

    ### Added
    - Now storing column name as well, at 5th index of variable holding all column details

    ## [3.2] - 2018-02-21
    ### Added
    - Changelog to note down version-wise changes and to make my life easy
    - Logic to rotate image when camera orientation is incorrect
    - Function to identify payment component
    - Added a special character in float value identification method, new character added is '–', which is used
        as a subtraction symbol in few paystubs
    - Added 'associate taxes' in tax headers
    - New global variable 'other_headers' to store all other headers
    - Added 'rate this period' in current col flags
    - Added 'year to' in YTD col flags
    - Added 'amount earned' in other col flags
    - Added 'chck1' in other columns in create blocks method
    - Added 'gross earnings' in gross columns in create blocks method

    ### Changed
    - Column-block mapping algortihm is changed, it works on following idea:
        For upto 3 lines above this column look for:
        1. Closest block on left of this column where block start-x is less than column start-x
        2. If not found, find closest block on right of this column where block start-x is greater than or equal 
            to column start-x
    - Delete column-block mapping logic is changed (for multiple columns of same type to same block),
        it works on following idea:
        1. For a block having multiple columns to its bottom-right, keep the one closest on its right side.
        2. If no such column found, for columns on its same line or above it, keep the one farthest to it on right side.
    - Logic to joint float values, now two integers with a space between them will be considered as a float. 
    (Missing decimal issue resolved)
    - Logic for payment component identification, now it uses a new method which is added in this version.
    (Solves issue of incorrect pay component detection)

    ### Removed
    - Extra init parameters that were carried along from the start of this project
    - Draw bounding box and get data in box code, as it was not relevant to this project.

"""
DEBUG = True

class paystub_gcv:
    def __init__(self):
        self.result={}
        self.text_val=[]
        self.keys=[]
        self.values=[]
        self.description = []
        self.pay_components = []

    def init_structure(self,all_headers):
        self.earning_headers = all_headers['block_headers']['earnings']
        self.normal_deduction_headers = all_headers['block_headers']['normal_deductions']
        self.pre_deduction_headers = all_headers['block_headers']['pre_deductions']
        self.post_deduction_headers = all_headers['block_headers']['post_deductions']
        self.deduction_headers = self.normal_deduction_headers + self.pre_deduction_headers + self.post_deduction_headers
        
        self.tax_headers = all_headers['block_headers']['taxes']
        self.other_headers = all_headers['block_headers']['other']
        
        #define column headers
        self.current_col_flags = all_headers['col_headers']['current']
        self.ytd_col_flags = all_headers['col_headers']['ytd']
        self.other_col_flags = all_headers['col_headers']['other_earnings']
        self.rate_col_flags = all_headers['col_headers']['rate']
        self.hour_col_flags = all_headers['col_headers']['hour']
        self.none_col_flags = all_headers['col_headers']['none']
        self.column_header_flags = self.current_col_flags+self.ytd_col_flags+self.other_col_flags+self.rate_col_flags+self.hour_col_flags+self.none_col_flags

        self.column_sequences = all_headers['col_sequence']
        self.rules = all_headers['rules']
        self.vertical_column_sequences = all_headers['vertical_col_sequence']

        self.data_val = all_headers['data_val']
        self.data_dict = all_headers['data_dict']

    def custom_print(self,*arg):
        if DEBUG:
            print(arg)

    def is_float(self,s):
        try:
            if s[-3] == ',':
                k = s.rfind(",")
                s = s[:k] + "." + s[k+1:]
        except:
            pass
        s = s.replace('B','8')
        s = s.replace('S','5')
        s = s.replace(',','.')
        #s = s.replace('$','')
        s = s.replace('-','')
        s = s.replace('–','')
        s = s.replace('—','')
        s = s.replace(' ','.')
        s = s.replace('.','',s.count('.')-1)
        try:
            int(s)
            return False
        except:
            try:
                float(s)
                return s
            except ValueError:
                return False

    def is_float_or_int(self,s):
        try:
            if s[-3] == ',':
                k = s.rfind(",")
                s = s[:k] + "." + s[k+1:]
        except:
            pass
        s = s.replace('B','8')
        s = s.replace('S','5')
        s = s.replace(',','')
        s = s.replace('to','')
        s = s.replace('/','')
        s = s.replace('-','')
        s = s.replace('–','')
        s = s.replace('—','')
        s = s.replace(' ','.')
        s = s.replace('.','',s.count('.')-1)
        try:
            int(s)
            return True
        except:
            try:
                float(s)
                return True
            except ValueError:
                return False

    def final_float(self,s,c_type='General'):
        s = s.replace('B','8')
        s = s.replace('S','5')
        s = s.replace('s','')
        s = s.replace(',','')
        #s = s.replace('$','')
        s = s.replace('-','')
        s = s.replace('–','')
        s = s.replace('—','')
        s = s.replace(' ','')
        if c_type != 'Rate':
            s = s.replace('.','')
            s = s[:-2]+'.'+s[-2:]
        return s
    
    def is_pay_component(self,word,l_index):
        s = word[0]
        if s.lower() in ['yes','no']:
            return False
        s = s.replace(',','')
        s = s.replace(':','')
        s = s.replace('/','')
        s = s.replace('-','')
        s = s.replace('–','')
        s = s.replace('—','')
        s = s.replace(' ','')
        s = s.replace('.','')
        s = s.replace('*','')
        try:
            int(s)
            return False
        except:
            if len(s) < 2:
                return False
            else:
                #add this new pay component
                self.add_pay_component(word,l_index)
                return True

    def add_pay_component(self,word,l_index):
        #pay component list values - [word_details,start-x,value_found_status,line_number]
        if self.pay_components:
            if self.pay_components[-1][3] == l_index:
                #if both words are on same line
                if not self.pay_components[-1][2]:
                    #if prev word has not found a value yet, find min difference for 
                    #current and prev both components
                    prev_word = self.pay_components[-1][0]
                    try:
                        min_diff_current = min(enumerate(self.pay_components[:-1]), key=lambda x: abs(word[1][0][0] - x[1][1]) if x[1][2] else float('inf'))
                        min_diff_prev = min(enumerate(self.pay_components[:-1]), key=lambda x: abs(prev_word[1][0][0] - x[1][1]) if x[1][2] else float('inf'))
                        #self.custom_print('Comparing pay components ',word,min_diff_current,min_diff_prev)
                        if abs(min_diff_current[1][0][1][0][0] - word[1][0][0]) > abs(min_diff_prev[1][0][1][0][0] - prev_word[1][0][0]):
                            if min_diff_current[1][0][0].lower() not in ['description']:
                                #self.custom_print('Using Previous component ',self.pay_components[-1])
                                return
                            elif min_diff_current[1][0] == min_diff_prev[1][0]:
                                #self.custom_print('Using Previous component ',self.pay_components[-1])
                                return
                    except:
                        pass
        self.pay_components.append([word,word[1][0][0],False,l_index])
        return

    def rectify_data(self,pa_points,mode_slant,mode_height):
        state_lines = []
        line_list = []
        line_heights = []
        desc = self.description.description
        self.custom_print(desc)

        max_height = mode_height * 2.5
        min_height = mode_height * 0.5
        mode_slant = mode_slant+round(mode_height/3)

        #sort all words as per y-axis of its first element
        res = sorted(self.result, key=lambda x: x[1][0][1])
        
        #initialise all values for reading first word of document
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

        for _, values in enumerate(res):
            self.custom_print(values)
            #check if word size is greater than mode height of all words
            if abs(values[1][0][1] - values[1][3][1]) > max_height or abs(values[1][0][1] - values[1][3][1]) < min_height:
                self.custom_print('Rejected word ',values)
                continue
            if abs(values[1][0][1] - values[1][1][1]) > mode_slant:
                self.custom_print('Rejected word because of improper alignment',values)
                continue
            if values[1][0][1] < prev_y_mid and abs(prev_y_start-values[1][0][1]) <= mod_ht:
                line_list[-1].append([values[0],values[1]])
            else:
                line_list.append([[values[0],values[1]]])
                prev_y_start = values[1][0][1]
                prev_y_end = values[1][2][1]
                #prev_y_mid = prev_y_start + round((prev_y_end-prev_y_start) * 0.75)
                prev_y_mid = int(((prev_y_start + prev_y_end) / 2 + prev_y_end)/2)
                line_heights.append(abs(prev_y_start-prev_y_end))
                mod_ht = max(line_heights,key=line_heights.count)
            if values in pa_points:
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
        compression_level = self.check_rule('Highly Compressed Text')
        if compression_level:
            height_wise_multiplier = 1.25
            space_wise_multiplier = 2.0
        else:
            height_wise_multiplier = 1.5
            space_wise_multiplier = 2.75
        
        block_header_flags = self.earning_headers + self.deduction_headers + self.tax_headers + self.other_headers

        for k,line in enumerate(line_list):
            line_list[k] = sorted(line, key=lambda x: x[1][0][0])
            line = line_list[k]
            pop_elements = []
            word_end = 0
            space_width = 0
            new_line_start = True
            if len(space_lists) > 5:
                general_space_width = int(sum(space_lists[-5:])/5)
            else:
                general_space_width = 100

            
            last_word = ['',[]]
            for w_index,word in enumerate(line):
                if word[0] == last_word[0]:
                    if word[1][0][0] < last_word[1][1][0]:
                        pop_elements.append(w_index)
                        continue
                last_word = word
                if word[0] in ('$','|','USD','(',')','=','>',':'):
                    pop_elements.append(w_index)
                    continue

                special_char = False
                #if new word is very close to the previous word
                if abs(word_end - word[1][0][0]) <= space_width and not new_line_start:
                    #check word without space
                    d = word_val + word[0]
                    d1 = word_val + ' ' + word[0]
                    if word[0] not in (',','.','/','-','–','—','%','to'):
                        if self.is_float_or_int(word_val):                        
                            if not self.is_float_or_int(word[0]):
                                line_list[k][w_index] = word
                                if general_space_width < (abs(word[1][0][1] - word[1][2][1]) * height_wise_multiplier):
                                    space_width = general_space_width
                                else:
                                    space_width = abs(word[1][0][1] - word[1][2][1]) * height_wise_multiplier
                                word_end = word[1][2][0]
                                word_val = word[0]
                                prev_index = w_index
                                check_word = word
                                continue
                            elif len(word[0]) == 2:
                                if '.' not in word_val and not ('/' in word_val or '-' in word_val or '–' in word_val or '—' in word_val):
                                    d = word_val+'.'+word[0]
                                    decimal_value = True
                                if word_val[-1] == '.':
                                    space_width = 0 
                    else:
                        if not self.is_float_or_int(word_val):
                            #check if next word is a digit
                            try:
                                if self.is_float_or_int(line[w_index+1][0]):
                                    line_list[k][w_index] = word
                                    if general_space_width < (abs(word[1][0][1] - word[1][2][1]) * height_wise_multiplier):
                                        space_width = general_space_width
                                    else:
                                        space_width = abs(word[1][0][1] - word[1][2][1]) * height_wise_multiplier
                                    word_end = word[1][2][0]
                                    word_val = word[0]
                                    prev_index = w_index
                                    check_word = word
                                    continue
                            except:
                                pass
                        special_char = True
                    if d in desc or decimal_value:
                        decimal_value = False
                        line_list[k][prev_index][0] = d
                        line_list[k][prev_index][1] = [check_word[1][0],word[1][1],word[1][2],check_word[1][3]]
                        #remove current word from line list
                        pop_elements.append(w_index)

                        #if word belongs to column header, no further word should be added in it.
                        col_word = difflib.get_close_matches(d.lower(),self.column_header_flags,cutoff=0.95)
                        if col_word:
                            self.custom_print('we are here making space width zero ',word)
                            space_width = 0
                        word_val = d
                        word_end = word[1][2][0]
                        continue

                    if d1 in desc:
                        #define space width
                        if not special_char:
                            space_width = abs(word_end - word[1][0][0]) * space_wise_multiplier if abs(word_end - word[1][0][0]) > 3 else space_width
                            space_lists.append(space_width)
                        
                        #check if combined word is a column header
                        col_word = difflib.get_close_matches(d1.lower(),self.column_header_flags,cutoff=0.95)
                        if col_word:
                            self.custom_print('we are here making space width zero ',word)
                            space_width = 0
                        else:
                            #check if prev word and next word are column headers
                            if difflib.get_close_matches(word_val.lower(),self.column_header_flags,cutoff=0.95) and difflib.get_close_matches(word[0].lower(),self.column_header_flags,cutoff=0.95):
                                line_list[k][w_index] = word
                                if general_space_width < (abs(word[1][0][1] - word[1][2][1]) * height_wise_multiplier):
                                    space_width = general_space_width
                                else:
                                    space_width = abs(word[1][0][1] - word[1][2][1]) * height_wise_multiplier
                                word_end = word[1][2][0]
                                word_val = word[0]
                                prev_index = w_index
                                check_word = word
                                continue
                        
                        line_list[k][prev_index][0] = d1
                        line_list[k][prev_index][1] = [check_word[1][0],word[1][1],word[1][2],check_word[1][3]]
                        #remove current word from line list
                        pop_elements.append(w_index)
                        word_val = d1
                        word_end = word[1][2][0]
                        continue
                    
                    #add this word without space to previous word if its a special character
                    if special_char:
                        line_list[k][prev_index][0] = d
                        line_list[k][prev_index][1] = [check_word[1][0],word[1][1],word[1][2],check_word[1][3]]
                        #remove current word from line list
                        pop_elements.append(w_index)
                        word_val = d
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
                    new_line_start = False
                    line_list[k][w_index] = word

                    if general_space_width < (abs(word[1][0][1] - word[1][2][1]) * height_wise_multiplier):
                        space_width = general_space_width
                    else:
                        space_width = abs(word[1][0][1] - word[1][2][1]) * height_wise_multiplier
                    """
                    #if word belongs to column header, no further word should be added in it.
                    col_word = difflib.get_close_matches(word[0].lower(),self.column_header_flags,cutoff=0.95)
                    if col_word:
                        self.custom_print('we are here making space width zero ',word)
                        space_width = 0
                    """
                    word_end = word[1][2][0]
                    word_val = word[0]
                    prev_index = w_index
                    check_word = word
            for i in reversed(pop_elements):
                line_list[k].pop(i)
        return line_list,state_lines

    """
    We assume that horizontal tables would be of three lines, first line for payment components
    second and third line for current and YTD or vice-versa
    """
    def read_horizontal_table(self,lines,l_index,word,probable_list,columns,data_blocks):
        line = lines[l_index]
        w_index = line.index(word)
        final_seq = ''
        for seq in probable_list:
            col_headers = []
            col_headers.append([word,w_index])
            word_mean = (word[1][0][0] + word[1][1][0])/2
            try:
                temp_l_index = l_index
                temp_l_index = temp_l_index+1
                temp_line = lines[temp_l_index]
                for s in range(1,len(seq)):
                    mean_diff = min(enumerate(temp_line),key=lambda x: abs(word_mean - x[1][1][0][0]))
                    try:
                        if self.is_float_or_int(mean_diff[1][0]):
                            temp_w_index = temp_line.index(mean_diff[1])
                            if difflib.get_close_matches(temp_line[temp_w_index-1][0].lower(),[seq[s][0]],cutoff=0.80):
                                col_headers.append([temp_line[temp_w_index-1],temp_w_index-1])
                        else:
                            if difflib.get_close_matches(mean_diff[1][0].lower(),[seq[s][0]],cutoff=0.80):
                                col_headers.append([mean_diff[1],temp_w_index])
                        temp_l_index = temp_l_index+1
                        temp_line = lines[temp_l_index]
                    except:
                        pass
                if len(col_headers) == len(seq):
                    self.custom_print('We found a sequence',seq)
                    final_seq = seq
                    break
            except Exception as e:
                self.custom_print(e)
        #If sequence is found look for values and their respective component
        if final_seq:
            paytype_line = lines[l_index]
            #find current and YTD line based on given types, 
            #   default is 1st Current, 2nd YTD
            try:
                if final_seq[1][1]['col_type'] == 'Current':
                    curr_line = lines[l_index+1]
                    ytd_line = lines[l_index+2]
                elif final_seq[1][1]['col_type'] == 'YTD':
                    ytd_line = lines[l_index+1]
                    curr_line = lines[l_index+2]
            except Exception as e:
                curr_line = lines[l_index+1]
                ytd_line = lines[l_index+2]
            
            #assign block name based on given block name,
            #   default is 'Summary_table'
            try:
                block_name = final_seq[0][1]['block_name']
            except Exception as e:
                block_name = 'Summary_table'

            temp_data_blocks = []
            l2_index = col_headers[1][1]
            l3_index = col_headers[2][1]
            tab_width = (paytype_line[w_index+1][1][0][0] - paytype_line[w_index][1][1][0]) * 1.5
            #for each word in paytype line, look for its respective values
            paytype_end = False
            try:
                for p_index in range(w_index,len(paytype_line)):
                    p_word = paytype_line[p_index]
                    try:
                        if abs(last_word[1][1][0] - p_word[1][0][0]) > tab_width:
                            paytype_end = True
                        last_word = p_word
                    except:
                        last_word = p_word
                    mean_diff = min(enumerate(curr_line),key=lambda x: p_word[1][1][0] - x[1][1][0][0] if p_word[1][1][0] - x[1][1][0][0] >= 0 else float('inf'))
                    if self.is_float_or_int(mean_diff[1][0]) and p_word[1][0][0] < mean_diff[1][1][1][0]:
                        temp_data_blocks.append([p_word[0],self.final_float(mean_diff[1][0]),'Current',block_name])
                    elif paytype_end:
                        break
                    mean_diff = min(enumerate(ytd_line),key=lambda x: p_word[1][1][0] - x[1][1][0][0] if p_word[1][1][0] - x[1][1][0][0] >= 0 else float('inf'))
                    if self.is_float_or_int(mean_diff[1][0]) and p_word[1][0][0] < mean_diff[1][1][1][0]:
                        temp_data_blocks.append([p_word[0],self.final_float(mean_diff[1][0]),'YTD',block_name])
            except Exception as e:
                self.custom_print(e)

            try:
                #nullify all pay components in first line, also current and ytd col
                update_lines = [lines[l_index],lines[l_index+1],lines[l_index+2]]
                for p_index in range(w_index,len(paytype_line)):
                    if paytype_line[p_index] == last_word:
                        update_lines[0][p_index][0] = 'None'
                        table_end_x = update_lines[0][p_index][1][1][0]
                        break
                    update_lines[0][p_index][0] = 'None'
                
                update_lines[1][l2_index][0] = 'None'
                update_lines[2][l3_index][0] = 'None'
                table_start_x = paytype_line[w_index][1][0][0]
            except Exception as e:
                pass            

            #delete all columns that comes in range of this horizontal table
            #   i.e whose mean is between table start-x and table end-x
            try: 
                pop_cols = []
                for i,x in enumerate(columns):
                    if x[3] > table_start_x and x[3] < table_end_x:
                        pop_cols.append(i)
                for i in reversed(pop_cols):
                    columns.pop(i)
            except Exception as e:
                pass
            data_blocks.extend(temp_data_blocks)
            return True, columns, data_blocks, update_lines
        
        return False, columns, data_blocks, None

    def find_column_sequence(self,line,word,probable_list,columns,blocks):
        w_index = line.index(word)
        final_seq = ''
        #for each sequence in probable sequence list, look for matching sequence
        for seq in probable_list:
            seq_word = difflib.get_close_matches(word[0],[s[0].lower() for s in seq],cutoff=0.80)
            s_index = [s[0] for s in seq].index(seq_word[0])
            try:
                temp_w_index = w_index
                match_found = match_not_found = 0
                temp_columns = []
                #for each word in sequence, check if it matches word in line
                for s in range(s_index,len(seq)):
                    temp_word = line[temp_w_index]
                    if difflib.get_close_matches(seq[s][0],[temp_word[0].lower()],cutoff=0.75):
                        match_found = match_found + 1
                        try:
                            if line[temp_w_index+1][1][0][0] > temp_word[1][1][0]:
                                if not difflib.get_close_matches(temp_word[0].lower()+line[temp_w_index+1][0].lower(),[t[0] for t in seq[s]],cutoff=0.80):
                                    end_x = line[temp_w_index+1][1][0][0]
                                    temp_w_index = temp_w_index + 1
                                else:
                                    end_x = 0
                            else:
                                end_x = 0
                        except:
                            end_x = 0
                        try:
                            temp_columns.append([temp_word[1][0][0],temp_word[1][0][1],end_x,(temp_word[1][0][0]+temp_word[1][1][0])/2,None,temp_word[0],seq[s][1]['col_type'],abs(temp_word[1][0][1]-temp_word[1][3][1])])
                        except:
                            temp_columns.append([temp_word[1][0][0],temp_word[1][0][1],end_x,(temp_word[1][0][0]+temp_word[1][1][0])/2,None,temp_word[0],None,abs(temp_word[1][0][1]-temp_word[1][3][1])])
                    else:
                        match_not_found = match_not_found + 1
                    temp_w_index = temp_w_index + 1
                seq_confidence = match_found/len(seq)
                if seq_confidence > 0.65:
                    final_seq = seq
                    break
            except:
                pass
        if final_seq:
            b_index = False
            
            #check for block name in sequence if sequence confidence is above 75
            if seq_confidence > 75:
                for i in final_seq:
                    try:
                        block_name = i[1]['block_name']
                        #if block name is provided in structure, search for block with this name
                        block_found = difflib.get_close_matches(block_name,[x[0] for x in blocks if x[5] == True],cutoff=0.85)
                        if block_found:
                            self.custom_print('Found block by name ',block_found[0])
                            block_id = [x for x in blocks if x[5] == True and x[0] == block_found[0]]
                            b_index = blocks.index(block_id[0])
                        #if no such block found, create a new block
                        else:
                            blocks.append([block_name,temp_columns[0][0],temp_columns[0][1],temp_columns[0][3],temp_columns[0][7],True])
                            b_index = len(blocks) - 1
                        break
                    except Exception as e:
                        self.custom_print(e)

            #if block is not finalised, look for block w.r.to mean distance
            if not b_index:
                #find closest block
                seq_mean = (temp_columns[0][0] + temp_columns[-1][0])/2
                seq_y = temp_columns[0][1]
                try:
                    y_diff = enumerate([x for x in blocks if x[5] == True and abs(x[2] - seq_y) < (3 * x[4])])
                    mean_diff = min(y_diff,key=lambda x: abs(seq_mean - ((x[1][3] * 2) - x[1][1])))
                    self.custom_print('Block for this sequence is',mean_diff)
                    b_index = blocks.index(mean_diff[1])
                except Exception as e:
                    self.custom_print(e)

            #delete previous columns, blocking columns and assign b_index to 
            try:
                #delete all columns which belonged to this block
                pop_cols = []
                for i,x in enumerate(columns):
                    if x[4] == b_index:
                        pop_cols.append(i)
                for i in reversed(pop_cols):
                    columns.pop(i)

                #delete columns which are being blocked by these new columns
                for i,t in enumerate(temp_columns):
                    temp_columns[i][4] = b_index
                    try:
                        mean_diff = min(enumerate(columns), key=lambda x:abs(x[1][3] - t[3]))
                        mean_width = mean_diff[1][7] * 1.5
                        if abs(mean_diff[1][3]-t[3]) < mean_width or abs(mean_diff[1][0]-word[1][0][0]) < mean_width:
                            columns.pop(mean_diff[0])                            
                    except:
                        pass
                columns.extend(temp_columns)
                return True, columns, blocks, final_seq
            except Exception as e:
                self.custom_print(e)
        return False, columns, blocks, final_seq

    def check_rule(self,rule_name):
        try:
            for sublist in self.rules:
                if sublist[0] == rule_name:
                    if sublist[1]['val'] == 'True':
                        return True
                    return False
            return False
        except:
            return False

    def check_type(self,word,type):
        if type['type'] == 'date':
            word = word.replace(' ','')
            val = re.findall(r'(([1-9]|0[0-9]|1[0-2])\s?[./-]([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?[./-](19|20|21|22)\d\d|(0[0-9]|1[0-2])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-]\d\d|(0[0-9]|1[0-2])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](19|20|21|22)\d\d|(0[0-9]|1[0-9])\s?(0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](19|20|21|22)\d\d|(0[0-9]|1[0-9])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?(19|20|21|22)\d\d)', word)
            if val:
                return word
            return False
        if type['type'] == 'amount':
            val = re.findall(r'((0[0-9]|1[0-2])\s?[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?[./-](19|20|21|22)\d\d|(0[0-9]|1[0-2])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-]\d\d|(0[0-9]|1[0-2])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](19|20|21|22)\d\d|(0[0-9]|1[0-9])\s?(0[1-9]|1[0-9]|2[0-9]|3[0-1])[./-](19|20|21|22)\d\d|(0[0-9]|1[0-9])[./-](0[1-9]|1[0-9]|2[0-9]|3[0-1])\s?(19|20|21|22)\d\d)', word)
            if not val:
                return self.is_float(word)
            return False
        return word

    def get_payslip_amounts(self,lines):
        block_header_flags = self.earning_headers + self.deduction_headers + self.tax_headers + self.other_headers
        
        #define general paytype headers
        general_paytype_headers = ['type','description','pay type']
        
        blocks = []
        columns = []

        data_blocks = []
        block_with_headers = self.check_rule('All Blocks With Headers')

        is_star_pre = self.check_rule('Is Star Pre-Tax')
        is_pre_header_defined = self.check_rule('Is TaxType Header Defined')
    
        last_star_component = ''

        #block list = [word,start-x,start-y,mean-x,word_height,status]
        #column_list = [start-x,start-y,end-x,mean-x,block_id,None,Type,Word Height]

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
            6C: check if this column belongs to any block by following steps:
                (a): Get all blocks upto 3 lines above this column
                (b): First, find nearest block on left of this column, if found assign column to this block
                (c): If not found, find nearest block on right side.
                6C(a): Delete all previous columns belonging to that block and having type(current/ytd) same as new column
                6C(b): Assign column to this block.
        7. If any column is created already, do following steps:
            7A: Check if word is a float value, If yes, look for the column where it may belong and assign it
            7B: Else, store the word as prev word value.
        8. Return data blocks.
        """
        for l_index,line in enumerate(lines):
            g_pt_header = False
            current_flag = False
            for w_index,word in enumerate(line): 
                mean_x = (word[1][0][0]+word[1][1][0])/2
                word_height = abs(word[1][0][1]-word[1][3][1])

                #check if word belongs to a hybrid data value pair
                try:
                    seq_word = difflib.get_close_matches(word[0].lower(),[j[0] for j in self.data_val['Hybrid']],cutoff=0.80)
                    if seq_word:
                        self.custom_print(seq_word)
                        try:
                            horizontal_word = line[w_index+1]
                        except:
                            horizontal_word = []
                        try:
                            vertical_word = min(enumerate(lines[l_index+1]), key=lambda x: word[1][1][0] - x[1][1][0][0] if word[1][1][0] - x[1][1][0][0] >= 0 and x[1][1][1][0] - word[1][0][0] > 0 else float('inf'))
                            #if word is too below on y-axis, reject it
                            if abs(vertical_word[1][1][0][1] - word[1][3][1]) > (2 * word_height):
                                vertical_word = []
                            else:
                                vertical_word = vertical_word[1]
                        except:
                            vertical_word = []

                        if horizontal_word or vertical_word:
                            for j in self.data_val['Hybrid']:
                                if j[0] == seq_word[0]:
                                    h_type = j[1]
                                    break
                            h_word = v_word = False
                            if horizontal_word:
                                if horizontal_word[0].lower() not in [j[0] for j in self.data_val['Hybrid']]:
                                    h_word = self.check_type(horizontal_word[0],h_type)
                            if vertical_word:
                                if vertical_word[0].lower() not in [j[0] for j in self.data_val['Hybrid']]:
                                    v_word = self.check_type(vertical_word[0],h_type)
                            if h_word and v_word:
                                #check difference w.r.to spacing
                                if abs(mean_x - (horizontal_word[1][0][0]+horizontal_word[1][1][0])/2) < (5 * word_height):
                                    v_word = False
                                else:
                                    h_word = False
                                pass                                
                            if h_word:
                                data_blocks.append([word[0],h_word,'Current','General'])
                            elif v_word:
                                data_blocks.append([word[0],v_word,'Current','General'])
                            else:
                                self.custom_print('No value found')
                except:
                    pass

                #check if word belongs to a horizontal data value pair
                try:
                    seq_word = difflib.get_close_matches(word[0].lower(),[j[0] for j in self.data_val['Horizontal']],cutoff=0.80)
                    if seq_word:
                        data_blocks.append([word[0],line[w_index+1][0],'Current','General'])
                except:
                    pass

                #check if word belongs to a vertical data value pair
                try:
                    seq_word = difflib.get_close_matches(word[0].lower(),[j[0] for j in self.data_val['Vertical']],cutoff=0.80)
                    if seq_word:
                        possible_word = min(enumerate(lines[l_index+1]), key=lambda x: word[1][1][0] - x[1][1][0][0] if word[1][1][0] - x[1][1][0][0] >= 0 else float('inf'))
                        if possible_word[1][1][1][0] > word[1][0][0]:
                            val = self.is_float(possible_word[1][0])
                            if val:
                                data_blocks.append([word[0],self.final_float(val),'Current','General'])
                except Exception as e:
                    pass

                #check if word belongs to a horizontal table
                try:
                    seq_word = difflib.get_close_matches(word[0].lower(),[j[0] for i in self.vertical_column_sequences for j in i],cutoff=0.80)
                    if seq_word:
                        self.custom_print('We have got a start of some horizontal table',seq_word)
                        probable_list = []
                        for s in seq_word:
                            for i in self.vertical_column_sequences:
                                if s in [j[0] for j in i]:
                                    if i not in probable_list:
                                        probable_list.append(i)
                        status, columns, data_blocks, update_lines = self.read_horizontal_table(lines,l_index,word,probable_list,columns,data_blocks)
                        if status:
                            self.custom_print('Horizontal Table has been read properly')
                            lines[l_index] = update_lines[0]
                            lines[l_index+1] = update_lines[1]
                            lines[l_index+2] = update_lines[2]
                            continue
                except:
                    pass

                #check if word belongs to block headers
                b = difflib.get_close_matches(word[0].lower(),block_header_flags,cutoff=0.90)
                if b:
                    self.custom_print('\nI am in B',word[0])
                    blocks.append([word[0],word[1][0][0],word[1][0][1],mean_x,word_height,True])
                    block_flag = True
                    
                    #check if there is any column upto 3 lines above which this block can be a part of
                    # that column should have its mean-x after block's mean-x and 
                    # each type should be added only once
                    try:
                        column_types_assigned = []
                        for i in range(len(columns)):
                            if columns[i][4] == None and columns[i][6] not in column_types_assigned:
                                if abs(columns[i][1] - word[1][0][1]) < (3 * columns[i][7]) and (columns[i][3] - mean_x) > 0:
                                    columns[i][4] = len(blocks) - 1
                                    column_types_assigned.append(columns[i][6])
                                    block_flag = False
                    except:
                        pass

                    if block_flag:
                        #check if block is blocking some other block, by using its mean and start x co-ordinates
                        try:
                            mean_diff = min(enumerate([x for x in blocks[0:-1] if x[5] == True]), key=lambda x:abs(x[1][3] - mean_x))
                            mean_width = mean_diff[1][4] * 1.5
                            b_index = blocks.index(mean_diff[1])    #index of closest block
                            change_block = False
                            
                            #check if its mean difference or start-x difference is less than certain value
                            if abs(blocks[b_index][3]-mean_x) < mean_width or abs(blocks[b_index][1]-word[1][0][0]) < mean_width:
                                change_block = True
                            #else check if current block's mean-x is coming between 
                            # closest block's mean and its respective 'Current' type column's start-x
                            else:
                                for i,x in enumerate(columns):
                                    if x[4] == b_index and x[6] == 'Current' and blocks[-1][3] > blocks[b_index][3] and blocks[-1][3] < x[0]:
                                        change_block = True
                            if change_block:
                                #assign previous block's columns to new block iff
                                #all blocks doesnt have headers
                                if not block_with_headers or (blocks[b_index][0].lower() in self.deduction_headers and blocks[-1][0].lower() in self.deduction_headers):
                                    self.custom_print('assigning prev blocks columns to new block')
                                    for i in range(len(columns)):
                                        if columns[i][4] == b_index:
                                            columns[i][4] = len(blocks) - 1
                                self.custom_print('--Disabling block ',blocks[b_index][0])
                                blocks[b_index][5] = False
                        except:
                            pass

                #check if word belongs to general paytypes header    
                g = difflib.get_close_matches(word[0].lower(),general_paytype_headers,cutoff=0.80)
                if g:
                    g_pt_header = True
                    if word[0].lower() in ['description','pay type']:
                        self.pay_components.append([word,word[1][0][0],True,l_index])
                
                #check if word belongs to column headers
                c = difflib.get_close_matches(word[0].lower(),self.column_header_flags,cutoff=0.80)
                if c:
                    mw_factor = 1
                    self.custom_print('\nI am in C',word,c)
                    
                    #check if this column is already added in column list, if yes go to next word
                    goto_next_word = False
                    for i in columns:
                        if i[0] == word[1][0][0] and i[1] == word[1][0][1]:
                            goto_next_word = True
                            break
                    if goto_next_word:
                        continue
                    
                    #check if it belongs to any pre-defined sequence
                    try:
                        seq_word = difflib.get_close_matches(word[0],[j[0] for i in self.column_sequences for j in i],cutoff=0.80)
                        if seq_word:
                            probable_list = []
                            for s in seq_word:
                                for i in self.column_sequences:
                                    if s in [j[0] for j in i]:
                                        if i not in probable_list:
                                            probable_list.append(i)
                            status, columns, blocks, _ = self.find_column_sequence(line,word,probable_list,columns,blocks)
                            if status:
                                continue
                    except Exception as e:
                        self.custom_print(e)

                    #check if is of type current or ytd
                    if c[0] in self.current_col_flags:
                        col_type = 'Current'
                        check_flag = self.current_col_flags
                    elif c[0] in self.ytd_col_flags:
                        col_type = 'YTD'
                        check_flag = self.ytd_col_flags
                    elif c[0] in self.rate_col_flags:
                        col_type = 'Rate'
                        check_flag = self.rate_col_flags
                    elif c[0] in self.hour_col_flags:
                        col_type = 'Hour'
                        check_flag = self.hour_col_flags
                    elif c[0] in self.none_col_flags:
                        col_type = 'None'
                        check_flag = self.none_col_flags
                    else:
                        check_flag = self.other_col_flags
                        if not current_flag:
                            current_flag = True
                            g_pt_header = False
                            col_type = 'Current'
                        else:
                            if g_pt_header:
                                col_type = 'Current'
                                g_pt_header = False
                            else:
                                col_type = 'YTD'
                        #must deactivate Current or YTD column just above this, increase mw_factor
                        mw_factor = 6

                    #check if next word of line is part of this column itself, if yes, define end_x as ZERO
                    try:
                        if line[w_index+1][1][0][0] > word[1][1][0]:
                            if not difflib.get_close_matches(word[0].lower()+' '+line[w_index+1][0].lower(),check_flag,cutoff=0.80):
                                if difflib.get_close_matches(line[w_index + 1][0].lower(), self.column_header_flags, cutoff=0.80):
                                    end_x = line[w_index+1][1][0][0]
                                else:
                                    end_x = 0
                            else:
                                end_x = 0
                        else:
                            end_x = 0
                    except:
                        end_x = 0
                    columns.append([word[1][0][0],word[1][0][1],end_x,mean_x,None,word[0],col_type,word_height])
                    
                    
                    #check if it is blocking some other column headers, if yes deactivate that column
                    try:
                        mean_diff = min(enumerate(columns[0:-1]), key=lambda x:abs(x[1][3] - mean_x) if abs(x[1][1] - word[1][0][1]) >= x[1][7] else float('inf'))
                        mean_width = mean_diff[1][7] * 1.5 * mw_factor
                        if abs(mean_diff[1][3]-mean_x) < mean_width or abs(mean_diff[1][0]-word[1][0][0]) < mean_width:
                            #columns[mean_diff[0]][6] = False
                            columns.pop(mean_diff[0])
                            self.custom_print('We are blocking this column',mean_diff)
                    except:
                        pass
                    
                    #check the block where this column belongs to, 
                    try:
                        #get all blocks upto 3 lines above this column as per block height
                        y_diff = enumerate([x for x in blocks if x[5] == True and abs(x[2] - word[1][0][1]) < (3 * x[4])])
                        #look for closest block on left of column as per start-x of words
                        try:
                            mean_diff = min(y_diff,key=lambda x: word[1][0][0] - x[1][1] if word[1][0][0] - x[1][1] > 0 else float('inf'))
                        #else, look for closest block on right of column as per start-x of words
                        except:
                            mean_diff = min(y_diff,key=lambda x: x[1][1] - word[1][0][0] if x[1][1] - word[1][0][0] >= 0 else float('inf'))
                        b_index = blocks.index(mean_diff[1])
                        columns[-1][4] = b_index
                        
                        #DELETE COLUMNS IF THERE ARE MORE THAN ONE FOR SAME BLOCK SAME TYPE
                        num_cols = sum(1 for x in columns if x[4] == b_index and x[6] == columns[-1][6])
                        if num_cols > 1:
                            c_block = enumerate([x for x in columns if x[4] == b_index and x[6] == columns[-1][6]])
                            #find closest column to block using mean, if block name is above column name on y-axis
                            try:
                                mean_diff = min(c_block,key=lambda x: x[1][0] - blocks[b_index][1] if x[1][1] > blocks[b_index][2] else float('inf'))
                                if not mean_diff[1][1] > (blocks[b_index][2] + blocks[b_index][4]/2):
                                    raise Exception('Go to exception')
                            #else, look for closest column above this block, where block and column's x-axis is not same
                            except:                                
                                c_block = enumerate([x for x in columns if x[4] == b_index and x[6] == columns[-1][6]])
                                mean_diff = min(c_block,key=lambda x: x[1][0] - blocks[b_index][1] if x[1][0] != blocks[b_index][1] else float('inf'))
                                self.custom_print('In exception, might delete a column now')
                            
                            #pop all other columns for this block and type, except the one selected above.
                            pop_cols = []
                            for i,x in enumerate(columns):
                                if x[4] == mean_diff[1][4] and x[6] == mean_diff[1][6] and (x[0] != mean_diff[1][0] or x[1] != mean_diff[1][1]) and x[5] != mean_diff[1][5]:
                                    self.custom_print('deleting columns as more than one for same type ',x)
                                    pop_cols.append(i)
                            for i in reversed(pop_cols):
                                columns.pop(i)
                    except Exception as e:
                        self.custom_print(e)
                        #No blocks have been created yet.

                    self.custom_print('--Latest Columns-- ',columns)
                    self.custom_print('--Blocks-- ',blocks)
                    self.is_pay_component(word,l_index)
                    continue
                    #check the paytype where this column belongs to

                #if columns are created, start looking for float values
                if columns:
                    val = self.is_float(word[0])
                    if val:
                        try:
                            next_word = line[w_index+1][0]
                            if next_word == '*':
                                val = '*'+str(val)
                        except:
                            pass
                        for i, e in reversed(list(enumerate(columns))):
                            if word[1][1][0] > columns[i][3] and (word[1][1][0] <= columns[i][2] or columns[i][2] == 0):
                                #if block of this column is deactivated, no need to read values
                                try:
                                    if not blocks[columns[i][4]][5]:
                                        break
                                except:
                                    pass

                                #check if line number of value and component is different:
                                if not self.pay_components or l_index > self.pay_components[-1][3]:
                                    try:
                                        vertical_word = min(enumerate(lines[l_index+1]), key=lambda x: word[1][0][0] - x[1][1][1][0] if word[1][0][0] - x[1][1][1][0] >= 0 else float('inf'))
                                        self.custom_print('probable word is ',vertical_word)
                                        self.is_pay_component(vertical_word[1],l_index+1)
                                    except:
                                        pass
                                
                                if not self.pay_components:
                                    continue

                                if columns[i][2] == 0:
                                    if abs(columns[i][3] - word[1][0][0]) <= (3 * columns[i][7] * 1.5):
                                        columns[i][2] = word[1][1][0] + (3 * columns[i][7] * 1.5)
                                    try:
                                        data_blocks.append([self.pay_components[-1][0][0],self.final_float(val,columns[i][6]),columns[i][6],blocks[columns[i][4]][0]])
                                    except:
                                        data_blocks.append([self.pay_components[-1][0][0],self.final_float(val,columns[i][6]),columns[i][6],'Undefined'])
                                else:
                                    try:
                                        data_blocks.append([self.pay_components[-1][0][0],self.final_float(val,columns[i][6]),columns[i][6],blocks[columns[i][4]][0]])
                                    except:
                                        data_blocks.append([self.pay_components[-1][0][0],self.final_float(val,columns[i][6]),columns[i][6],'Undefined'])
                                self.custom_print(data_blocks[-1])
                                self.pay_components[-1][2] = True

                                #identify type of deduction, if component is of deduction
                                dh = difflib.get_close_matches(data_blocks[-1][3].lower(),self.deduction_headers,cutoff=0.90)
                                if dh:
                                    nh = difflib.get_close_matches(data_blocks[-1][3].lower(),self.normal_deduction_headers,cutoff=0.90)
                                    if nh:
                                        #code to find 'Total' pay component
                                        if difflib.get_close_matches(data_blocks[-1][0].lower(),['total','total '+data_blocks[-1][3].lower(),data_blocks[-1][3].lower()],cutoff=0.80):
                                            data_blocks[-1][0] = 'Total'
                                        elif "total" in data_blocks[-1][0].lower():
                                            data_blocks[-1][0] = 'Total'

                                        #code for identifying pre and post based on star or header
                                        if is_star_pre:
                                            #if star pre tax apply this rule
                                            if data_blocks[-1][0].find('*') != -1 or data_blocks[-1][1].find('*') != -1 or data_blocks[-1][0] == last_star_component:
                                                data_blocks[-1][0] = data_blocks[-1][0].replace('*','')
                                                data_blocks[-1][1] = data_blocks[-1][1].replace('*','')
                                                data_blocks[-1][3] = 'Pre Tax Deductions'
                                                last_star_component = data_blocks[-1][0]
                                                break
                                            else:
                                                data_blocks[-1][3] = 'Post Tax Deductions'
                                        elif is_pre_header_defined:
                                            identified_block = False
                                            try:
                                                pc_index = line.index(self.pay_components[-1][0])
                                                for i in range(pc_index+1,len(line)):
                                                    if line[i][0].lower() in ['yes','b','pre']:
                                                        identified_block = 'Pre Tax Deductions'
                                                        break
                                                    elif line[i][0].lower() in ['no','a','post']:
                                                        identified_block = 'Post Tax Deductions'
                                                        break
                                                if identified_block:
                                                    data_blocks[-1][3] = identified_block
                                                    break
                                            except:
                                                pass
                                    else:
                                        if difflib.get_close_matches(data_blocks[-1][3].lower(),self.pre_deduction_headers,cutoff=0.90):
                                            data_blocks[-1][3] = 'Pre Tax Deductions'
                                        else:
                                            data_blocks[-1][3] = 'Post Tax Deductions'
                                        break
                                    #code for identifying pre and post based on name if found
                                    if data_blocks[-1][0].lower().find('pre') != -1:
                                        data_blocks[-1][3] = 'Pre Tax Deductions'
                                    else:
                                        data_blocks[-1][3] = 'Post Tax Deductions'
                                    break
                                break
                    else:
                        if self.is_pay_component(word,l_index):
                            #check if it is blocking some column headers, if yes deactivate that column
                            try:
                                #if component contains any digit, do not block columns
                                if bool(re.search(r'\d', self.pay_components[-1][0][0])):
                                    #continue to next word
                                    continue
                                pop_cols = []
                                for i,x in enumerate(columns):
                                    if x[3] > word[1][0][0] and x[3] < word[1][1][0]:
                                        pop_cols.append(i)
                                for i in reversed(pop_cols):
                                    self.custom_print('word ',word[0],' is blocking this column ',columns[i])
                                    columns.pop(i)
                            except:
                                pass
        return data_blocks

    def read_data_dict(self,val_name):
        data_def = {
            'post_deduction_total_auto':['Post Tax Deductions','Total'],
            'pre_deduction_total_auto':['Pre Tax Deductions','Total'],
            'tax_total_auto':['Taxes','Total']
            }
        try:
            return data_def[val_name]
        except:
            return False

    def create_blocks(self,data_blocks):
        net_columns = ['net pay','total net','net earnings','net wages','total net pay',
                        'current net pay','ytd net pay','net pay current','net pay ytd']
        gross_columns = ['gross pay','total gross','gross earnings','gross',
                        'current gross','ytd gross','current gross pay','ytd gross pay',
                        'total gross earnings','cross pay','gross wages']
        other_columns = ['checking ','net check','checkng','Chck1',
                        'reimb & other payments',
                        'savings','direct deposit','dir dip check',
                        'your federal taxable wages this period','federal taxable wages',
                        'excluded from federal taxable wages','federal taxable']
        final_data = {'Net Pay':[],'Gross Pay':[],'Earnings':[],'Pre Tax Deductions':[],'Post Tax Deductions':[],'Taxes':[],'Others':[]}
        block_completed_flags = {
                'Earnings': False,
                'Pre Tax Deductions': False,
                'Post Tax Deductions': False,
                'Taxes': False,
        }
        
        prev_word = ''
        prev_block = ''
        temp_rate = temp_hour = ''
        temp_rate_val = temp_hour_val = 0.00
        ytd_left = False

        # for each value in data block
        for i,db in enumerate(data_blocks):
            #finalize block name based on column name or block name
            pc = difflib.get_close_matches(db[0].lower(),net_columns+gross_columns+other_columns,cutoff=0.85)
            if pc and db[0].lower() not in ['federal taxes','fed tax']:
                if pc[0] in net_columns:
                    block_name = 'Net Pay'
                    if 'ytd' in db[0].lower():
                        db[2] = 'YTD'
                elif pc[0] in gross_columns:
                    block_name = 'Gross Pay'
                    if 'ytd' in db[0].lower():
                        db[2] = 'YTD'
                else:
                    block_name = 'Others'
            else:
                bn = difflib.get_close_matches(db[3].lower(),self.earning_headers+self.tax_headers+['pre tax deductions','post tax deductions'],cutoff=0.80)
                if bn:
                    if bn[0] in ['pre tax deductions','post tax deductions']:
                        block_name = db[3]
                    elif bn[0] in self.earning_headers:
                        block_name = 'Earnings'
                    elif bn[0] in self.tax_headers:
                        block_name = 'Taxes'
                else:
                    if db[3].lower() in ['net pay distribution'] and db[0].lower() in ['total']:
                        block_name = 'Net Pay'
                        db[2] = 'Current'
                    else:
                        block_name = 'Others'
            
            #if block name is others, read data dict to find its true value if applicable
            if block_name == 'Others':
                summary_word = difflib.get_close_matches(db[0].lower(),[s[0].lower() for s in self.data_dict],cutoff=0.85)
                if summary_word:
                    s_index = [s[0] for s in self.data_dict].index(summary_word[0])
                    [bn, cn] = self.read_data_dict(self.data_dict[s_index][1]['col'])
                    db[0] = cn
                    block_name = bn
                else:
                    block_name = 'Others'

            #check if the component is total, if yes update name as 'Total'
            if difflib.get_close_matches(db[0].lower(),['total','total '+db[3].lower(),db[3].lower()],cutoff=0.80):
                db[0] = 'Total'
            elif "total" in db[0].lower():
                db[0] = 'Total'
            
            #change block name to others if block is completed already.
            try:
                if block_completed_flags[block_name] and not ytd_left:
                    block_name = 'Others'
            except:
                pass

            #add values of Rate, Hour, Current and YTD in final data with proper block name and components
            if db[2] == 'Rate':
                temp_rate = db[0]
                temp_rate_val = db[1]
            elif db[2] == 'Hour':
                temp_hour = db[0]
                temp_hour_val = db[1]
            elif db[2] == 'Current':
                final_data[block_name].append([db[0],db[1],'','',''])
                prev_word = db[0]
                prev_block = block_name
                if prev_word == temp_rate:
                    final_data[block_name][-1][3] = temp_rate_val
                    temp_rate = ''
                if prev_word == temp_hour:
                    final_data[block_name][-1][4] = temp_hour_val
                    temp_hour = ''
            elif db[2] == 'YTD':
                if db[0] == prev_word and block_name == prev_block:
                    final_data[block_name][-1][2] = db[1]
                    prev_word = ''
                    prev_block = ''
                else:
                    final_data[block_name].append([db[0],'',db[1],'',''])

            #check if block should be declared completed
            try:
                if db[0] == 'Total' and db[2] in ['Current','YTD']:
                    if len(final_data[block_name]) > 1 and not block_completed_flags[block_name]:
                        block_completed_flags[block_name] = True
                        ytd_left = True
                    else:
                        ytd_left = False
            except:
                pass

        
        #Calculate total of each block and add 'Total_calculated' component in blocks
        for x in final_data:
            if x in ['Pre Tax Deductions','Post Tax Deductions','Taxes','Earnings']:
                cal_cur = 0
                cal_ytd = 0
                for dt in final_data[x]:
                    if dt[0] != 'Total':
                        try:
                            if dt[1].find('+') != -1:
                                cal_cur = cal_cur - float(dt[1])
                            else:
                                cal_cur = cal_cur + float(dt[1])
                        except:
                            pass
                        try:
                            cal_ytd = cal_ytd + float(dt[2])
                        except:
                            pass
                final_data[x].append(['Total_Calculated',"{:.2f}".format(cal_cur),"{:.2f}".format(cal_ytd),'','']) 
        
        #Finalize Net Pay
        if len(final_data['Net Pay']) > 1:
            for i in final_data['Net Pay']:
                if i[1] != '' and i[2] != '':
                    final_data['Net Pay'] = [i]
                    break
        if len(final_data['Net Pay']) == 1:
            final_data['Net Pay'][0][0] = 'Net Pay'
            final_data['Net Pay'][0][1] = self.final_float(final_data['Net Pay'][0][1])
            final_data['Net Pay'][0][2] = self.final_float(final_data['Net Pay'][0][2])
        
        #Finalize Gross Pay
        if len(final_data['Gross Pay']) > 1:
            for i in final_data['Gross Pay']:
                if i[1] != '' and i[2] != '':
                    final_data['Gross Pay'] = [i]
                    break
        if len(final_data['Gross Pay']) == 1:
            final_data['Gross Pay'][0][0] = 'Gross Pay'
            final_data['Gross Pay'][0][1] = self.final_float(final_data['Gross Pay'][0][1])
            final_data['Gross Pay'][0][2] = self.final_float(final_data['Gross Pay'][0][2])
        elif len(final_data['Gross Pay']) == 0:
            #assign total of earnings block to gross pay if it is avaialable.
            try:
                for lt in final_data['Earnings']:
                    if lt[0] == 'Total':
                        final_data['Gross Pay'] = [['Gross Pay',lt[1],lt[2],'','']]
                        break
            except:
                pass

        return final_data

    def get_text(self,path,img=False):
        client = vision.ImageAnnotatorClient()
        ext = path.split('.')[-1]
        if not img:
            with io.open(path, 'rb') as image_file:
                self.image_content = image_file.read()
        else:
            b = io.BytesIO()
            if ext.lower() in ('png'):
                save_ext = 'PNG'
            elif ext.lower() in ('jpg','jpeg'):
                save_ext = 'JPEG'
            img.save(b, save_ext)
            self.image_content = b.getvalue()

        image = types.Image(content=self.image_content)
        
        response = client.document_text_detection(image=image)
        texts = response.text_annotations
        self.description = texts[0]
        
        height_list = []
        slanted_list = []
        rotated_list = []

        for text in texts[1:]:

            self.text_val.append(text.description)
            vertices = [(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices]
            self.keys.append(text.description)
            self.values.append(vertices)
            height_list.append(abs(vertices[0][1]-vertices[3][1]))
            slanted_list.append(abs(vertices[0][1]-vertices[1][1]))
            if vertices[0][1] > vertices[2][1]:
                rotated_list.append(270)
            elif vertices[1][1] > vertices[3][1]:
                rotated_list.append(90)
            else:
                rotated_list.append(0)
        self.result=zip(self.keys, self.values)
        data = " ".join(map(str, self.text_val))
        return data, height_list, slanted_list, rotated_list

    def get_paystub_type(self,paystub_types):
        lookups = [j for x in paystub_types for j in paystub_types[x]]
        if not lookups:
            return 'Generic'
        lookup_string = lookups[0]
        for i in range(1,len(lookups)):
            lookup_string = lookup_string+'|'+lookups[i]
        val = re.compile(r'\b(!?'+lookup_string+r')\b', re.IGNORECASE)
        lookup_found = val.findall(self.description.description)
        if lookup_found:
            for pt in paystub_types:
                if difflib.get_close_matches(lookup_found[0].lower(),[x.lower() for x in paystub_types[pt]],cutoff=0.90):
                    print('Paystub Type Found',pt)
                    return pt
        print('No type found, using Generic')
        return 'Generic'

    def get_structure(self,root,all_headers,paystub_type):
        for item in root.findall('./paystub'):
            if item.attrib.get('id') == paystub_type:
                paystub_structure = item
                break
        for table in paystub_structure.findall('./'):
            if table.tag in ['block_headers','col_headers']:
                #fresh list gets created for block and col headers
                if table.tag == 'block_headers':
                    all_headers['block_headers'] = {
                            'earnings':[],'normal_deductions':[],'pre_deductions':[],
                            'post_deductions':[],'taxes':[],'other':[],'none':[]}
                elif table.tag == 'col_headers':
                    all_headers['col_headers'] = {
                            'current':[],'ytd':[],'other_earnings':[],
                            'rate':[],'hour':[],'none':[]}
                for val_type in table.findall('./'):
                    type_id = val_type.attrib.get('id')
                    for vals in val_type.findall('./'):
                        all_headers[table.tag][type_id].append(vals.text)
            elif table.tag in ['col_sequence','vertical_col_sequence']:
                #fresh list gets created for col sequences
                all_headers[table.tag] = []
                for val_type in table.findall('./'):
                    all_headers[table.tag].append([])
                    for vals in val_type.findall('./'):
                        try:
                            all_headers[table.tag][-1].append([vals.text,vals.attrib])
                        except:
                            all_headers[table.tag][-1].append([vals.text,None])
            elif table.tag in ['data_val']:
                #data values are added in previous list
                if not table.tag in all_headers:
                    all_headers[table.tag] = {}
                for val_type in table.findall('./'):
                    type_id = val_type.attrib.get('id')
                    if not type_id in all_headers[table.tag]:
                        all_headers[table.tag][type_id] = []
                    for vals in val_type.findall('./'):
                        try:
                            all_headers[table.tag][type_id].append([vals.text,vals.attrib])
                        except:
                            all_headers[table.tag][type_id].append([vals.text,None])
            elif table.tag in ['data_dict']:
                all_headers[table.tag] = []
                for val_type in table.findall('./'):
                    all_headers[table.tag].append([val_type.text,val_type.attrib])
            else:
                all_headers['rules'] = []
                for val_type in table.findall('./'):
                    all_headers['rules'].append([val_type.text,val_type.attrib])
        return all_headers

    def remove_dotted_band(self):
        #img = cv2.imread(sys.argv[1], 0)
        img = Image.open(io.BytesIO(self.image_content))
        w, h = img.size
        if h+w > 5000:
            filter_size = 12
        else:
            filter_size = 5
        img = np.array(img) 

        #if image is not black and white already, convert it to grayscale
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img

        gray = cv2.threshold(gray, 127, 255,
                cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        img = cv2.medianBlur(gray, 1)
        
        _, blackAndWhite = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

        nlabels, labels, stats, _ = cv2.connectedComponentsWithStats(blackAndWhite, 4, cv2.CV_32S)
        sizes = stats[1:, -1] #get CC_STAT_AREA component
        img2 = np.zeros((labels.shape), np.uint8)
        
        for i in range(0, nlabels - 1):
            if sizes[i] >= filter_size:   #filter small dotted regions
                img2[labels == i + 1] = 255
        res = cv2.bitwise_not(img2)
        pilImage = Image.fromarray(res)
        return pilImage

    def check_gross_net(self,final_data):
        gp = np = False
        try:
            if float(final_data['Gross Pay'][0][1]) == float(final_data['Earnings'][-1][1]):
                gp = True
        except:
            pass
        try:
            if float(final_data['Net Pay'][0][1]) < float(final_data['Earnings'][-1][1]):
                np = True
        except:
            pass
        np_current_calculated = float(final_data['Earnings'][-1][1]) - (float(final_data['Taxes'][-1][1])+float(final_data['Pre Tax Deductions'][-1][1])+float(final_data['Post Tax Deductions'][-1][1]))
        np_ytd_calculated = float(final_data['Earnings'][-1][2]) - (float(final_data['Taxes'][-1][2])+float(final_data['Pre Tax Deductions'][-1][2])+float(final_data['Post Tax Deductions'][-1][2]))
        return gp, np, np_current_calculated, np_ytd_calculated

    def change_coordinates(self,mode_rotate,points):
        image = Image.open(io.BytesIO(self.image_content))
        width, height = image.size
        text_result = copy.deepcopy(self.result)

        new_result = []
        new_points = []

        slanted_list = []
        height_list = []
        if mode_rotate == 90:
            for v in text_result:
                for i in range(4):
                    v[1][i] = (v[1][i][1],width-v[1][i][0])
                height_list.append(abs(v[1][0][1]-v[1][3][1]))
                slanted_list.append(abs(v[1][0][1]-v[1][1][1]))
                new_result.append(v)
            for p in points:
                for i in range(4):
                    p[1][i] = (p[1][i][1],width-p[1][i][0])
                new_points.append(p)
        elif mode_rotate == 270:
            for v in text_result:
                for i in range(4):
                    v[1][i] = (height-v[1][i][1],v[1][i][0])
                height_list.append(abs(v[1][0][1]-v[1][3][1]))
                slanted_list.append(abs(v[1][0][1]-v[1][1][1]))
                new_result.append(v)
            for p in points:
                for i in range(4):
                    p[1][i] = (height-p[1][i][1],p[1][i][0])
                new_points.append(p)
        self.result = new_result
        return height_list, slanted_list, points

    def create_canvas(self):
        image = Image.open(io.BytesIO(self.image_content))
        #image.show()
        #return
        """
        width, height = image.size
        print(width, height)
        blank_image = np.zeros((height,width,3), np.uint8)
        blank_image = cv2.bitwise_not(blank_image)
        """
        blank_image = np.array(image)
        for t in self.result:
            cv2.circle(blank_image,t[1][0], 1, (0,0,255), -1)
        pilImage = Image.fromarray(blank_image)
        pilImage.show()
    
    def paystub_details(self,path):

        #get text data from GCV
        text_output_data, hl, sl, rl = self.get_text(path)
        result_output = copy.deepcopy(self.result)

        #get state code
        pa = paystub_address()
        pa_status, pa_points = pa.get_state_coordinates(self.description,self.result)
        if not pa_status and not pa_points:
            self.custom_print('We could not find state in this paystub')

        mode_rotate = max(set(rl), key=rl.count)
        if mode_rotate != 0:
            #code for rotating image by given degrees.
            hl, sl, pa_points = self.change_coordinates(mode_rotate,pa_points)

        mode_slant = max(set(sl), key=sl.count)
        mode_height = max(set(hl), key=hl.count)

        #self.create_canvas()
        #return

        #parse tree and get root element
        tree = ElementTree.parse('struct.xml')
        root = tree.getroot()
        paystub_structs = []
        for item in root.findall('./paystub'):
            paystub_structs.append(item.attrib.get('id'))


        #get all headers from Generic structure
        all_headers = {}
        all_headers = self.get_structure(root,all_headers,'Generic')

        #read all structure types and their lookup texts
        paystub_types = {}
        for item in root.findall('./paystub_types/'):
            type_id = item.attrib.get('id')
            paystub_types[type_id] = []
            for lookups in item.findall('./'):
                paystub_types[type_id].append(lookups.text)

        #get paystub type based on text
        paystub_type = self.get_paystub_type(paystub_types)
        if paystub_type != 'Generic':
            all_headers = self.get_structure(root,all_headers,paystub_type)


        #initilize structure to read paystub
        self.init_structure(all_headers)

        #convert raw data into line-wise structured data
        lines,state_lines = self.rectify_data(pa_points,mode_slant,mode_height)

        for line in lines:
            self.custom_print(line)

        address_details = []
        if state_lines:
            address_details = pa.get_address_lines(lines,state_lines)

        #get data blocks
        data_blocks = self.get_payslip_amounts(lines)

        #get output data from data blocks
        final_data = self.create_blocks(data_blocks)
        final_data['addresses'] = address_details

        if paystub_type == 'ADP':
            gp, np, np_cal_cur, np_cal_ytd = self.check_gross_net(final_data)
            if not gp or not np:
                self.custom_print('Old Final Data ADP',final_data)
                clear_image = self.remove_dotted_band()
                self.result={}
                self.text_val=[]
                self.keys=[]
                self.values=[]
                self.description = []
                text_output_data, _, _, _ = self.get_text(path,clear_image)

                if mode_rotate != 0:
                    #code for rotating image by given degrees.
                    _, _, pa_points = self.change_coordinates(mode_rotate,pa_points)

                #convert raw data into line-wise structured data
                lines,state_lines = self.rectify_data(pa_points,mode_slant,mode_height)

                #get data blocks
                data_blocks = self.get_payslip_amounts(lines)

                #get output data from data blocks
                new_final_data = self.create_blocks(data_blocks)
                gp_new, np_new, np_cal_cur_new, np_cal_ytd_new = self.check_gross_net(new_final_data)
                self.custom_print('New Final Data ADP: ',new_final_data)
                if not gp and gp_new:
                    final_data['Gross Pay'] = new_final_data['Gross Pay']
                if not np and np_new:
                    final_data['Net Pay'] = new_final_data['Net Pay']
     
                #remove second last element from earnings - (gross pay in dotted, erroneous)
                try:
                    if round(float(final_data['Earnings'][-1][1]) - float(final_data['Earnings'][-2][1]),2) == float(final_data['Gross Pay'][0][1]):
                        final_data['Earnings'].pop(-2)
                except:
                    pass

                #update other tables if they were not proper in prev iteration
                try:
                    if np_cal_cur != float(final_data['Net Pay'][0][1]) or np_cal_ytd != float(final_data['Net Pay'][0][2]):
                        if np_cal_cur_new == float(final_data['Net Pay'][0][1]) and np_cal_ytd_new == float(final_data['Net Pay'][0][2]):
                            final_data['Earnings'] = new_final_data['Earnings']
                            final_data['Pre Tax Deductions'] = new_final_data['Pre Tax Deductions']
                            final_data['Post Tax Deductions'] = new_final_data['Post Tax Deductions']
                            final_data['Taxes'] = new_final_data['Taxes']
                except:
                    pass


        print(final_data)
        return final_data, text_output_data, result_output

class paystub_address:
    def __init__(self):
        self.result={}
        self.description = []

    def custom_print(self,*arg):
        if DEBUG:
            print(arg)

    def get_data_in_box(self,bounding,lines):
        bounding_x1, bounding_y1 = bounding[0]
        bounding_x2, bounding_y2 = bounding[1]
        min_overlap = 40
        output_values = []
        for l_index,line in enumerate(lines):
            for _, values in enumerate(line):
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

    def get_state_coordinates(self,description,result):
        self.description = description.description
        
        self.result = copy.deepcopy(result)

        state_name = re.findall(r'\b(!?AL|AK|AS|AZ|AŽ|AŻ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY|York|YORK|JERSEY|Jersey)\s?\.?\,?\-?\s?(\d{5}(?:\s?\-\s?\d{1,4})|(\d{5}(?:\s?\,\s?\d{1,4})|\d{5}(?:\s?\.\s?\d{4})|\d{5}))', str(self.description))
        state = state_name
        all_points = []
        if not state:
            return False, []

        state_found = False
        state_search_try = 0
        found_val = []
        for _, values in enumerate(self.result):
            if state_found:
                if values[0] in state[len(all_points)][1]:
                    all_points.append(found_val)
                    state_search_try = 0
                    if len(all_points) == len(state):
                        break
                elif state_search_try == 2:
                    state_found = False
                    state_search_try = 0
                else:
                    state_search_try += 1
            if difflib.get_close_matches(values[0],[state[len(all_points)][0]],cutoff=0.90):
                state_found = True
                found_val = values
        if all_points:
            return True, all_points
        return False, []

    def get_address_lines(self,lines,state_lines):
        all_addresses = []
        for sl in state_lines:
            state_name = sl[0][0]
            sc_vertices = vertices = sl[0][1]
            on_left = 8
            on_right = 6
            state_word = [x for x in lines[sl[1]] if state_name+',' in x[0] or state_name+' ' in x[0] or state_name+'-' in x[0]]
            if state_word:
                if sc_vertices[0][0] < state_word[0][1][0][0]:
                    continue
                vertices = state_word[0][1]
                on_left = 2
                on_right = 2
            text_height = (vertices[0][1] - vertices[2][1])
            height = round(text_height * 4)

            third_pt_y = vertices[2][1] + (on_right * (sc_vertices[2][1]-sc_vertices[3][1]))
            third_pt_x = vertices[2][0] + (on_right * (sc_vertices[2][0]-sc_vertices[3][0]))
            
            first_pt_y = vertices[0][1] + round(on_left * (sc_vertices[0][1] - vertices[1][1]))
            first_pt_x = vertices[0][0] + round(on_left * (sc_vertices[0][0] - vertices[1][0]))
            first_pt_y += height
            
            data_box = self.get_data_in_box([(first_pt_x,first_pt_y),(third_pt_x,third_pt_y)],lines)
            if data_box:
                self.custom_print('Data box: ',data_box)
                status,details = self.extract_address(data_box,state_name)
                if not status:
                    pass
                else:
                    all_addresses.append(details)
            else:
                pass
        return all_addresses

    def extract_address(self,data_box,state_name):
        output = {'name':[]}
        if len(data_box) < 2:
            return False,[]

        prev_line_number = -1
        address_lines = []

        #convert data of multiple lines into joined words form in each line
        junk_words = ['employee address','employee name','address',
        'employer address','employer name','order','to the','of','exemptions/allowances']
        for db in reversed(data_box):
            self.custom_print('values are ',db[0])
            if db[0].lower() in junk_words:
                continue
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
        total_name_lines = 1

        for i,db in enumerate(address_lines):
            if not start_x:
                #look for word having state name, this should be the last line of our address
                for j,al in enumerate(db):
                    if state_name in al[0]:
                        output['address'] = [al[0]]
                        start_x = al[1][0][0]
                        start_y = al[1][0][1]
                        self.custom_print('found start_x',start_x)
                        a_height = abs(al[1][0][1] - al[1][3][1]) * 4
                        self.custom_print('height is ',a_height)
                        end_x = al[1][2][0]
                        break
                continue
            if re.search(r'\b(=?\d+\s)',output['address'][-1]):
                address_found = True
            min_diff = min(enumerate(db),key = lambda x: abs(x[1][1][0][0] - start_x))
            self.custom_print(min_diff,start_x)
            if abs(min_diff[1][1][0][0] - start_x) < a_height:
                if not address_found:
                    match_check = re.findall(r'((!?\d+)\s[A-Za-z]+)|([A-Za-z]+\s(!?\d+))|\d+',min_diff[1][0])
                    if match_check:
                        self.custom_print('Address line 2 finalized by first regex')
                        output['address'].insert(0,min_diff[1][0])
                        start_y = min_diff[1][1][0][1]
                        address_found = True
                    #check if third line is also address line
                    else:
                        try:                            
                            min_diff_1 = min(enumerate(db[i+1]),key = lambda x: abs(x[1][1][0][0] - start_x))
                            self.custom_print(min_diff_1)
                            match_check_1 = re.findall(r'((!?\d+)\s[A-Za-z]+)|([A-Za-z]+\s(!?\d+))|\d+',min_diff_1[1][0])
                            if match_check_1 and abs(min_diff_1[1][1][0][0] - start_x) < a_height:
                                self.custom_print('2nd and 3rd Address Lines Finalized')
                                output['address'].insert(0,min_diff[1][0])
                                output['address'].insert(0,min_diff_1[1][0])
                                start_y = min_diff_1[1][1][0][1]
                                address_found = True
                            else:
                                #it might be a name line
                                output['name'].insert(0,min_diff_1[1][0])
                                self.custom_print('Found a name line')
                                name_line_completed += 1
                                name_started = True
                                address_found = True
                        except:
                            address_found= True
                elif not name_started:
                    match_check = re.findall(r'((!?\d+)\s[A-Za-z]+)|([A-Za-z]+\s(!?\d+))|\d+',min_diff[1][0])
                    if match_check:
                        output['address'].insert(0,min_diff[1][0])
                        #self.custom_print('Address line 3 finalized')
                    else:
                        output['name'].insert(0,min_diff[1][0])
                        #self.custom_print('Found a name line')
                        name_line_completed += 1
                    name_started = True
                elif name_line_completed < total_name_lines:
                    output['name'].insert(0,min_diff[1][0])
                    #self.custom_print('Found another name line')
                    name_line_completed += 1
                if name_line_completed == total_name_lines:
                    break
            else:
                #self.custom_print('This word is out of box range')
                #now there is no chance for getting address, check if we can get name
                if i>2:
                    address_found = True
        #self.custom_print(output)
        return True,output


def main():
    pt = paystub_gcv()
    image_path = sys.argv[1]
    ext = image_path.split('.')[-1]
    if ext == 'pdf':
        split_path = os.path.split(os.path.abspath(image_path))
        filename = split_path[1].split('.')[0] + '.jpg'
        out_path = os.path.join(split_path[0],filename)
        image_path = image_path.replace(' ','\ ')
        out_path = out_path.replace(' ','\ ')
        subprocess.call('convert -density 300 -trim ' +image_path+ ' -quality 100 -append '+out_path,shell=True)
        image_path = out_path.replace('\ ',' ')
    pt.paystub_details(image_path)

"""
To run this program manually.
"""
if __name__ == "__main__":
    main()