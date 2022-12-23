import requests


baseurl = "https://leagueoflegends.fandom.com/wiki/"

def parsename(name):
    twowords = 0
    for i in range(len(name)):
        if name[i] == ' ':
            twowords = 1
            idx = i
            break
        if name[i] == "'":
            twowords = 2
            idx = i
            break

    if twowords == 1:
        ret = baseurl + str(
            name[0].upper() + name[1:idx] + '_' + name[idx + 1].upper() + name[idx + 2:len(name)]) + '/LoL'
    elif twowords == 2:
        ret = baseurl + str(name[0:idx] + "'" + name[idx + 1].upper() + name[idx + 2:len(name)]) + '/LoL'
    else:
        ret = baseurl + str(name) + '/LoL'
    return ret

def stat(webtxt, stat):
   # lvl 1 stat
    start = webtxt.find('</a></div><span id="' + stat + '_')
    if start == -1:
        return start
    stat1 = 0.0
    while True:
        if webtxt[start].isdigit():
             break
        start += 1
    end = start
    while True:
        if not webtxt[end].isdigit():
            break
        stat1 = 10.0 * stat1 + int(webtxt[end])
        end += 1

    # stat per lvl
    start2 = start + 5
    while True:
        if webtxt[start2].isdigit():
            break
        start2 += 1

    perlvl = 0.0
    flt = 0
    end2 = start2
    while True:
        if not webtxt[end2].isdigit() and webtxt[end2] != '.':
            break
        elif webtxt[end2] == '.':
            flt = 10
        if flt > 0 and webtxt[end2] != '.':
            perlvl += float(webtxt[end2])/(flt)
            flt *= 10
        elif webtxt[end2] != '.':
            perlvl = 10 * perlvl + int(webtxt[end2])
        end2 += 1

    stat18 = stat1 + 17.0 * perlvl

    print(stat + ': ' + '%.1f' % stat1 + ' - ' + '%.1f' % stat18 + ', ' + '%.1f' % perlvl + ' per level')
    return start

def resource(webtxt):
    # check for mana or energy
    start = webtxt.find('</a></div><span id="ResourceBar_')
    if start == -1:
        start = webtxt.find('</a></span></div><span id="ResourceBar_')

    # if not, print secondary resource type
    if start == -1:
        start = webtxt.find('Secondary Bar</a></div> <span class="glossary" style="white-space:pre; position:relative;"'
                            ' data-game="lol" data-tip=')
        if(start == -1):  # if no mana, energy, or secondary resource
            print("Secondary Resource: N/A")
            return
        start += 117
        end = start
        while True:
            if not webtxt[end].isalpha():
                break
            end += 1

        print("Secondary Resource: " + webtxt[start:end])
        return

    # find name of resource
    end = start
    start -= 1
    while True:
        if not webtxt[start].isalpha():
            break
        start -= 1
    start += 1

    # find base resource at lvl1
    start2 = end
    stat1 = 0
    while True:
        if webtxt[start2].isdigit():
            break
        start2 += 1
    end2 = start2
    while True:
        if not webtxt[end2].isdigit():
            break
        stat1 = 10 * stat1 + int(webtxt[end2])
        end2 += 1

    # resource gain per lvl
    start3 = end2 + 1
    while True:
        if webtxt[start3].isdigit():
            break
        start3 += 1


    perlvl = 0
    end3 = start3
    while True:
        if not webtxt[end3].isdigit():
            break
        perlvl = 10 * perlvl + int(webtxt[end3])
        end3 += 1

    stat18 = stat1 + 17 * perlvl

    print(webtxt[start:end] + ': ' + str(stat1) + ' - ' + str(stat18) + ', ' + str(perlvl) + ' per level')
    return

def getstats(webtxt, namelength):
    # name
    start = webtxt.find('<meta property="og:title" content=')
    start += 35

    print('\n' + webtxt[start:(start + namelength)])

    # title
    start = webtxt.find('font-weight: bold; text-transform: uppercase; font-size: 14px; color: #dddddd;">')
    start += 80
    idx = start
    while True:
        if webtxt[idx] == '<':
            break
        idx += 1
    print(webtxt[start].upper() + webtxt[start + 1:idx] + '\n')

    stat(webtxt, 'Health')
    resource(webtxt)

    stat(webtxt, 'AttackDamage')
    stat(webtxt, 'Armor')
    stat(webtxt, 'MagicResist')

    print("\n\n")
    return


while True:
    print("LoL Champion Statistics\n")
    print("A. Single Champion Stats")
    print("Q. Quit\n")

    command = input('\nEnter a command:')
    #print(command)
    if command.upper() == 'A':
        champ = input("Champion: ")
        #print(champ)

        url = parsename(champ)
        #print(url)

        page = requests.get(url)

        if page.status_code != 200:
            print("Champion not found")
        else:
            #print(page.text)
            getstats(page.text, len(champ))
    elif command.upper() == 'Q':
        break

