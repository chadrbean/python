from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from proceedure_method import compare_words

#Starting Working Directory For Refrence Point Of Where Python Was Ran From
starting_wd = os.getcwd()

# Function To keyword Map which contains all info to rename file
def json_keys():
    final_rules = []
    os.chdir(starting_wd+'/rules')
    print(os.getcwd())
    dirs = os.listdir()
    for eachfile in dirs:
        if '.json' in eachfile:
            with open(eachfile) as rulefile:
                rules = json.load(rulefile)
                final_rules.append(rules)
    return final_rules

# Open Pdf and extract useful data
def open_pdf(file_name):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    print(os.getcwd())
    with open(file_name, 'rb') as fp:
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()
    device.close()
    retstr.close()
    print(text)
    return text

#Function To Do the Actual Rename Of File
def auto_rename(pdf_file, file, finalname_list):

    #Variable that date slices go into
    final_date = ''
    #pdfminer get creation date
    with open(file, 'rb') as file_date:
        parser = PDFParser(file_date)
        doc = PDFDocument(parser)
        file_date.close()

    #Slice the main date part, had to specifiy date because it was a byte datatype
    date = str(doc.info[0]['CreationDate'])[4:14]

    #date slicing and random.int to stop overwritting of files and make unique
    final_date += date[0:4] + '-' + date[4:6] + '-' + date[6:8] + '-' + date[8:10] + date[10:12] + '-' + str(random.randint(1, 99))
    final_filename = final_date + ' - ' + ''.join(finalname_list[0])
    if final_filename in os.listdir():
        print(f'You Are Overwritting a File {final_filename}')

    print(f'this is the filename BEFORE {file}')

    os.rename(file, final_filename)
    print(f'this is the filename AFTER {final_filename}')


def find_matchL1(pdf_file, json_keys):

    for inlist in json_keys:
        for keyword in inlist['keywords']:
            if keyword in pdf_file:

                return inlist


def find_matchL2(pdf_file, found_matchL1):

    for keyword in found_matchL1['l2keywords']:
        if keyword in pdf_file:
            return (found_matchL1['l2keywords'][keyword])


def run_rename(json_keys, set_folder):
    os.chdir(set_folder)
    # Change source directory where files will be renamed from
    source_directory = set_folder
    # Change target directory where renamed files will be moved to

    enum_folder = os.listdir(source_directory)
    try_counter = 0
    except_counter = 0
    for file in enum_folder:
        #Make sure it is a PDF file or else i was getting system files causing errors
        if '.pdf' in file:
            try:
                try_counter += 1
                finalname_list = []

                #extract OCR data and return to match with keywords:
                pdf_file = open_pdf(file)
                #make contents lowercase
                pdf_file = pdf_file.lower()
                #call level one function to match first level keyword with ocrdata
                found_matchL1 = find_matchL1(pdf_file, json_keys)

                #if keyword matches True then
                print('this is after fount_matchl1')
                if found_matchL1 is not None:
                    #See if there is a L2 keyword to match
                    found_matchL2 = find_matchL2(pdf_file, found_matchL1)
                    if found_matchL2 is not None:
                        #if L2 keyword matches then create a list with the Type - Name - Keyword - L2Keyword
                        #Call file rename function
                        finalname_list.append([found_matchL1['type'], ' - ', found_matchL1['prettyname'], ' - ', found_matchL2,'.pdf'])
                        print(f'this is the file sent to autorename1 {file}')
                        auto_rename(pdf_file, file, finalname_list)

                    elif found_matchL2 is None:

                        # If no L2 Keyword is found rename the file wihtout a L2keyword
                        # call file rename function
                        # I would like to add a function to add rules and rerun to get the second match
                        finalname_list.append([found_matchL1['type'], ' - ', found_matchL1['prettyname'], '.pdf'])
                        print(f'this is the file sent to autorename2 {file}')
                        auto_rename(pdf_file, file, finalname_list)
                # Catch files that dont match any rules
                else:
                    print(f'File did NOT match any rules {file}')
                    continue
            except:
                except_counter += 1

def menu():

    # Open keyword csv and parse/split into a dictionary with key being the company.
    # This will be used for the autorename and file move functions
    set_folder = str(input('What Is The Full Folder Path Of Your PDF Files? >'))
    keys = json_keys()


    while True:
        print('\n\nThis Program Automatically Renames and Sorts PDF Files Into Directories of Your Choosing')
        print('Please Set Menu Option #1 First In Order To Specify Where Your PDF Files Are Located')
        print('Option #3 Is Useful In Determining What Keywords To Use In Creating The JSON Files\n ')
        print(f'Your Current Folder Location is: {set_folder}\n')
        user_input = int(input("1.) - View The OCR Data of A Individual File\n"
              "2.) - View The JSON Rule Files\n"
              "3.) - Compare OCR Data of An Entire Folder and Count How Many Times That Word Appears\n"
              "4.) - Start AutoRename Process Of Files You Set In Folder From Option #1\n"
              "5.) - Exit This Probram\n"
              "> "))
        try:
            if user_input <= 5:
                if user_input == 1:
                    ocr_file = input('Enter The File including Full Path That You Wish To View The OCR Contents? > ')
                    ocr_data = open_pdf(ocr_file)
                    print(ocr_data)
                if user_input == 2:
                    key_counter = 0
                    for key in keys:
                        print(f'Item Number: {key_counter}')
                        print(key)
                        key_counter += 1
                if user_input == 3:
                    word_path = input('Which Folder Would You Like To Compare Words From? Make Sure EOL Has A "/" > ')
                    compared_words = compare_words.run_compare_words(word_path)
                    print(compared_words)
                    with open(starting_wd + '/word_compare.csv', 'w') as cwords:
                        cwords.write(compared_words)
                if user_input == 4:
                    run_rename(keys, set_folder)
                    print(matches_found, match_notfound)
                if user_input == 5:
                    print('You Chose To Quit The Program!!')
                    break
        except:
            print('You Typed An Invalid Number. Please Try Again')
            continue

#Start Program Menu
menu()

