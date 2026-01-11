from setuptools import setup, find_packages

setup(
    name="smart-ytdl",
    version="1.0.0",
    description="A Smart YouTube Downloader with GUI and CLI support",
    author="Your Name",
    packages=find_packages(),
    
    py_modules=['main'],
    
    install_requires=[
        "PyQt6",
        "yt-dlp",
        "requests",
    ],
    entry_points={
        'console_scripts': [
            'ytdownload=main:main',
        ],
    },
)