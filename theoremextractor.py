import re
import argparse
from TexSoup import TexSoup
#Process user-defined \newtheorem aliases
#Convert them into a 
def newtheorem_proc(soup):
    nt_dic = {}
    newtheorems = soup.find_all('newtheorem')
    for newtheorem in newtheorems:
        val1, val2, val3 = newtheorem.args
        val1 = val1[0:]
        val2 = val2[0:]
        val3 = val3[0:]
        nt_type = (str(newtheorem))[-1]
        if nt_type == ']': #Type 1 aka theorems
            nt_dic[val1] = val2
        elif nt_type == '}': #Type 2 aka lemmas
            nt_dic[val1] = val3
        else:
            print("Error: The term is {}".format(newtheorem))
    print("\\newtheorem dictionary: {}".format(nt_dic))
    return nt_dic
def find_all(paper, mac):
    bm = '\\\\begin{' + mac + '}'
    em = '\\\\end{' + mac + '}'
    bsm = '\\\\begin*{' + mac + '}'
    esm = '\\\\end*{' + mac + '}'
    pattern = re.compile('(' + bm + '.+?' + em + ')|(' + bsm + '.+?' + esm + ')', re.DOTALL)
    res_list = re.findall(pattern, paper)
    final_list = []
    for res in res_list:
        final_list.append(res[0])
    return final_list
def collect_dict(data, red):
    ret = []
    for key in red:
        ret.append(f'Here are all the {red[key]}s:')
        ret.extend(find_all(data, key))
    return ret
def process(data):
    soup = TexSoup(data)
    red = newtheorem_proc(soup)
    ret = collect_dict(data, red)
    output = '\n\n'.join(ret)
    return output
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract all theorems from a paper in .tex.')
    parser.add_argument('-o', metavar='file', type=str, help='Output file', nargs = '?', default = 'te_output.txt')
    parser.add_argument('paper', metavar='file', type=str, help='A paper to process')
    args = parser.parse_args()
    paper = vars(args)['paper']
    output = vars(args)['o']
    with open(paper) as f:
        data = f.read()
    res = process(data)
    with open(output, 'w') as g:
        g.write(res)



