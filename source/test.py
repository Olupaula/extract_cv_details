import cv_extractor as cve
from nltk import pos_tag
from PyPDF4 import PdfFileReader

# The file of interest
file = open('../cvs/testing_cv.pdf', 'rb')
reader = PdfFileReader(file)

# get the total number of pages in the pdf document
no_of_pages = reader.getNumPages()

# reading the text from all the pages
text = ""
for no in range(no_of_pages):
    page = reader.getPage(no)
    text += page.extractText()

# text = 'f@gmail.com, j@yahoo.com, mark@skynet.com'
# the result
contact_number = cve.get_contact_number(text)
email = cve.get_email(text)
skills = cve.get_skills(text, skill_list=['python', 'django', 'writing'])
education = cve.get_education(text, degrees=['msc', 'bsc', 'ssce'])
name = cve.get_name(file, email)

print('contact name:', contact_number)
print('email:', email)
print('skills:', skills)
print('education:', education)
print('name:', name)
