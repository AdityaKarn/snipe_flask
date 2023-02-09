

'''

Chops each page in half, e.g. if a source were
created in booklet form, you could extract individual
pages, and re-combines it
'''
from PyPDF2 import PdfFileWriter,PdfFileReader, PdfFileMerger
#split left

def script():
    with open("abc.pdf", "rb") as in_f:
        input1 = PdfFileReader(in_f)
        output = PdfFileWriter()

        numPages = input1.getNumPages()

        for i in range(numPages):
            page = input1.getPage(i)
            page.mediabox.upper_right =(
                page.mediabox.right / 2,
                page.mediabox.top,
            )
            # page.cropBox.upperRight = (305, 700)
            output.addPage(page)

        with open("left.pdf", "wb") as out_f:
            output.write(out_f)

    # #split right
    with open("abc.pdf", "rb") as in_f:
        input1 = PdfFileReader(in_f)
        output = PdfFileWriter()

        numPages = input1.getNumPages()


        for i in range(numPages):
            page = input1.getPage(i)
            page.mediabox.upper_left =(
                page.mediabox.right / 2,
                page.mediabox.top,
            )
            output.addPage(page)

        with open("right.pdf", "wb") as out_f:
            output.write(out_f)

    #combine splitted files
    input1 = PdfFileReader(open("left.pdf","rb"))
    input2 = PdfFileReader(open("right.pdf","rb"))
    output = PdfFileWriter()
    numPages = input1.getNumPages()

    for i in range(numPages):
        l = input1.getPage(i)
        output.addPage(l)
        r = input2.getPage(i)
        output.addPage(r)

    with open("out.pdf", "wb") as out_f:
        output.write(out_f)