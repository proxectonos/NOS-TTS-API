# preprocesado para a transcrición fonética con cotovía
# realiza a transcrición fonética e devolve a puntuación orixinal

import re
import os
import subprocess
import random
import string


PUNCLIST = [';', '?', '¿', ',', ':', '.', '!', '¡']


def canBeNumber(n):
    try:
        int(n)
        return True
    except ValueError:
        # Not a number
        return False

def accent_convert(phontrans):
    transcript = re.sub('a\^','á',phontrans)
    transcript = re.sub('e\^','é',transcript)
    transcript = re.sub('i\^','í',transcript)
    transcript = re.sub('o\^','ó',transcript)
    transcript = re.sub('u\^','ú',transcript)
    transcript = re.sub('E\^','É',transcript)
    transcript = re.sub('O\^','Ó',transcript)
    return transcript

def remove_tra3_tags(phontrans):
    s = re.sub(r'#(.+?)#', r'', phontrans)
    s = re.sub(r'%(.+?)%', r'', s)
    s = re.sub(' +',' ',s)
    s = re.sub('-','',s)
    return s.strip()

def to_cotovia(text_segments):
    # Input and output Cotovía files
    res = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    COTOVIA_IN_TXT_PATH = res + '.txt'
    COTOVIA_IN_TXT_PATH_ISO = 'iso8859-1' + res + '.txt'
    COTOVIA_OUT_PRE_PATH = 'iso8859-1' + res + '.tra'
    COTOVIA_OUT_PRE_PATH_UTF8 = 'utf8' + res + '.tra'


    print("Text segments: ", text_segments)
    ## Initial text preprocessing
    # substitute ' M€' by 'millóns de euros' and 'somewordM€' by 'someword millóns de euros'
    text_segments = [re.sub(r"(\w+)\s*M€", r"\1 millóns de euros", seg) for seg in text_segments]

    # substitute ' €' by 'euros' and 'someword€' by 'someword euros'
    text_segments = [re.sub(r"(\w+)\s*€", r"\1 euros", seg) for seg in text_segments]

    # substitute ' ºC' by 'graos centígrados' and 'somewordºC' by 'someword graos centígrados'
    text_segments = [re.sub(r"(\w+)\s*ºC", r"\1 graos centígrados", seg) for seg in text_segments]


    text_segments = [subprocess.run(["sed", "-e", "s/₂//g", "-e", "s/⸺//g", "-e", "s/ //g", "-e", "s///g", "-e", "s/č/c/g", "-e", "s/ț/t/g", "-e", "s/ğ/g/g", "-e", "s/ș/s/g",
                "-e", "s/ş/s/g", "-e", "s/Ž/Z/g", "-e", "s/ž/z/g", "-e", "s/ț/t/g", "-e", "s/ğ/g/g", "-e", "s/ș/s/g", "-e", "s/ş/s/g", "-e", "s/«//g", "-e", "s/»//g",
                "-e", "s/<<//g", "-e", "s/>>//g", "-e", "s/“/\"/g", "-e", "s/”/'\"'/g", "-e", "s/\'//g", "-e", "s/‘//g", "-e", "s/’//g", "-e", "s/…//g",
                "-e", "s/-/-/g", "-e", "s/–/-/g", "-e", "s/—/-/g", "-e", "s/―/-/g", "-e", "s/−/-/g", "-e", "s/‒/-/g", "-e", "s/─/-/g", "-e", "s/^Si$/Si\./g"],
                input=seg, text=True, capture_output=True).stdout for seg in text_segments]
    
    print("Text segments after sed: ", text_segments)

    with open(COTOVIA_IN_TXT_PATH, 'w') as f:
        for seg in text_segments:
            if seg:
                f.write(seg + '\n')
            else:
                f.write(',' + '\n')

    # utf-8 to iso8859-1
    subprocess.run(["iconv", "-f", "utf-8", "-t", "iso8859-1", COTOVIA_IN_TXT_PATH, "-o", COTOVIA_IN_TXT_PATH_ISO], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    # call cotovia with -t3 option
    subprocess.run(["cotovia", "-i", COTOVIA_IN_TXT_PATH_ISO, "-t3", "-n"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    # iso8859-1 to utf-8
    subprocess.run(["iconv", "-f", "iso8859-1", "-t", "utf-8", COTOVIA_OUT_PRE_PATH, "-o", COTOVIA_OUT_PRE_PATH_UTF8], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    segs = []
    try:
        with open(COTOVIA_OUT_PRE_PATH_UTF8, 'r') as f:
            segs = [line.rstrip() for line in f]
            segs = [remove_tra3_tags(line) for line in segs]
    except:
        print("ERROR: Couldn't read cotovia output")

    subprocess.run(["rm", COTOVIA_IN_TXT_PATH, COTOVIA_IN_TXT_PATH_ISO, COTOVIA_OUT_PRE_PATH, COTOVIA_OUT_PRE_PATH_UTF8], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    print("Cotovia segments: ", segs)

    return segs

def is_number(index, text):
    if index == 0:
        return False
    elif index == len(text) - 1:
        return False
    else:
        return canBeNumber(text[index - 1]) and canBeNumber(text[index + 1])

#Splits text from punctuation marks, gives list of segments in between and the punctuation marks. Skips punctuation not present in training.
def split_punc(text):
    segments = []
    puncs = []
    curr_seg = ""
    previous_punc = False
    for i, c in enumerate(text):        
        if c in PUNCLIST and not previous_punc and not is_number(i, text):
            segments.append(curr_seg.strip())
            puncs.append(c)
            curr_seg = ""
            previous_punc = True
        elif c in PUNCLIST and previous_punc:
            puncs[-1] += c
        else:
            curr_seg += c
            previous_punc = False
    
    segments.append(curr_seg.strip())

    print("Split Segments: ", segments)

    #Remove empty segments in the list
    segments = filter(None, segments)

    # store segments as a list
    segments = list(segments)

    print("Split Segments: ", segments)
    print("Split Puncs: ", puncs)

    return segments, puncs

def merge_punc(text_segs, puncs):
    merged_str = ""
    print("Text segs: ", text_segs)
    print("Puncs: ", puncs)
    for i, seg in enumerate(text_segs):
        merged_str += seg + " "
        
        if i < len(puncs):
            merged_str += puncs[i] + " "

    # remove spaces before , . ! ? ; : ) ] of the merged string
    merged_str = re.sub(r"\s+([.,!?;:)\]])", r"\1", merged_str)

    # remove spaces after ( [ ¡ ¿ of the merged string
    merged_str = re.sub(r"([\(\[¡¿])\s+", r"\1", merged_str)
    
    print("Merged str: ", merged_str)

    return merged_str.strip()


def text_preprocess(text):
    
    ### - , ' and () by commas
    # substitute '- text -' to ', text,'
    text = re.sub(r"(\w+)\s+-([^-]*?)-\s+([^-]*?)", r"\1, \2, ", text)

    # substitute ' - ' by ', '
    text = re.sub(r"(\w+[!\?]?)\s+-\s*", r"\1, ", text)

    # substitute ' ( text )' to ', text,'
    text = re.sub(r"(\w+)\s*\(\s*([^\(\)]*?)\s*\)", r"\1, \2,", text)

    # remove inverted marks
    text = re.sub(r'([¡¿])', r'', text)

    #Split from punc
    text_segments, puncs = split_punc(text)

    cotovia_phon_segs = to_cotovia(text_segments)

    cotovia_phon_str = merge_punc(cotovia_phon_segs, puncs)

    phon_str = accent_convert(cotovia_phon_str)

    # add final punctuation mark if it is not present
    if not re.match(r"[.!?]", phon_str[-1]):
        phon_str = phon_str + "."

    return phon_str
    