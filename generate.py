#!/usr/bin/env python3
# This is a simple script to generate different versions (current TeX and
# plaintext) of my resume from the 'resume.json' data file.

import argparse
import json
import re
import sys
import textwrap

# TODO: make this regex work for more general URLs (cover more cases)
url_regex = re.compile(r'https?://[A-Za-z0-9_/.-]*[A-Za-z0-9_/-]')

class Outputter:
    def __init__(self, output=sys.stdout):
        self.output = output

    def format_address(self, address):
        return address

    # Format all URLs in the input string.
    def format_all_urls(self, text):
        new_text = ''
        match = url_regex.search(text)
        while match is not None:
            new_text += text[:match.start()] + self.format_url(match.group(0))
            text = text[match.end():]
            match = url_regex.search(text)
        new_text += text
        return new_text

    def format_date(self, date):
        return date

    def format_summary(self, summary):
        return textwrap.fill(self.format_all_urls(summary), width=80)

    def print(self, text=None):
        if text is None:
            self.output.write('\n')
        else:
            self.output.write(text + '\n')

    def print_education(self, education):
        self.print(self.format_heading('Education'))
        for school in education:
            self.print_school(school)
            self.print()

    def print_experience(self, experience):
        self.print(self.format_heading('Experience'))
        for job in experience:
            self.print_job(job)
            self.print()

    def print_publications(self, publications):
        self.print(self.format_heading('Publications and presentations'))
        pub_list = ['{} ({})'.format(pub['title'], self.format_url(pub['url']))
            for pub in publications]
        self.print(self.format_list(pub_list))
        self.print()

    def print_resume(self, resume):
        self.print_preamble()
        self.print_header(resume)
        self.print_summary(resume['summary'])
        self.print_education(resume['education'])
        self.print_experience(resume['experience'])
        self.print_skills(resume['skills'])
        self.print_publications(resume['publications'])
        self.print_postamble()

    def print_skills(self, skills):
        self.print(self.format_heading('Skills'))
        for skill in skills:
            self.print_skill(skill)
            self.print()

    def print_summary(self, summary):
        self.print(self.format_heading('Summary'))
        self.print(self.format_summary(summary))
        self.print()

class Latex(Outputter):
    def format_date_range(self, start, end):
        return self.format_date(start) + '--' + self.format_date(end)

    def format_email(self, email):
        return r'\href{{mailto:{0}}}{{{0}}}'.format(email)

    def format_heading(self, heading, level=1):
        if level == 1:
            return r'\section*{{{}}}'.format(heading)
        else:
            return r'\textbf{{{}}}'.format(heading)

    def format_list(self, items):
        return ('\\begin{itemize}\n'
            + '\n'.join([textwrap.fill(r'\item ' + item, subsequent_indent='  ',
                                       break_long_words=False,
                                       break_on_hyphens=False)
                         for item in items])
            + '\n\\end{itemize}')

    def format_name(self, name):
        return r'{{\Large\bfseries {}}}'.format(name)

    def format_phone(self, phone):
        return '({}) {}--{}'.format(phone[0:3], phone[3:6], phone[6:10])

    def format_url(self, url):
        return r'\url{{{}}}'.format(url)

    def print_header(self, resume):
        name = self.format_name(resume['name'])
        address = self.format_address(resume['address'])
        phone = self.format_phone(resume['phone'])
        email = self.format_email(resume['email'])
        self.print(r'''\begin{{center}}
  {} \\
  {} \\
  {} \\
  {}
\end{{center}}
'''.format(name, address, phone, email))

    def print_job(self, job):
        self.print('\\entry{{{}}}\n{{{}}}\n{{{}}}\n{{{}}}'.format(
            job['title'],
            self.format_date_range(job['start'], job['end']),
            job['organization'],
            job['location']))
        self.print(self.format_list(map(self.format_all_urls,
                                        job['experiences'])))

    def print_postamble(self):
        self.print('\end{document}')

    def print_preamble(self):
        self.print(r'''\documentclass[10pt]{article}
\input{resume_preamble.tex}
\begin{document}''')

    def print_school(self, school):
        self.print('\\entry{{{}}}\n{{{}}}\n{{{}}}\n{{{}}}'.format(
            school['name'],
            self.format_date(school['graduated']),
            school['degree'],
            'Overall G.P.A.: ' + school['gpa']))
        self.print(self.format_list(map(self.format_all_urls,
                                        school['awards'])))

    def print_skill(self, skill):
        self.print(self.format_heading(skill['name'], 2))
        self.print(self.format_list(map(self.format_all_urls,
                                        skill['notes'])))

class Plaintext(Outputter):
    def format_date_range(self, start, end):
        return self.format_date(start) + ' - ' + self.format_date(end)

    def format_email(self, email):
        return email

    def format_heading(self, heading, level=1):
        if level == 1:
            underline = '='
        else:
            underline = '-'
        return heading + '\n' + underline * len(heading)

    def format_list(self, items):
        return '\n'.join([textwrap.fill('* ' + item, subsequent_indent='  ',
                                        break_long_words=False,
                                        break_on_hyphens=False)
                          for item in items])

    def format_name(self, name):
        return name

    def format_phone(self, phone):
        return '({}){}-{}'.format(phone[0:3], phone[3:6], phone[6:10])

    def format_url(self, url):
        return url

    def print_header(self, resume):
        self.print(self.format_name(resume['name']))
        self.print('Address: ' + self.format_address(resume['address']))
        self.print('Phone: ' + self.format_phone(resume['phone']))
        self.print('Email: ' + self.format_email(resume['email']))
        self.print()

    def print_job(self, job):
        heading = '{} ({})'.format(job['title'],
                self.format_date_range(job['start'], job['end']))
        self.print(self.format_heading(heading, 2))
        self.print('Organization: ' + job['organization'])
        self.print('Location: ' + job['location'])
        self.print(self.format_list(job['experiences']))

    def print_postamble(self): pass

    def print_preamble(self): pass

    def print_school(self, school):
        self.print(self.format_heading(school['name'], 2))
        self.print('Graduated: ' + self.format_date(school['graduated']))
        self.print('Degree: ' + school['degree'])
        self.print('Overall G.P.A.: ' + school['gpa'])
        self.print('Awards and designations:')
        self.print(self.format_list(school['awards']))

    def print_skill(self, skill):
        self.print(self.format_heading(skill['name'], 2))
        self.print(self.format_list(skill['notes']))

parser = argparse.ArgumentParser(description='Generate resume from JSON data.')
parser.add_argument('-o', '--output', default='-', help='set output file')
parser.add_argument('-p', '--plaintext', action='store_true',
    help='output in plaintext format')
parser.add_argument('input', nargs='?', default='resume.json',
    help='JSON data file')
args = parser.parse_args()

with open(args.input, 'r') as resume_file:
    resume = json.load(resume_file)

if args.output == '-':
    output = sys.stdout
else:
    output = open(args.output, 'w')

if args.plaintext:
    outputter = Plaintext(output)
else:
    outputter = Latex(output)

outputter.print_resume(resume)
