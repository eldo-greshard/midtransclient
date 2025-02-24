from setuptools import find_packages, setup

setup(
    name="midtransclient",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "django",
    ],
    include_package_data=True,
    description="A reusable Midtrans client for Django projects",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/midtransclient",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
    ],
)
