# Makefile for Python documentation
# ---------------------------------
#
# See also the README file.
#
# This is a bit of a mess.  The documents are identified by short names:
#   api -- Python/C API Reference Manual
#   doc -- Documenting Python
#   ext -- Extending and Embedding the Python Interpreter
#   lib -- Library Reference Manual
#   mac -- Macintosh Library Modules
#   ref -- Python Reference Manual
#   tut -- Python Tutorial
#   inst -- Installing Python Modules
#   dist -- Distributing Python Modules
#
# The LaTeX sources for each of these documents are in subdirectories
# with the three-letter designations above as the directory names.
#
# The main target creates HTML for each of the documents.  You can
# also do "make lib" (etc.) to create the HTML versions of individual
# documents.
#
# The document classes and styles are in the texinputs/ directory.
# These define a number of macros that are similar in name and intent
# as macros in Texinfo (e.g. \code{...} and \emph{...}), as well as a
# number of environments for formatting function and data definitions.
# Documentation for the macros is included in "Documenting Python"; see
# http://www.python.org/doc/current/doc/doc.html, or the sources for
# this document in the doc/ directory.
#
# Everything is processed by LaTeX.  See the file `README' for more
# information on the tools needed for processing.
#
# There's a problem with generating the index which has been solved by
# a sed command applied to the index file.  The shell script fix_hack
# does this (the Makefile takes care of calling it).
#
# Additional targets attempt to convert selected LaTeX sources to
# various other formats.  These are generally site specific because
# the tools used are all but universal.  These targets are:
#
#   ps  -- convert all documents from LaTeX to PostScript
#   pdf -- convert all documents from LaTeX to the
#		Portable Document Format
#
# See the README file for more information on these targets.
#
# The formatted output is located in subdirectories.  For PDF and
# PostScript, look in the paper-$(PAPER)/ directory.  For HTML, look in
# the html/ directory.  If you want to fix the GNU info process, look
# in the info/ directory; please send patches to docs@python.org.

# This Makefile only includes information on how to perform builds; for
# dependency information, see Makefile.deps.

# Customization -- you *may* have to edit this

# You could set this to a4:
PAPER=letter

# Ideally, you shouldn't need to edit beyond this point

INFODIR=	info
TOOLSDIR=	tools

# This is the *documentation* release, and is used to construct the
# file names of the downloadable tarballs.  It is initialized by the
# getversioninfo script to ensure that the right version number is
# used; the script will also write commontex/patchlevel.tex if that
# doesn't exist or needs to be changed.  Documents which depend on the
# version number should use \input{patchlevel} and include
# commontex/patchlevel.tex in their dependencies.
RELEASE=$(shell $(PYTHON) tools/getversioninfo)

PYTHON=	   python
DVIPS=	   dvips -N0 -t $(PAPER)

# This is ugly!  The issue here is that there are two different levels
# in the directory tree at which we execute mkhowto, so we can't
# define it just once using a relative path (at least not with the
# current implementation and Makefile structure).  We use the GNUish
# $(shell) function here to work around that restriction by
# identifying mkhowto and the commontex/ directory using absolute paths.
#
# If your doc build fails immediately, you may need to switch to GNU make.
# (e.g. OpenBSD needs package gmake installed; use gmake instead of make)
PWD=$(shell pwd)

# (The trailing colon in the value is needed; TeX places it's default
# set of paths at the location of the empty string in the path list.)
TEXINPUTS=$(PWD)/commontex:

# The mkhowto script can be run from the checkout using the first
# version of this variable definition, or from a preferred version
# using the second version.  The standard documentation is typically
# built using the second flavor, where the preferred version is from
# the Python CVS trunk.
MKHOWTO=   TEXINPUTS=$(TEXINPUTS) $(PYTHON) $(PWD)/tools/mkhowto

MKDVI=	   $(MKHOWTO) --paper=$(PAPER) --dvi
MKHTML=	   $(MKHOWTO) --html --about html/stdabout.dat \
		--iconserver ../icons --favicon ../icons/pyfav.png \
		--address $(PYTHONDOCS) --up-link ../index.html \
		--up-title "Python Documentation Index" \
		--global-module-index "../modindex.html" --dvips-safe
MKISILOHTML=$(MKHOWTO) --html --about html/stdabout.dat \
		--iconserver ../icons \
		--l2h-init perl/isilo.perl --numeric --split 1 \
		--dvips-safe
MKISILO=   iSilo386 -U -y -rCR -d0
MKPDF=	   $(MKHOWTO) --paper=$(PAPER) --pdf
MKPS=	   $(MKHOWTO) --paper=$(PAPER) --ps

BUILDINDEX=$(TOOLSDIR)/buildindex.py

PYTHONDOCS="See <i><a href=\"about.html\">About this document...</a></i> for information on suggesting changes."
HTMLBASE=  file:`pwd`

# The emacs binary used to build the info docs. GNU Emacs 21 is required.
EMACS=     emacs

# The end of this should reflect the major/minor version numbers of
# the release:
WHATSNEW=whatsnew24

references-pdf:	
		$(MKPDF) Reference/Reference.tex
		
references-html:
		$(MKHTML) Reference/Reference.tex

