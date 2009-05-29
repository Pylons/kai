try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='kai',
    version='0.1',
    description='',
    author='Ben Bangert',
    author_email='ben@groovie.org',
    install_requires=[
        "Pylons>=0.9.7rc4", "CouchDB>=0.4", "python-openid>=2.2.1",
        "pytz>=2008i", "Babel>=0.9.4", "tw.forms==0.9.3", "docutils>=0.5",
        "PyXML>=0.8.4", "cssutils>=0.9.6a0", "Pygments>=1.0",
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'kai': ['i18n/*/LC_MESSAGES/*.mo']},
    message_extractors = {'kai': [
            ('**.py', 'python', None),
            ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
            ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = kai.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
