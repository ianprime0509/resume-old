# My resume

Preliminary note: if you are interested in seeing my resume in PDF format,
please see [the GitHub releases page for this
project](https://github.com/ianprime0509/resume/releases) and look at the most
recent release.  I had to remove PDF files from the repository itself because
they were causing too many merge conflicts, and anyways it's not really good
practice to include generated files in Git repositories (usually).

This is the working repository for my resume.  The main branch should contain
*all* notable experience, skills, etc. with other (local) branches being used
to trim things down to a single page by removing details not needed for
particular applications.

For a general, one-page resume, see the 'one-page' branch.  This branch should
always contain an up-to-date copy of the resume that fits within a single page
and is applicable to most jobs.

The resume is generated from a JSON file (`resume.json`), resulting in a PDF
and a plaintext version.  This makes it easier to maintain both versions
simultaneously (otherwise they will most certainly get out of sync) and leaves
the door open to using the JSON file in other projects as well (like a
portfolio site).

## References document

The generator script can generate a document containing references (by default
described in `references.json`) using the `-r, --references` flag.  For privacy
reasons, no files containing reference information will ever be committed to
this repository.  However, the following is an example of what
`references.json` looks like:

```json
{
  "metadata": {
    "title": "Ian Johnson's references",
    "subject": "Ian Johnson's references"
  },
  "name": "Ian Johnson",
  "address": "2925 Rensselaer Court, Vienna, VA 22181",
  "phone": "7038198495",
  "email": "IanTimothyJohnson@gmail.com",
  "references": [{
    "name": "Example",
    "relationship": "Example",
    "email": "example@example.com",
    "phone": "5555555555"
  }]
}
```
