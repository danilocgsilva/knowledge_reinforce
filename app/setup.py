from setuptools import setup, find_packages

setup(
    name="knowledge_reinforce",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    author="Danilo Silva",
    author_email="contact@danilocgsilva.me",
    description="Storage knowledge reinforcement",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/danilocgsilva/knowledge_reinforce",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)