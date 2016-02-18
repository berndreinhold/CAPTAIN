""" copy of http://www.scipy-lectures.org/advanced/scikit-learn/
Author : Bernd
Date : Dec. 23, 2015
"""
import sys
import shutil

class html_picture_summary():
    def __init__(self, of_name, of_dir="", CSS=[]):
        """
        CSS is a list of style sheets
        """
        self._output_file=of_name
        self._output_dir=of_dir
        self._header = ""
        self._CSS = CSS
        self._body = ""
        self._body_content = ""

    def header(self,title):
        """
        produces the header of an html file. 
        """
        l = []
        l[len(l):] = ["<head><title>%s</title>" % title]
        l[len(l):] = ['<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">']
        for c in self._CSS:
            l[len(l):] = ['<link rel="stylesheet" type="text/css" href="%s">' % c]
            shutil.copy(c, self._output_dir)
        l[len(l):] = ["</head>"]
        self._header = "\n".join(l)

    def body(self, title, comment=""):
        l = []
        l[len(l):] = ["<body>"]
        l[len(l):] = ["<h1>%s</h1>" % title]
        l[len(l):] = [comment]
        l[len(l):] = [self._body_content]
        l[len(l):] = ["</body>"]
        self._body = "\n".join(l)

    def all_html(self):
        """
        produces the actual html code of the whole document. Requires self._header and self._body to be set.
        """
        l = []
        l[len(l):] = ["<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'>"]
        l[len(l):] = ["<html>"]
        l[len(l):] = [self._header]
        l[len(l):] = [self._body]
        l[len(l):] = ["</html>"]
        return "\n".join(l)


    def loop(self, title, comment=""):
        f = open(self._output_dir + self._output_file, 'w')
        self.header(title)
        self.body(title, comment)
        f.write(self.all_html())

        f.close()
        if f.closed: print("wrote to: %s/%s" % (self._output_dir, self._output_file))
        else:
            print("something went wrong with %s" % self._output_file)
            sys.exit(-1)

def main():
    output_file = "mytest.html"
    output_path = "./"
    h = html_picture_summary(output_file, output_path, ["basic_style.css"])
    h.loop("Yippie!")
    

if __name__ == "__main__":
    status = main()
    sys.exit(status)
