import PyPDF2
import re
import os

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

def parse_experience(text):
    # Look for patterns like "5 years", "5+ years", "Experience: 5 years"
    exp_pattern = re.compile(r'(\d+)\s*(?:\+)?\s*years?', re.IGNORECASE)
    matches = exp_pattern.findall(text)
    if matches:
        # Return the maximum found (often people list total experience or individual role durations)
        return max([int(m) for m in matches])
    return 0

def parse_education(text):
    text = text.lower()
    if 'phd' in text or 'doctorate' in text:
        return 'PhD'
    elif 'master' in text or 'm.sc' in text or 'm.tech' in text or 'mba' in text:
        return 'Master\'s'
    elif 'bachelor' in text or 'b.sc' in text or 'b.tech' in text or 'graduate' in text:
        return 'Bachelor\'s'
    return 'Bachelor\'s' # Default

def parse_role(text):
    text = text.lower()
    roles = {
        'Doctor': ['doctor', 'md', 'physician', 'medical practitioner'],
        'Surgeon': ['surgeon', 'surgical'],
        'Nurse': ['nurse', 'nursing', 'rn'],
        'Pharmacist': ['pharmacist', 'pharmacy', 'b.pharm'],
        'Dentist': ['dentist', 'dmd', 'dds'],
        'Physiotherapist': ['physiotherapist', 'physical therapist', 'pt'],
        'Medical Laboratory Technician': ['lab technician', 'medical laboratory', 'mlt'],
        'Electrical Engineer': ['electrical engineer'],
        'Mechanical Engineer': ['mechanical engineer'],
        'Civil Engineer': ['civil engineer'],
        'Software Engineer': ['software engineer', 'developer', 'programmer', 'coder', 'backend', 'frontend', 'fullstack'],
        'Data Engineer': ['data engineer', 'etl engineer'],
        'Chemical Engineer': ['chemical engineer'],
        'Network Engineer': ['network engineer', 'systems engineer'],
        'Data Scientist': ['data scientist', 'data science'],
        'Machine Learning Engineer': ['machine learning', 'ml engineer'],
        'AI Researcher': ['ai researcher', 'artificial intelligence'],
        'Cybersecurity Analyst': ['cybersecurity', 'security analyst', 'infosec'],
        'DevOps Engineer': ['devops', 'site reliability engineer', 'sre'],
        'Cloud Architect': ['cloud architect', 'aws', 'azure', 'gcp'],
        'Database Administrator': ['database administrator', 'dba'],
        'Sales Manager': ['sales manager', 'account manager'],
        'Marketing Manager': ['marketing manager', 'brand manager'],
        'Product Manager': ['product manager', 'pm'],
        'Operations Manager': ['operations manager', 'ops manager'],
        'Business Analyst': ['business analyst', 'ba'],
        'Human Resources Manager': ['hr manager', 'human resources manager'],
        'Project Manager': ['project manager', 'pmp'],
        'Accountant': ['accountant', 'ca', 'cpa'],
        'Financial Analyst': ['financial analyst'],
        'Investment Banker': ['investment banker'],
        'Auditor': ['auditor', 'internal audit'],
        'Tax Consultant': ['tax consultant', 'taxation'],
        'Lawyer': ['lawyer', 'attorney', 'legal'],
        'Compliance Officer': ['compliance officer'],
        'Teacher': ['teacher', 'educator', 'school teacher'],
        'Professor': ['professor', 'lecturer', 'academic'],
        'Research Scientist': ['research scientist'],
        'Academic Counselor': ['academic counselor', 'career counselor'],
        'Training Specialist': ['training specialist', 'l&d'],
        'Graphic Designer': ['graphic designer', 'creative designer'],
        'UI/UX Designer': ['ui/ux', 'product designer', 'user interface'],
        'Content Writer': ['content writer', 'copywriter'],
        'Video Editor': ['video editor'],
        'Animator': ['animator', '3d artist'],
        'Journalist': ['journalist', 'reporter'],
        'Social Media Manager': ['social media manager'],
        'Electrician': ['electrician'],
        'Plumber': ['plumber'],
        'HVAC Technician': ['hvac'],
        'Welder': ['welder'],
        'Automotive Technician': ['automotive technician', 'mechanic'],
        'Construction Supervisor': ['construction supervisor'],
        'Store Manager': ['store manager', 'retail manager'],
        'Customer Support Executive': ['customer support', 'customer service'],
        'Retail Sales Associate': ['retail sales', 'sales associate'],
        'Cashier': ['cashier'],
        'Call Center Representative': ['call center'],
        'Supply Chain Manager': ['supply chain'],
        'Logistics Coordinator': ['logistics'],
        'Warehouse Manager': ['warehouse manager'],
        'Procurement Specialist': ['procurement', 'purchasing'],
        'Chef': ['chef', 'cook'],
        'Hotel Manager': ['hotel manager', 'hospitality manager'],
        'Travel Consultant': ['travel consultant', 'travel agent'],
        'Event Manager': ['event manager', 'event planner'],
        'Flight Attendant': ['flight attendant', 'cabin crew'],
        'Police Officer': ['police officer', 'cop'],
        'Firefighter': ['firefighter'],
        'Army Officer': ['army officer', 'military officer'],
        'Administrative Officer': ['administrative officer', 'admin officer'],
        'Manager': ['manager', 'lead', 'head', 'director', 'vp'],
        'Analyst': ['analyst', 'data analyst'],
        'HR': ['hr', 'human resources', 'recruitment', 'talent acquisition']
    }
    
    for role, keywords in roles.items():
        if any(keyword in text for keyword in keywords):
            return role
    return 'Software Engineer' # Default

def extract_features(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    if not text:
        return None
    
    features = {
        'Experience': parse_experience(text),
        'Education': parse_education(text),
        'Role': parse_role(text)
    }
    return features

if __name__ == "__main__":
    # Test with dummy text
    dummy_text = "I have 5 years of experience as a Software Developer. I hold a Master's degree in Computer Science."
    print(f"Exp: {parse_experience(dummy_text)}")
    print(f"Edu: {parse_education(dummy_text)}")
    print(f"Role: {parse_role(dummy_text)}")
