# create_tempfile_test.py

from create_tempfile import create_tempfile

f = create_tempfile()
f.write("hello\n")

raise RuntimeError("boom")

