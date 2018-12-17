import re
import argparse
from TexSoup import TexSoup
#Process user-defined \newtheorem aliases
#Convert them into a 
def newtheorem_proc_replace(data):
    soup = TexSoup(data)
    nt_dic = {}
    newtheorems = soup.find_all('newtheorem')
    for newtheorem in newtheorems:
        val1, val2, val3 = newtheorem.args
        val1 = val1[0:]
        val2 = val2[0:]
        val3 = val3[0:]
        original = (str(newtheorem))[11:]
        print(original)
        nt_type = (str(newtheorem))[-1]
        if nt_type == ']': #Type 1 aka theorems
            nt_dic[val1] = val2
            #original = '{' + val1 + '}{' + val2 + '}[' + val3 + ']'
            expanded = '{' + val2 + '}{' + val2 + '}[' + val3 + ']'
            print(expanded)
            data = data.replace(original, expanded)
        elif nt_type == '}': #Type 2 aka lemmas
            nt_dic[val1] = val3           
            if val2 in nt_dic: #teo
                expanded = '{' + val3 + '}[' + nt_dic[val2] + ']{' + val3 + '}'
                print(expanded)
            else:
                expanded = '{' + val3 + '}[' + val2 + ']{' + val3 + '}'
                print(expanded)
            data = data.replace(original, expanded)
        else:
            print("Error: The term is {}".format(newtheorem))
    print("\\newtheorem dictionary: {}".format(nt_dic))
    return nt_dic, data
def replace_all(paper, red):
    for key in red:
        bm = '\\begin{' + key + '}'
        em = '\\end{' + key + '}'
        bsm = '\\begin*{' + key + '}'
        esm = '\\end*{' + key + '}'
        bmn = '\\begin{' + red[key] + '}'
        emn = '\\end{' + red[key] + '}'
        bsmn = '\\begin*{' + red[key] + '}'
        esmn = '\\end*{' + red[key] + '}'
        #print(bm)
        #print(em)
        #print(bmn)
        #print(emn)
        paper = paper.replace(bm, bmn)
        paper = paper.replace(em, emn)
        paper = paper.replace(bsm, bsmn)
        paper = paper.replace(esm, esmn)
    return paper
def process(data):
    red, data = newtheorem_proc_replace(data)
    processed = replace_all(data, red)
    return processed
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Standardize all \newtheorem in a .tex file.')
    parser.add_argument('file', metavar='file', type=str, help='An .tex file to process')
    args = parser.parse_args()
    file = vars(args)['file']
    with open(file) as f:
        data = f.read()
    data = process(data)
    if len(file) > 3 and file[-4:] == '.tex': #extension exists
        output_file = file[:-4] + '_clean.tex'
    else: #no extension
        output_file = file + '_clean'
    with open(output_file, 'w') as g:
        g.write(data)


