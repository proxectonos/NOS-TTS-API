import re
import os
import subprocess
import string
import random


# función que engade a puntuación orixinal á extensión de números de cotovía (opción p)
def punctuate_p(str_ext):

    # substitute ' ·\n' by ...
    str_ext = re.sub(r" ·", r"...", str_ext)
    
    # remove spaces before , . ! ? ; : ) ] of the extended string
    str_ext = re.sub(r"\s+([.,!?;:)\]])", r"\1", str_ext)

    # remove spaces after ( [ ¡ ¿ of the extended string
    str_ext = re.sub(r"([\(\[¡¿])\s+", r"\1", str_ext)

    # remove unwanted spaces between quotations marks
    str_ext = re.sub(r'"\s*([^"]*?)\s*"', r'"\1"', str_ext)

    # substitute '- text -' to '-text-'
    str_ext = re.sub(r"-\s*([^-]*?)\s*-", r"-\1-", str_ext)

    # remove initial question marks
    str_ext = re.sub(r"[¿¡]", r"", str_ext)

    # eliminate extra spaces
    str_ext = re.sub(r"\s+", r" ", str_ext)

    str_ext = re.sub(r"(\d+)\s*-\s*(\d+)", r"\1 \2", str_ext)

    ### - , ' and () by commas
    # substitute '- text -' to ', text,'
    str_ext = re.sub(r"(\w+)\s+-([^-]*?)-\s+([^-]*?)", r"\1, \2, ", str_ext)

    # substitute ' - ' by ', '
    str_ext = re.sub(r"(\w+[!\?]?)\s+-\s*", r"\1, ", str_ext)

    # substitute ' ( text )' to ', text,'
    str_ext = re.sub(r"(\w+)\s*\(\s*([^\(\)]*?)\s*\)", r"\1, \2,", str_ext)

    # add final punctuation mark if it is not present
    # if not re.match(r"[.!?]", str_ext[-1]):
    #     str_ext = str_ext + "."

    return str_ext


def to_cotovia(text):
    print("Text segments: ", text)
    ## Initial text preprocessing
    # substitute ' M€' by 'millóns de euros' and 'somewordM€' by 'someword millóns de euros'
    text = re.sub(r"(\w+)\s*M€", r"\1 millóns de euros", text)

    # substitute ' €' by 'euros' and 'someword€' by 'someword euros'
    text = re.sub(r"(\w+)\s*€", r"\1 euros", text)
    
    # substitute ' ºC' by 'graos centígrados' and 'somewordºC' by 'someword graos centígrados'
    text = re.sub(r"(\w+)\s*ºC", r"\1 graos centígrados", text)

    # Random string generation
    res = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))

    text = subprocess.run(["sed", "-e", "s/₂//g", "-e", "s/⸺//g", "-e", "s/ //g", "-e", "s///g", "-e", "s/č/c/g", "-e", "s/ț/t/g", "-e", "s/ğ/g/g", "-e", "s/ș/s/g",
                "-e", "s/ş/s/g", "-e", "s/Ž/Z/g", "-e", "s/ž/z/g", "-e", "s/ț/t/g", "-e", "s/ğ/g/g", "-e", "s/ș/s/g", "-e", "s/ş/s/g", "-e", "s/«//g", "-e", "s/»//g",
                "-e", "s/<<//g", "-e", "s/>>//g", "-e", "s/“/\"/g", "-e", "s/”/'\"'/g", "-e", "s/\'//g", "-e", "s/‘//g", "-e", "s/’//g", "-e", "s/…//g",
                "-e", "s/-/-/g", "-e", "s/–/-/g", "-e", "s/—/-/g", "-e", "s/―/-/g", "-e", "s/−/-/g", "-e", "s/‒/-/g", "-e", "s/─/-/g"],
                input = text, text = True, capture_output=True).stdout

    print("Preprocessed text: ", text)

    # Input and output Cotovía files
    COTOVIA_IN_TXT_PATH = res + '.txt'
    COTOVIA_IN_TXT_PATH_ISO = 'iso8859-1' + res + '.txt'
    COTOVIA_OUT_PRE_PATH = 'iso8859-1' + res + '.pre'
    COTOVIA_OUT_PRE_PATH_UTF8 = 'utf8' + res + '.pre'

    with open(COTOVIA_IN_TXT_PATH, 'w') as f:
        # for seg in text:
        #     if seg:
        #         f.write(seg + '\n')
        #     else:
        #         f.write(',' + '\n')
        f.write(text + '\n')

    # especial characters
    # subprocess.run(["sed", "-i", "-e", "s/₂//g", "-e", "s/⸺//g", "-e", "s/ //g", "-e", "s///g", "-e", "s/č/c/g", "-e", "s/ț/t/g", "-e", "s/ğ/g/g", "-e", "s/ș/s/g",
    #             "-e", "s/ş/s/g", "-e", "s/Ž/Z/g", "-e", "s/ž/z/g", "-e", "s/ț/t/g", "-e", "s/ğ/g/g", "-e", "s/ș/s/g", "-e", "s/ş/s/g", "-e", "s/«//g", "-e", "s/»//g",
    #             "-e", "s/<<//g", "-e", "s/>>//g", "-e", "s/“/\"/g", "-e", "s/”/\"/g", "-e", "s/\"//g", "-e", "s/\'//g", "-e", "s/‘//g", "-e", "s/’//g", "-e", "s/…//g",
    #             "-e", "s/-/-/g", "-e", "s/–/-/g", "-e", "s/—/-/g", "-e", "s/―/-/g", "-e", "s/−/-/g", "-e", "s/‒/-/g", "-e", "s/─/-/g",
    #             COTOVIA_IN_TXT_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    

    # utf-8 to iso8859-1
    subprocess.run(["iconv", "-f", "utf-8", "-t", "iso8859-1", COTOVIA_IN_TXT_PATH, "-o", COTOVIA_IN_TXT_PATH_ISO], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    print("Preprocessing text with Cotovía...")
    #subprocess.run(["cotovia", "-n", "-p", "-S", ">", COTOVIA_IN_TXT_PATH_ISO,], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    with open(COTOVIA_OUT_PRE_PATH, 'w') as out_f, open(COTOVIA_IN_TXT_PATH_ISO, 'r') as in_f:
        subprocess.run(["cotovia", "-n", "-p", "-S"], stdin=in_f, stdout=out_f, stderr=subprocess.STDOUT)
    #print(COTOVIA_IN_TXT_PATH_ISO)
    subprocess.run(["iconv", "-f", "iso8859-1", "-t", "utf-8", COTOVIA_OUT_PRE_PATH, "-o", COTOVIA_OUT_PRE_PATH_UTF8], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    # print COTOVIA_OUT_PRE_PATH_UTF8 content with open
    with open(COTOVIA_OUT_PRE_PATH_UTF8, 'r') as f:
        print("COTOVIA_OUT_PRE_PATH_UTF8 content after sed: ")
        print(f.read())
    
 

    segs = []
    try:
        with open(COTOVIA_OUT_PRE_PATH_UTF8, 'r') as f:
            segs = [line.rstrip() for line in f]
            # segs = [remove_tra3_tags(line) for line in segs] # modificar con punctuate_p
            segs = [punctuate_p(line) for line in segs] # modificar con punctuate_p
            print(segs)
    except:
        print("ERROR: Couldn't read cotovia output")

    subprocess.run(["rm", COTOVIA_IN_TXT_PATH, COTOVIA_IN_TXT_PATH_ISO, COTOVIA_OUT_PRE_PATH, COTOVIA_OUT_PRE_PATH_UTF8], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    print("Text segments: ", segs)
    return segs

def text_preprocess(text):

    cotovia_preproc_text = to_cotovia(text)

    # convert list to string
    cotovia_preproc_text_res = ' '.join(cotovia_preproc_text)
    
    # print("cotovia_preproc_text: ", cotovia_preproc_text)

    # remove extra spaces
    cotovia_preproc_text_res = re.sub(r"\s+", r" ", cotovia_preproc_text_res)

    # add final punctuation mark if it is not present
    if not re.match(r"[.!?]", cotovia_preproc_text_res[-1]):
        cotovia_preproc_text_res = cotovia_preproc_text_res + "."

    return cotovia_preproc_text_res
