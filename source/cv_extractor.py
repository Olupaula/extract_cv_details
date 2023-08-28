from PyPDF3 import PdfFileReader
from nltk import pos_tag
from nltk.corpus import stopwords
import re
from nltk.corpus import names

name_bank = list(names.words())
stopwords = stopwords.words('english')


def get_contact_number(supplied_text):
    """
    Get the phone numbers in a CV, the first number of which is likely to be the CV owner's number using
    m1 and m2 methods and take which ever is not empty.
    :param supplied_text: the supplied text
    :return: contact number of the candidate
    """

    # first method (m1)
    search_result = re.search(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', supplied_text)
    contact_number_m1 = ''.join(search_result.group().split()) if search_result else None

    # second method (m2)
    contact_number_m2 = [
        int(re.sub(r'[^\w\s]', '', x)) for x in supplied_text.split()
        if "+" in x
        and re.sub(r'[^\w\s]', '', x).isnumeric()
        and len(re.sub(r'[^\w\s]', '', x)) >= 10
    ]

    return contact_number_m1 if contact_number_m1 is not [] else contact_number_m2


# getting email
def get_email(supplied_text):
    """
    Gets email from the text using two methods
    :param supplied_text: the text read from a pdf file.
    :return: the email of the candidate
    """
    # using method one (m1)
    search_result = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', supplied_text)
    email_m1 = search_result.group() if search_result else None

    # using method two (m2)
    email_m2 = [x.rstrip('.,;+\"\'!#$%*_-+=/><?&*') for x in supplied_text.split() if "@" in x]
    confirmed_email = True if email_m1 in email_m2 else False
    return email_m1 if confirmed_email else ""


def get_skills(supplied_text, skill_list):
    """
    :param supplied_text: the text read from a pdf file.
    :param skill_list: a list of skills desired by the recruiter.
    :return: the skills the candidate has, of the skills desired by the recruiter.
    """
    split_text = [x.rstrip('.,;+\"\'!#$%*_-+=/><?&*') for x in supplied_text.lower().split()]

    # skill_pos is the index position in which the word skill appears.
    skill_pos = (
        split_text.index('skills')
        if 'skills' in split_text
        else split_text.index('skill') if 'skill' in split_text
        else None
    )

    # Take only texts that come after position skill_pos
    contains_skills = split_text[skill_pos+1:] if skill_pos is not None else []
    skills = list(set(skill for skill in contains_skills if skill in skill_list))
    return skills


def get_education(supplied_text, degrees):
    """
    :param supplied_text: the text obtained from a pdf
    :param degrees: the degrees in which the recruiter is interested
    :return: the degrees owned by the candidate, of the degrees which are of interest to the recruiter.
    """
    split_text = [re.sub(r'[^\w\s]', '', x) for x in supplied_text.lower().split()]
    degrees_acquired = list(set(degree for degree in split_text if degree in degrees))
    return degrees_acquired


def get_name(file, email):
    """
    Returns applicants name based on email. If the name is contained in the email, then it likely the name.
    This algorithm uses only the first page of the cv. If the cv owner has no email, the algorithm may fail.
    :param email: a list of emails obtained from the cv.
    :param the file: the pdf file from which a text is to be read.
    :return: the names
    """
    needed_text = PdfFileReader(file).getPage(0).extractText()
    split_text = list(set(re.sub(r'[^\w\s]', '', x) for x in needed_text.split()
                          if x.lower() not in stopwords))
    names_and_tags = pos_tag(split_text)

    # remove all words that are not names, upper case words and include any word that can be found in
    # the cv owner's name and names that can be found in the name_bank
    name = [x[0] for x in names_and_tags if x[1] == 'NNP'
            and x[0].lower() and not(x[0].isupper())
            and (x[0].lower() in email
            or x[0] in name_bank)]
    return name[:3]


