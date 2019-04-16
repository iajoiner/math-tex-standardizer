#Version 2.0
import re
import argparse
#from TexSoup import TexSoup
#Process user-defined \newtheorem aliases
#Convert them into a 
def newtheorem_proc_replace(data):
    #soup = TexSoup(data)
    #Obtain data
    basic_pattern = r'[ \t]*\\newtheorem[ \t]*{[^\[\]{}]+}[ \t]*{[^\[\]{}]+}[ \t]*'
    numberless_pattern = r'[ \t]*\\newtheorem[ \t]*\*[ \t]*{[^\[\]{}]+}[ \t]*{[^\[\]{}]+}[ \t]*'
    first_counter_pattern = r'[ \t]*\\newtheorem[ \t]*{[^\[\]{}]+}[ \t]*{[^\[\]{}]+}[ \t]*\[[^\[\]{}]+\][ \t]*'
    shared_counter_pattern = r'[ \t]*\\newtheorem[ \t]*{[^\[\]{}]+}[ \t]*\[[^\[\]{}]+\][ \t]*{[^\[\]{}]+}[ \t]*'
    nt_dic = {}#Keys are shortcuts and values are printed stuff
    #nt_counter_dic = {}#Keys are shortcuts of the theorem and values are shortcuts of the parent counter
    nt_b = re.findall(basic_pattern, data)
    nt_n = re.findall(numberless_pattern, data)
    nt_fc = re.findall(first_counter_pattern, data)
    nt_sc = re.findall(shared_counter_pattern, data)
    b_dic = {}
    n_dic = {}
    fc_dic = {}
    sc_dic = {}
    #print(nt_b)
    #print(nt_n)
    #print(nt_fc)
    #print(nt_sc)
    for pat in nt_b:
        lis = re.split('{|}',pat)
        if len(lis) != 5:
            print(f'{lis} is weird!')
        nt_dic[lis[1]] = lis[3]
        b_dic[lis[1]] = (lis[3], pat)
        #print(lis)
    for pat in nt_n:
        lis = re.split('{|}',pat)
        if len(lis) != 5:
            print(f'{lis} is weird!')
        nt_dic[lis[1]] = lis[3]
        n_dic[lis[1]] = (lis[3], pat)
        #print(lis)
    for pat in nt_fc:
        lis = re.split('{|}|\[|\]',pat)
        if len(lis) != 7:
            print(f'{lis} is weird!')
        nt_dic[lis[1]] = lis[3]
        #nt_counter_dic[lis[1]] = lis[5]
        fc_dic[lis[1]] = (lis[3], lis[5], pat)
        #print(lis)
    for pat in nt_sc:
        lis = re.split('{|}|\[|\]',pat)
        if len(lis) != 7:
            print(f'{lis} is weird!')
        nt_dic[lis[1]] = lis[5]
        #nt_counter_dic[lis[1]] = lis[3]
        sc_dic[lis[1]] = (lis[5], lis[3], pat)
        #print(lis)
    print(nt_dic)
##    #print(nt_counter_dic)
    print(b_dic)
    print(n_dic)
    print(fc_dic)
    print(sc_dic)
    #Replacement in the heading
    for key in b_dic:
        if key in fc_dic:
            counter_key = fc_dic[key][1]
            new_key = fc_dic[key][0]
            if counter_key in nt_dic:
                counter_key = nt_dic[counter_key]
            new = '\\newtheorem{' + new_key + '}{' + new_key + '}[' + counter_key + ']'
            #print(f'The old one is {fc_dic[key][2]}')
            #print(f'The new one is {new}')
            data = data.replace(fc_dic[key][2], new)
        else:
            new_key = b_dic[key][0]
            new = '\\newtheorem{' + new_key + '}{' + new_key + '}'
            #print(f'The old one is {b_dic[key][1]}')
            #print(f'The new one is {new}')
            data = data.replace(b_dic[key][1], new)
    for key in n_dic:
        new_key = n_dic[key][0]
        new = '\\newtheorem*{' + new_key + '}{' + new_key + '}'
        #print(f'The old one is {n_dic[key][1]}')
        #print(f'The new one is {new}')
        data = data.replace(n_dic[key][1], new)
    for key in sc_dic:
        #print(f'Meow {key}!')
        counter_key = sc_dic[key][1]
        new_key = sc_dic[key][0]
        if counter_key in nt_dic:
            counter_key = nt_dic[counter_key]
        new = '\\newtheorem{' + new_key + '}[' + counter_key + ']{' + new_key + '}'
        #print(f'The old one is {sc_dic[key][2]}')
        #print(f'The new one is {new}')
        data = data.replace(sc_dic[key][2], new)
    #Replacement in the body of the paper
    for key in nt_dic:
        bm = re.compile(r'[ \t]*\\begin[ \t]*{' + key + '}[ \t]*')
        em = re.compile(r'[ \t]*\\end[ \t]*{' + key + '}[ \t]*')
        bsm = re.compile(r'[ \t]*\\begin*[ \t]*{' + key + '}[ \t]*')
        esm = re.compile(r'[ \t]*\\end*[ \t]*{' + key + '}[ \t]*')
        bmn = r'\\begin{' + nt_dic[key] + '}'
        emn = r'\\end{' + nt_dic[key] + '}'
        bsmn = r'\\begin*{' + nt_dic[key] + '}'
        esmn = r'\\end*{' + nt_dic[key] + '}'
        #print(bm)
        #print(em)
        #print(bmn)
        #print(emn)
        data = re.sub(bm, bmn, data)
        data = re.sub(em, emn, data)
        data = re.sub(bsm, bsmn, data)
        data = re.sub(esm, esmn, data)
    return data
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Standardize all \newtheorem in a .tex file.')
    parser.add_argument('file', metavar='file', type=str, help='An .tex file to process')
    args = parser.parse_args()
    file = vars(args)['file']
    with open(file) as f:
        data = f.read()
    data = newtheorem_proc_replace(data)
    if len(file) > 3 and file[-4:] == '.tex': #extension exists
        output_file = file[:-4] + '_clean.tex'
    else: #no extension
        output_file = file + '_clean'
    with open(output_file, 'w') as g:
        g.write(data)


