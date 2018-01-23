import re
import sys
import math
import ntpath

def roundPnt(pnt):
    rounded = math.floor(int(pnt))
    if rounded < 1:
        rounded = 1

    doing some big calculation that is gross but it works
    return str(int(rounded))

if len(sys.argv) < 2:
    print("Enter the HTML file to edit fool.")
    sys.exit()

uglyhtml = open(sys.argv[1], 'r')

prettyhtml = '<font>'
tableCount = 0      #looking to edit just the first 3 tables
pageCount = 0
attrPnts = [0, 0, 0, 0, 0, 0]
attrCount = 0

for l in uglyhtml:
    #lighten up untraing spec3 and broad3 
    #Might be overkill?
    #if re.search('td\.(spec|broad)3.*\{.*\}', l):
    #     prettyhtml += l.replace('grey', 'lightgrey')
    #bold spec1 and spec2
    if re.search('td\.spec[12].*\{.*\}', l):
        prettyhtml += l.replace('}', 'font-weight: bold; }')
    elif re.search('<tr>.*(Strength|Dexterity|Constitution|Intelligence|Will|Personality).*</td>', l):
        attrPnts[attrCount] = int(re.findall(r'\d+', l)[0])
        attrCount += 1
        if attrCount == 6:
            attrCount = 0
        prettyhtml += l
    #the first tables don't need all that padding
    elif re.search('<table.*>', l) and tableCount < 3:
        for match in re.finditer(r"cellpadding=", l):
            pos = match.end() + 1
        prettyhtml += l[0:pos] + "2" + l[pos+1:]
        tableCount += 1
    #keep track of what page we're on
    elif re.search('<p class="newpage">', l):
        pageCount += 1
        prettyhtml += l
    #we got skills yo
    elif re.search('^<tr.*</tr>', l) and pageCount > 0 and attrCount < 6:
        prettyRow = ""
        for row in re.finditer(r"<tr.*?</tr>", l):
            cellCount = 0
            trained = False    #assume untrained
            prettyRow += "<tr>"
            cells = re.findall(r"<td.*?</td>", row.group(0))
            cellOffset = len(cells) - 9

            #print cellOffset
            for cell in cells:
                skillPnt = attrPnts[attrCount]
                #print cell
                if cellCount == 0 and re.search("1", cell):
                    trained = True

                if not trained:
                    if cellCount == 2 + cellOffset:
                        skillStr = re.findall(r'\d+', cell)[0]
                        cell = cell.replace(skillStr, str(skillPnt))
                    elif cellCount == 4 + cellOffset:
                        skillStr = re.findall(r'\d+', cell)[0]
                        cell = cell.replace(skillStr, roundPnt(skillPnt/2))
                    elif cellCount == 6 + cellOffset:
                        skillStr = re.findall(r'\d+', cell)[0]
                        cell = cell.replace(skillStr, roundPnt(skillPnt/4))
                    elif cellCount == 8 + cellOffset:
                        cell = cell.replace("+d4", "+d8")

                prettyRow += cell
                cellCount += 1
            prettyRow += "</tr>"
        attrCount += 1
        prettyhtml += "<tr>" + prettyRow + "</tr>"
    else:
        prettyhtml += l
#remember to set working directory to this location
uglyhtml.close()
wFile = open("pretty"+ntpath.basename('pretty'+sys.argv[1]), 'w')
wFile.write(prettyhtml)
wFile.close()
