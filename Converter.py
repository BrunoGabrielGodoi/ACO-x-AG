

def ConverttxtToMatrix(nCitys,pathToFile):

    numeroDeCidades = nCitys
    f = open(pathToFile,"r")



    contents = f.read()
    espaço = True

    finalstring = ""
    print(len(contents))


    for i in range(0,(numeroDeCidades+1)):
        if i == 0:
            finalstring += "[   [ 0,"
        elif i == numeroDeCidades:
            finalstring += str(i) + "]," + "\n"
        else:
            finalstring += str(i) + ", "


    i = 1
    for index,c in enumerate(contents):


        if index == 0:
            finalstring += "[ " + str(i) + ", "
            i +=1

        if c == ' ' :
            if espaço:
                pass
                finalstring += " "
            else:
                finalstring += ","
                #contents[index] = ','
                espaço = True
        elif c == "\n":
            finalstring += "]," + "\n" + "[ " + str(i) + ", "
            espaço = True
            i += 1

        else:
            finalstring += c
            espaço = False
    else:
        finalstring += "]   ]" 


    print(finalstring)

ConverttxtToMatrix(26,"graph.txt")