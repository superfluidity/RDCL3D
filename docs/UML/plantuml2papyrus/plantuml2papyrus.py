#!/usr/bin/env python2

import sys
from papyrus import *

rootclass = None
classes = {}
associations = []

f = open(sys.argv[1])

for line in f.readlines():
    l = line.strip()
    if len(l) == 0:
        continue

    if l.startswith("package"):
        continue #TODO not implemented yet

    if l.startswith("/'"):
        continue #TODO not implemented yet

    if l.startswith("class"):
        tokens = l.split(" ")
        i = 0
        t = tokens[i]
        while t != "class":
            t = tokens[i]
            i+=1
        classname = tokens[i+1].strip()
        # TODO: parse the contents of the class declaration
        newclass = UMLClass(classname)
        classes[classname] = newclass
        print "class " + classname
        if rootclass == None:
            rootclass = classname

    elif l.find("o--") >= 0:
        # association from class A to class B
        newassoc = UMLAssociation("")
        classA, classB = l.split("o--")

        tokens = [t for t in classA.split('"') if len(t.strip()) > 0]
        classAname = tokens[0].strip()
        # TODO: class A multiplicity
        assocClassA = classes[classAname]

        tokens = [t for t in classB.split('"') if len(t.strip()) > 0]
        if len(tokens) > 1:
            classBmult = tokens[0].strip()
            classBname = tokens[1].strip()
        else:
            classBmult = ""
            classBname = tokens[0].strip()
        assocClassB = classes[classBname]

        print classAname + " o-- " + classBname
        newassoc.addLink(assocClassA, assocClassB, "shared", classBmult)
        associations.append(newassoc)

    elif l.find("*--") >= 0:
        # association from class A to class B
        newassoc = UMLAssociation("")
        classA, classB = l.split("*--")

        tokens = [t for t in classA.split('"') if len(t.strip()) > 0]
        classAname = tokens[0].strip()
        # TODO: class A multiplicity
        assocClassA = classes[classAname]

        tokens = [t for t in classB.split('"') if len(t.strip()) > 0]
        if len(tokens) > 1:
            classBmult = tokens[0].strip()
            classBname = tokens[1].strip()
        else:
            classBmult = ""
            classBname = tokens[0].strip()
        assocClassB = classes[classBname]

        print classAname + " *-- " + classBname
        newassoc.addLink(assocClassA, assocClassB, "composite", classBmult)
        associations.append(newassoc)



uml_Model = UMLModel()
uml_Model.extend(classes.values())
uml_Model.extend(associations)

print "writing model"
f = open('model.uml', 'w')
f.write(ET.tostring(uml_Model.toET(), encoding='UTF-8'))
f.close()

print "writing notation"
f = open('model.notation', 'w')
f.write(ET.tostring(uml_Model.toNotation(), encoding='UTF-8'))
f.close()


