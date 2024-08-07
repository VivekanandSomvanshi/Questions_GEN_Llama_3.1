from setuptools import setup, find_packages

setup (
            name="mcq_generator",
            version="0.0.1",
            author = "Vivekanand Somvanshi",
            author_email='somvanshivivek7@gmail.com',
            install_requires=["groq","langchain","streamlit","python-dotenv","langchain-core",'langchain-groq','langchain-community','pandas'],
            packages=find_packages(),
    
    )