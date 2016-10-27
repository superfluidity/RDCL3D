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



umleid = randomeid()

uml_Model = ET.Element('uml:Model', attrib={
        'xmi:version': "20131001",
        'xmi:id': umleid,
        'name': "NSD",
        'xmlns:xmi': "http://www.omg.org/spec/XMI/20131001",
        'xmlns:ecore': "http://www.eclipse.org/emf/2002/Ecore",
        'xmlns:uml': "http://www.eclipse.org/uml2/5.0.0/UML"
    })

uml_Model.extend([c.toET() for c in classes.values()])
uml_Model.extend([a.toET() for a in associations])

print "writing model"
f = open('model.uml', 'w')
f.write(ET.tostring(uml_Model, encoding='UTF-8'))
f.close()


notationdiagram = ET.Element('notation:Diagram', attrib={
        'xmi:version': "2.0",
        'xmlns:xmi': "http://www.omg.org/XMI",
        'xmlns:notation': "http://www.eclipse.org/gmf/runtime/1.0.2/notation",
        'xmlns:style': "http://www.eclipse.org/papyrus/infra/viewpoints/policy/style",
        'xmlns:uml': "http://www.eclipse.org/uml2/5.0.0/UML",
        'xmi:id': randomeid(),
        'type': "PapyrusUMLClassDiagram",
        'name': "Class Diagram",
        'measurementUnit': "Pixel"
})

e = ET.SubElement(notationdiagram, 'element', attrib={
        'xmi:type': "uml:Model",
        'href': "model.uml#%s" % umleid
})

s = ET.SubElement(notationdiagram, 'styles', attrib={
        'xmi:type': "notation:StringValueStyle",
        'name': "diagram_compatibility_version",
        'stringValue': "1.2.0",
        'xmi:id': randomeid()
})

s = ET.SubElement(notationdiagram, 'styles', attrib={
        'xmi:type': "notation:DiagramStyle",
        'xmi:id': randomeid()
})

s = ET.SubElement(notationdiagram, 'styles', attrib={
        'xmi:type': "style:PapyrusViewStyle",
        'xmi:id': randomeid()
})
o = ET.SubElement(s, 'owner', attrib={
        'xmi:type': "uml:Model",
        'href': "model.uml#%s" % umleid
})

notationdiagram.extend([c.toNotation() for c in classes.values()])
notationdiagram.extend([a.toNotation() for a in associations])

print "writing notation"
f = open('model.notation', 'w')
f.write(ET.tostring(notationdiagram, encoding='UTF-8'))
f.close()


