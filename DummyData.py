import os
import django
import random
from faker import Faker
from datetime import datetime, timedelta

# Ensure correct settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airozgar.settings')  # Update with correct project name

# Setup Django
django.setup()

# Now import models
from django.contrib.auth.models import User
from home.models import Company, Job, Internship  # Replace 'home' with the actual app name

fake = Faker()

# Predefined fields, categories, job descriptions, responsibilities, and skills
fields = ['AI', 'ML', 'MLOps', 'Data Scientist']
categories = {
    'AI': ['Computer Vision', 'NLP', 'Signal Processing'],
    'ML': ['Computer Vision', 'NLP', 'Signal Processing'],
    'MLOps': ['MLOps'],
    'Data Scientist': ['Data Scientist']
}

job_details = {
    'AI': {
        'titles': ['AI Engineer', 'AI Research Scientist', 'AI Developer', 'AI Software Engineer'],
        'description': """We are seeking an enthusiastic AI Engineer to join our team and contribute to the development of AI-based solutions. 
        As a fresher, you will assist in building and optimizing AI models and algorithms. You will work with datasets to train AI systems 
        that can understand and process natural language, images, and other forms of data. The ideal candidate is curious, 
        has a basic understanding of machine learning, and is eager to learn more about AI technologies.""",
        'responsibilities': [
            'Assist in building AI models and algorithms for real-world applications.',
            'Participate in training and evaluating AI models using datasets.',
            'Collaborate with cross-functional teams to integrate AI solutions.',
            'Conduct research to enhance existing AI algorithms and implement new features.',
            'Document all processes and code for future reference and updates.'
        ],
        'skills': [
            'Basic understanding of AI and machine learning concepts.',
            'Familiarity with Python and AI frameworks like TensorFlow or PyTorch.',
            'Good problem-solving skills and willingness to learn.',
            'Ability to work in a team and communicate effectively.',
            'Analytical mindset with attention to detail.'
        ]
    },
    'ML': {
        'titles': ['Machine Learning Engineer', 'ML Scientist', 'Deep Learning Engineer', 'ML Researcher'],
        'description': """We are looking for a passionate Machine Learning Engineer to help build ML models and applications. 
        Freshers will collaborate with the team to solve business challenges by applying machine learning techniques to real-world problems. 
        You will gain hands-on experience in developing, testing, and deploying machine learning models, enabling you to contribute to impactful projects.""",
        'responsibilities': [
            'Assist in developing and training machine learning models.',
            'Help fine-tune machine learning algorithms for better performance.',
            'Support in deploying models into production environments.',
            'Analyze data sets to derive actionable insights and identify patterns.',
            'Work closely with data engineers to optimize data pipelines and processes.'
        ],
        'skills': [
            'Basic knowledge of machine learning algorithms and principles.',
            'Familiarity with Python and libraries like scikit-learn, NumPy, and Pandas.',
            'Interest in deep learning frameworks such as TensorFlow or PyTorch.',
            'Strong analytical skills and a passion for data.',
            'Effective communication skills for collaboration with team members.'
        ]
    },
    'MLOps': {
        'titles': ['MLOps Engineer', 'MLOps Architect', 'ML Infrastructure Engineer'],
        'description': """We offer an exciting opportunity for an MLOps Engineer to streamline ML operations. 
        As a fresher, you will gain hands-on experience in automating ML models, managing infrastructure, and enhancing deployment processes. 
        This role is crucial in ensuring that our machine learning models are efficient, scalable, and easily maintainable.""",
        'responsibilities': [
            'Help set up and maintain machine learning pipelines and infrastructure.',
            'Assist in automating the deployment of models into production.',
            'Collaborate with data scientists and engineers to implement CI/CD pipelines.',
            'Monitor and troubleshoot deployed models for optimal performance.',
            'Document processes and best practices for model deployment and management.'
        ],
        'skills': [
            'Basic knowledge of machine learning lifecycle and DevOps concepts.',
            'Familiarity with cloud platforms (AWS, GCP, or Azure).',
            'Understanding of Docker or Kubernetes for containerization.',
            'Strong problem-solving skills and a detail-oriented mindset.',
            'Ability to learn new tools and technologies quickly.'
        ]
    },
    'Data Scientist': {
        'titles': ['Data Scientist', 'Big Data Scientist', 'Predictive Analytics Specialist'],
        'description': """We are looking for a motivated Data Scientist to analyze and interpret data for actionable insights. 
        Freshers will work on data cleaning and exploration, using statistical techniques to analyze data sets and identify trends. 
        You will collaborate with stakeholders to understand their data needs and provide data-driven solutions that drive business growth.""",
        'responsibilities': [
            'Assist in analyzing and interpreting data to provide actionable insights.',
            'Work on data cleaning, pre-processing, and exploration tasks.',
            'Collaborate with the team to develop predictive models using machine learning algorithms.',
            'Create visualizations and reports to present findings to non-technical stakeholders.',
            'Stay updated on industry trends and emerging technologies in data science.'
        ],
        'skills': [
            'Basic understanding of statistics, data analysis, and machine learning.',
            'Proficiency in Python and data science libraries (Pandas, NumPy, Matplotlib).',
            'Familiarity with SQL and databases for data retrieval and manipulation.',
            'Good communication skills to explain data insights to stakeholders.',
            'Curiosity and willingness to explore new tools and techniques.'
        ]
    }
}

# Function to generate dummy data
def generate_dummy_data():
    Job.objects.all().delete()
    Internship.objects.all().delete()
    Company.objects.all().delete()
    companies = []

    # Create 10 Company entries
    for _ in range(10):
        user = User.objects.create_user(username=fake.user_name(), password='password123')
        company_name = fake.company()
        company = Company.objects.create(
            user=user,
            company_name=company_name,
            phone_number=fake.phone_number(),
            email=f'{company_name.replace(" ", "").lower()}@gmail.com',
            website=f'www.{company_name.replace(" ", "").lower()}.com',
            location=fake.address()
        )
        companies.append(company)
        print(f'Created Company: {company_name}')

    # Create 20 Job entries
    for _ in range(20):
        company = random.choice(companies)
        job_field = random.choice(fields)

        if job_field in ['ML', 'AI']:
            job_category = random.choice(categories[job_field])
        else:
            job_category = job_field

        job_title = random.choice(job_details[job_field]['titles'])
        job_description = job_details[job_field]['description']
        job_responsibilities = "\n".join(job_details[job_field]['responsibilities'])
        job_skills = ", ".join(job_details[job_field]['skills'])

        job = Job.objects.create(
            company=company,
            title=job_title,
            description=f"{job_description}\n\nResponsibilities:\n{job_responsibilities}",
            field=job_field,
            category=job_category,
            pay_range=f"{random.randint(300000, 1000000)} - {random.randint(1100000, 3000000)}",
            location=fake.city(),
            expiry_date=fake.date_between(start_date='today', end_date='+30d'),
            skills=job_skills,
            student_applied=[]
        )
        print(f'Created Job: {job.title} ({job_field}) at {company.company_name}')

    # Create 20 Internship entries
    for _ in range(20):
        company = random.choice(companies)
        internship_field = random.choice(fields)

        if internship_field in ['ML', 'AI']:
            internship_category = random.choice(categories[internship_field])
        else:
            internship_category = internship_field

        internship_title = random.choice(job_details[internship_field]['titles'])
        internship_description = job_details[internship_field]['description']
        internship_responsibilities = "\n".join(job_details[internship_field]['responsibilities'])
        internship_skills = ", ".join(job_details[internship_field]['skills'])

        internship = Internship.objects.create(
            company=company,
            title=f"Internship - {internship_title}",
            description=f"{internship_description}\n\nResponsibilities:\n{internship_responsibilities}",
            field=internship_field,
            category=internship_category,
            stipend=f"{random.randint(1000, 50000)}",
            location=fake.city(),
            expiry_date=fake.date_between(start_date='today', end_date='+30d'),
            skills=internship_skills,
            student_applied=[]
        )
        print(f'Created Internship: {internship.title} ({internship_field}) at {company.company_name}')

# Run the script when the file is executed directly
if __name__ == "__main__":
    generate_dummy_data()
