import re

# http://stackoverflow.com/questions/4236243/python-replace-tags-but-preserve-inner-text
_replacements = {
    '[[': '<b>',
    ']]': '</b>',
    '{{': '<i>',
    '}}': '</i>',
}

def _do_replace(match):
    return _replacements.get(match.group(0))

def replace_tags(text, _re=re.compile('|'.join(re.escape(r) for r in _replacements))):
    return _re.sub(_do_replace, text)

kk=replace_tags("This is an [[example]] sentence. It is [[{{awesome}}]].")

print (kk)

print ("------------------------------")







ln = "Hola ''caracola'', hola ''caraculo'' y [[corchetes]] adios"


# r'\[\[(.*?)\]\]', r'<b>\1</b>',

p = re.compile(r'\'\'(.*?)\'\'')
m = p.search(ln)
m2 = p.findall(ln)
for tag in m2:
        print p.sub("", tag)
        
      
phone = "2004-959-559 #This is Phone Number"

# Delete Python-style comments
num = re.sub(r'\'\'(.*?)\'\'', "", phone)
print "Phone Num : ", num      
        
#if m:
#    print('Match found: ')
#            if m.group(0):
#                print(m.group(0))
#            if m.group(1):
#                print(m.group(1))
#            if m.group(2):
#                print(m.group(2))
    #  self.lin = p.sub( newImg, self.lin)
#    print(m.group(0))
    #print(m.group(1))  
    #print(m.group(2))  
#else:
#    print ('No match found in for [expr] in  [' + ln + ']')
