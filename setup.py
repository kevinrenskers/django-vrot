from distutils.core import setup

setup(
    name="django-vrot",
    version=__import__("vrot").get_version(),
    description="A collection of Django templatetags, context processors, middleware and other reusable hacks.",
    long_description=open("README.md").read(),
    author="Kevin Renskers",
    author_email="info@mixedcase.nl",
    url="https://github.com/kevinrenskers/django-vrot",
    packages=[
        "vrot",
    ],
    package_dir={"vrot": "vrot"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        "Framework :: Django",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
