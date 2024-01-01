from pyresparser import ResumeParser
import PyPDF2
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def read_text_from_pdf(PDF_file_path):
    with open(PDF_file_path, 'rb') as file:
        read_text = ''
        read_PDF_file = PyPDF2.PdfReader(file)
        
        for num_of_pages in range(len(read_PDF_file.pages)):
            extracted_pages = read_PDF_file.pages[num_of_pages]
            read_text += extracted_pages.extract_text()
    return read_text

def extract_skills(read_text):
    skills_list = ['Premiere Pro,','android development','flutter','kotlin','xml','kivy','ios','ios development','swift','cocoa','Angularjs','Python',
                    'cocoa touch','xcode','html','css','sass','mongodb','mysql','ux','adobe xd','figma','canva','zeplin','balsamiq','ui','prototyping','wireframes',
                    'storyframes','adobe photoshop','photoshop','editing','adobe illustrator','illustrator','adobe after effects',
                    'after effects','adobe premier pro','premier pro','adobe indesign','After Effects','indesign','wireframe','solid','grasp','Java Script',
                    'user research','user experience','Data Visualization','Predictive Analysis','Statistical Modeling','Data Mining',
                    'Clustering & Classification','Data Analytics','Quantitative Analysis','Web Scraping', 'Data Analysis',
                    'ML Algorithms','Keras','Pytorch','Probability','Scikit-learn','Tensorflow',"Flask",'Streamlit','MATLAB',
                    'React','Django','Node JS','React JS','php','laravel','Magento','wordpress','Javascript','Angular JS','c#','SDK', 'R',
                    'Android','Android development','Flutter','Kotlin','XML','Java','Kivy','GIT','SDK','SQLite', 'ML','CVS','LaTeX','Machine Learning',
                    'Financial modeling']

    words = word_tokenize(read_text)

    stop_words = set(stopwords.words("english"))
    words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

    extracted_skills = [skill for skill in skills_list if any(re.search(rf'\b{re.escape(skill.lower())}\b', ' '.join(words)) for word in words)]
    return extracted_skills

def extract_resume_info(file_path):
    data = ResumeParser(file_path).get_extracted_data()

    name = data.get('name', None)
    email = data.get('email', None)
    contact_number = data.get('mobile_number', None)

    resume_text = read_text_from_pdf(file_path)
    skills = extract_skills(resume_text) if resume_text else []

    return {
        "Name": name,
        "Email": email,
        "Contact Number": contact_number,
        "Skills": skills
    }

if __name__ == "__main__":
    pdf_paths_lst = []

    for i in range(3):
        input_resume_path = input(f'Enter PDF Resume of Candidate {i + 1}: ')
        pdf_paths_lst.append(input_resume_path)

    for input_resume_path in pdf_paths_lst:
        result = extract_resume_info(input_resume_path)

        print(f"\nName: {result['Name']}")
        print(f"Email: {result['Email']}")
        print(f"Contact Number: {result['Contact Number']}")

        if result['Skills']:
            print("\nSkills:")
            for skill in result['Skills']:
                print(f"- {skill}")
        else:
            print("\nNo skills found in the Uploaded Resume :)")
