#!/usr/bin/env python3
# This is a simple script to generate different versions (current TeX and
# plaintext) of my resume from the 'resume.json' data file.

import json

class OutputModule:
    def format_address(self, address):
        return address

    def format_date(self, date):
        return date

    def format_summary(self, summary):
        import textwrap
        return textwrap.fill(summary, width=80)

    def print_education(self, education):
        print(self.format_heading('Education'))
        for school in education:
            self.print_school(school)
            print()

    def print_experience(self, experience):
        print(self.format_heading('Experience'))
        for job in experience:
            self.print_job(job)
            print()

    def print_publications(self, publications):
        print(self.format_heading('Publications and presentations'))
        pub_list = ['{} ({})'.format(pub['title'], self.format_url(pub['url']))
                for pub in publications]
        print(self.format_list(pub_list))
        print()

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
        print(self.format_heading('Skills'))
        for skill in skills:
            self.print_skill(skill)
            print()

    def print_summary(self, summary):
        print(self.format_heading('Summary'))
        print(self.format_summary(summary))
        print()

class Latex(OutputModule):
    def format_date_range(self, start, end):
        return self.format_date(start) + '--' + self.format_date(end)

    def format_email(self, email):
        return r'\href{{mailto:{0}}}{{{0}}}'.format(email)

    def format_name(self, name):
        return r'{{\Large\bfseries {}}}'.format(name)

    def format_phone(self, phone):
        return '({}) {}--{}'.format(phone[0:3], phone[3:6], phone[6:10])

class Plaintext(OutputModule):
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
        return '\n'.join(['* ' + item for item in items])

    def format_name(self, name):
        return name

    def format_phone(self, phone):
        return '({}){}-{}'.format(phone[0:3], phone[3:6], phone[6:10])

    def format_url(self, url):
        return url

    def print_header(self, resume):
        print(self.format_name(resume['name']))
        print('Address: ' + self.format_address(resume['address']))
        print('Phone: ' + self.format_phone(resume['phone']))
        print('Email: ' + self.format_email(resume['email']))
        print()

    def print_job(self, job):
        heading = '{} ({})'.format(job['title'],
                self.format_date_range(job['start'], job['end']))
        print(self.format_heading(heading, 2))
        print('Organization: ' + job['organization'])
        print('Location: ' + job['location'])
        print(self.format_list(job['experiences']))

    def print_school(self, school):
        print(self.format_heading(school['name'], 2))
        print('Graduated: ' + self.format_date(school['graduated']))
        print('Overall G.P.A.: ' + school['gpa'])
        print('Awards and designations:')
        print(self.format_list(school['awards']))

    def print_skill(self, skill):
        print(self.format_heading(skill['name'], 2))
        print(self.format_list(skill['notes']))

    def print_postamble(self): pass

    def print_preamble(self): pass

with open('resume.json') as resume_file:
    resume = json.load(resume_file)
    Plaintext().print_resume(resume)
