#!/usr/bin/env python3
# This is a simple script to generate different versions (current TeX and
# plaintext) of my resume from the 'resume.json' data file.

# TODO:
# - Handle escaping special characters in LaTeX output (such as & and #).

import argparse
import json
import re
import sys
import textwrap

# TODO: make this regex work for more general URLs (cover more cases).
url_regex = re.compile(r'https?://[A-Za-z0-9_/.-]*[A-Za-z0-9_/-]')

# An (abstract) base class for an outputter, which converts resume JSON data
# into an output format (LaTeX, plaintext, HTML, etc.).  Most methods are
# explicitly not implemented, and are only included in this class as
# pseudo-abstract members so that they can be documented.
#
# The methods that are implemented are those whose implementations should not
# vary between output formats, except perhaps in some very exceptional cases.
# Even methods whose implementations are the same in every (current) derived
# class may not have their definitions in this class if it is conceivable that
# another output format would require a new definition.
class Outputter:
    def __init__(self, output=sys.stdout):
        self.output = output

    # Format all URLs in the input string, returning the formatted string.
    def format_all_urls(self, text):
        new_text = ''
        match = url_regex.search(text)
        while match is not None:
            new_text += text[:match.start()] + self.format_url(match.group(0))
            text = text[match.end():]
            match = url_regex.search(text)
        new_text += text
        return new_text

    # Format the given date range.
    def format_date_range(self, start, end):
        raise NotImplementedError()

    # Format the given email address, adding a hyperlink if available.
    def format_email(self, email):
        raise NotImplementedError()

    # Format a heading (e.g. the title of a section or subsection).
    def format_heading(self, heading, level=1):
        raise NotImplementedError()

    # Format a list of items.  No special formatting will be done on the text
    # contained in each item except (possibly) to word-wrap it to a suitable
    # column width.
    def format_list(self, items):
        raise NotImplementedError()

    # Format a phone number, inserting parentheses and dashes where
    # appropriate.
    def format_phone(self, phone):
        raise NotImplementedError()

    def format_url(self, url):
        raise NotImplementedError()

    # Write the given string to the output used by this Outputter, followed by
    # a newline.
    def print(self, text=''):
        self.output.write(text + '\n')

    # Output the education section from the given list of entries.
    def print_education(self, education):
        self.print(self.format_heading('Education'))
        for school in education:
            self.print_school(school)
            self.print()

    # Output the experience section from the given list of entries.
    def print_experience(self, experience):
        self.print(self.format_heading('Experience'))
        for job in experience:
            self.print_job(job)
            self.print()

    # Output the resume header (the letterhead) from the given resume data.
    def print_header(self, resume):
        raise NotImplementedError()

    # Output a single job (entry in the experience section) from the given
    # description.
    def print_job(self, job):
        raise NotImplementedError()

    # Output any text that needs to come at the very end of the document (e.g.
    # '\end{document}' for LaTeX).  Since this is not always necessary,
    # subclasses need not provide an implementation.
    def print_postamble(self): pass

    # Output any text that needs to come at the very beginning of the document
    # (e.g. '\begin{document}' for LaTeX).  Since this is not always necessary,
    # subclasses need not provide an implementation.
    def print_preamble(self): pass

    # Output a single school (entry in the education section) from the given
    # data.
    def print_school(self, school):
        raise NotImplementedError()

    # Output a single skill from the given data.  A default implementation is
    # provided which should work for all sensible output formats.
    def print_skill(self, skill):
        self.print(self.format_heading(skill['name'], 2))
        self.print(self.format_list(map(self.format_all_urls,
                                        skill['notes'])))

    # Output the publications section from the given list of entries.
    def print_publications(self, publications):
        self.print(self.format_heading('Publications and presentations'))
        pub_list = ['{} ({})'.format(pub['title'], self.format_url(pub['url']))
                    for pub in publications]
        self.print(self.format_list(pub_list))
        self.print()

    # Output the entire resume from the given data.
    def print_resume(self, resume):
        self.print_preamble()
        self.print_header(resume)
        self.print_summary(resume['summary'])
        self.print_education(resume['education'])
        self.print_experience(resume['experience'])
        self.print_skills(resume['skills'])
        self.print_publications(resume['publications'])
        self.print_postamble()

    # Output the skills section from the given list of entries.
    def print_skills(self, skills):
        self.print(self.format_heading('Skills'))
        for skill in skills:
            self.print_skill(skill)
            self.print()

    # Output the summary section from the given list of entries.
    def print_summary(self, summary):
        self.print(self.format_heading('Summary'))
        self.print(self.format_summary(summary))
        self.print()

# An outputter which produces a LaTeX document.  Styles and the definitions of
# macros can be found in the 'resume_prelude.tex' file in order to keep this
# code concise and maintainable.  Comments explaining the purpose of each
# method can be found on the corresponding methods in the 'Outputter' base
# class.
class Latex(Outputter):
    def format_date_range(self, start, end):
        return start + '--' + end

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

    def format_summary(self, summary):
        return textwrap.fill(self.format_all_urls(summary), width=80)

    def format_url(self, url):
        return r'\url{{{}}}'.format(url)

    def print_header(self, resume):
        name = resume['name']
        address = resume['address']
        phone = self.format_phone(resume['phone'])
        email = self.format_email(resume['email'])
        self.print(r'''\begin{{center}}
  {{\Large\bfseries {}}} \\
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
            school['graduated'],
            school['degree'],
            'Overall G.P.A.: ' + school['gpa']))
        self.print(self.format_list(map(self.format_all_urls,
                                        school['awards'])))

# An outputter which produces a plaintext document.  Comments explaining the
# purpose of each method can be found on the corresponding methods in the
# 'Outputter' base class.
class Plaintext(Outputter):
    def format_date_range(self, start, end):
        return start + ' - ' + end

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

    def format_phone(self, phone):
        return '({}){}-{}'.format(phone[0:3], phone[3:6], phone[6:10])

    def format_summary(self, summary):
        return textwrap.fill(self.format_all_urls(summary), width=80)

    def format_url(self, url):
        return url

    def print_header(self, resume):
        self.print(resume['name'])
        self.print('Address: ' + resume['address'])
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
        self.print('Graduated: ' + school['graduated'])
        self.print('Degree: ' + school['degree'])
        self.print('Overall G.P.A.: ' + school['gpa'])
        self.print('Awards and designations:')
        self.print(self.format_list(school['awards']))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate resume from JSON data.')
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
