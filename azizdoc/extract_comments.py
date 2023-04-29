import sys
from tkinter import Tk, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
import re

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m azizdoc <path_to_python_file>")
    else:
        extract_comments_and_functions(sys.argv[1])

def extract_comments_and_functions(cc):
    with open(cc, 'r') as f:
        code = f.read()
    def create_pdf(code):
        func_pattern = re.compile("def\s+(\w+)\s*\([^)]*\)\s*:")
        cmnt_pattern = re.compile(r"#.*?$|'''(.*?)'''|\"\"\"(.*?)\"\"\"", re.DOTALL | re.MULTILINE)

        functions = {}
        miscellaneous = []

        # Find all function blocks and their associated comments
        for match in func_pattern.finditer(code):
            func_name = match.group(1)
            func_code = code[match.start():]
            next_func_match = func_pattern.search(func_code[1:])
            func_code_end = len(func_code) if next_func_match is None else next_func_match.start() + 1
            func_code = func_code[:func_code_end]
            func_comments = []
            func_indentation = match.start() - code.rfind("\n", 0, match.start()) - 1
            for cmnt_match in cmnt_pattern.finditer(func_code):
                cmnt_indentation = cmnt_match.start() - func_code.rfind("\n", 0, cmnt_match.start()) - 1
                if cmnt_match.group(0).startswith("#") and cmnt_indentation > func_indentation:
                    func_comments.append(cmnt_match.group(0).strip())
                elif cmnt_match.group(0).startswith("'''") and cmnt_indentation > func_indentation:
                    func_comments.append(cmnt_match.group(0).strip())
                elif cmnt_match.group(0).startswith("\"\"\"") and cmnt_indentation > func_indentation:
                    func_comments.append(cmnt_match.group(0).strip())

            functions[func_name] = func_comments

        # Find all miscellaneous comments
        last_func_end = 0
        for match in cmnt_pattern.finditer(code):
            if match.start() < last_func_end:
                continue
            is_miscellaneous = True
            for func_comments in functions.values():
                if match.group(0).strip() in func_comments:
                    is_miscellaneous = False
                    break
            if is_miscellaneous:
                if match.group(0).startswith("#"):
                    miscellaneous.append(match.group(0).strip())
                elif match.group(0).startswith("'''"):
                    miscellaneous.append(match.group(1).strip())

        # Add the miscellaneous comments to the dictionary
        if miscellaneous:
            functions["miscellaneous"] = miscellaneous

        cleaned_dict = {}

        for key, comments in functions.items():
            for comment in comments:
                if comment.startswith("#"):
                    cleaned_comments = [comment.replace("#", "").strip() for comment in comments]

                elif comment.startswith("'''"):
                    cleaned_comments = comment.strip("'''")

                else:
                    cleaned_comments = [comment.replace("\"\"\"", "").strip() for comment in comments]

            cleaned_dict[key] = cleaned_comments





        # Initialize tkinter root window
        root = Tk()
        root.withdraw()

        # Ask user to select directory to save PDF
        file_path = filedialog.asksaveasfilename(defaultextension='.pdf', filetypes=[('PDF Files', '*.pdf')])

        data = cleaned_dict

        doc = SimpleDocTemplate(file_path, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)

        styles = getSampleStyleSheet()
        styleH = styles['Heading1']

        bullet_list = []
        for key, value in data.items():
            if not value:
                value = ['No comments for this function.']

            function_bullet = ListFlowable(
                [
                    Paragraph(f"<bullet>&#8226;</bullet> {key}", styleH),
                    ListFlowable(
                        [
                            ListItem(Paragraph(comment, styles['Normal']), bulletColor='black', value='\u25A0')
                            for comment in value
                        ],
                        bulletType='bullet',
                        bulletFontName='Helvetica',
                        bulletFontSize=10,
                        bulletIndent=20,
                        start='bullet',
                        leftIndent=30
                    )
                ]
            )
            bullet_list.append(function_bullet)
            bullet_list.append(Spacer(1, 0.5 * inch))

        doc.build(bullet_list)
        print("Your pdf has been generated.")


    # Get the filename argument from the command-line
    filename = sys.argv[1]

    # Read the contents of the file into a string
    with open(filename, 'r') as f:
        code1 = f.read()

    # Convert the string to a dictionary of function comments
    create_pdf(code1)



if __name__ == "__main__":
    main()



'''class Person():
    def __int__(self,name):
        self.name = name
        #this is the initialization function
    
    #this is a class function
    
    def nom(self):
        return(self.name)'''







