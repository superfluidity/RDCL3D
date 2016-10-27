import xml.etree.ElementTree as ET
import random


def randomeid():
    "return a random id for an element"
    r = "_"
    while len(r) < 22:
        r += chr(random.randint(ord('A'), ord('Z')))
    return r

class UMLElement():
    "base UML element class"
    def __init__(self, name, eid=""):
        self.name = name
        if eid != "":
            self.eid = eid
        else:
            self.eid = randomeid()

class UMLLinkException():
    pass

class UMLClass(UMLElement):
    "this class represents an UML class element"
    description = ""
    description_eid = None

    def toET(self):
        "convert this class into an ElementTree object"
        e = ET.Element('packagedElement', attrib={
            'xmi:type': "uml:Class",
            'xmi:id': self.eid,
            'name': self.name
            })

        if self.description != "":
            self.description_eid = randomeid()
            o = ET.SubElement(e, 'ownedAttribute', attrib={
                'xmi:type': "uml:Property",
                'xmi:id': randomeid(),
                'name': "Attribute1"
                })
            n = ET.SubElement(e, 'nestedClassifier', attrib={
                'xmi:type': "uml:DataType",
                'xmi:id': self.description_eid,
                'name': self.description
                })
        return e

    def toNotation(self):
        "convert this class into an ElementTree object for the notation XML"
        self.shapeeid = randomeid()
        k = ET.Element('children', attrib={
            'xmi:type': "notation:Shape",
            'xmi:id': self.shapeeid,
            'type': "Class_Shape"
            })

        e = ET.SubElement(k, 'element', attrib={
            'xmi:type': "uml:Class",
            'href': "model.uml#%s" % self.eid
            })
        l = ET.SubElement(k, 'layoutConstraint', attrib={
            'xmi:type': "notation:Bounds",
            'xmi:id': randomeid(),
            })

        c = ET.SubElement(k, 'children', attrib={
            'xmi:type': "notation:DecorationNode",
            'xmi:id': randomeid(),
            'type': "Class_NameLabel"
            })
        c = ET.SubElement(k, 'children', attrib={
            'xmi:type': "notation:DecorationNode",
            'xmi:id': randomeid(),
            'type': "Class_FloatingNameLabel"
            })
        l = ET.SubElement(c, 'layoutConstraint', attrib={
            'xmi:type': "notation:Location",
            'xmi:id': randomeid(),
            'y': "5"
            })

        c = ET.SubElement(k, 'children', attrib={
            'xmi:type': "notation:BasicCompartment",
            'xmi:id': randomeid(),
            'type': "Class_AttributeCompartment"
            })
        if self.description != "" and self.description_eid != None:
            h = ET.SubElement(c, 'children', attrib={
                'xmi:type': "notation:Shape",
                'xmi:id': randomeid(),
                'type': "DataType_ClassNestedClassifierLabel"
                })
            e = ET.SubElement(h, 'element', attrib={
                'xmi:type' : "uml:DataType",
                'href': "model.uml#%s" % self.description_eid
                })
            l = ET.SubElement(h, 'layoutConstraint', attrib={
                'xmi:type': "notation:Location",
                'xmi:id': randomeid(),
                })
        s = ET.SubElement(c, 'styles', attrib={
            'xmi:type': "notation:TitleStyle",
            'xmi:id': randomeid(),
            })
        s = ET.SubElement(c, 'styles', attrib={
            'xmi:type': "notation:SortingStyle",
            'xmi:id': randomeid(),
            })
        s = ET.SubElement(c, 'styles', attrib={
            'xmi:type': "notation:FilteringStyle",
            'xmi:id': randomeid(),
            })
        l = ET.SubElement(c, 'layoutConstraint', attrib={
            'xmi:type': "notation:Bounds",
            'xmi:id': randomeid(),
            })

        c = ET.SubElement(k, 'children', attrib={
            'xmi:type': "notation:BasicCompartment",
            'xmi:id': randomeid(),
            'type': "Class_OperationCompartment"
            })
        s = ET.SubElement(c, 'styles', attrib={
            'xmi:type': "notation:TitleStyle",
            'xmi:id': randomeid(),
            })
        s = ET.SubElement(c, 'styles', attrib={
            'xmi:type': "notation:SortingStyle",
            'xmi:id': randomeid(),
            })
        s = ET.SubElement(c, 'styles', attrib={
            'xmi:type': "notation:FilteringStyle",
            'xmi:id': randomeid(),
            })
        l = ET.SubElement(c, 'layoutConstraint', attrib={
            'xmi:type': "notation:Bounds",
            'xmi:id': randomeid(),
            })

        c = ET.SubElement(k, 'children', attrib={
            'xmi:type': "notation:BasicCompartment",
            'xmi:id': randomeid(),
            'type': "Class_NestedClassifierCompartment"
            })
        s = ET.SubElement(c, 'styles', attrib={
            'xmi:type': "notation:TitleStyle",
            'xmi:id': randomeid(),
            })
        s = ET.SubElement(c, 'styles', attrib={
            'xmi:type': "notation:SortingStyle",
            'xmi:id': randomeid(),
            })
        s = ET.SubElement(c, 'styles', attrib={
            'xmi:type': "notation:FilteringStyle",
            'xmi:id': randomeid(),
            })
        l = ET.SubElement(c, 'layoutConstraint', attrib={
            'xmi:type': "notation:Bounds",
            'xmi:id': randomeid(),
            })

        return k

    def addDescription(self, description):
        "add a (short) description for the class"
        self.description = description


class UMLAssociation(UMLElement):
    "this class represents an UML association element"
    link = None
    aggregation = ""
    multiplicity = ""

    def addLink(self, srcClass, dstClass, aggregationType, multiplicity=""):
        "defines an association from srcClass to dstClass, which are assumed to be UMLClass objects."
        self.link = (srcClass, dstClass)

        if not aggregationType in ["shared", "composite"]:
            raise UMLLinkException()
        self.aggregation = aggregationType

        self.multiplicity = multiplicity

    def __literaltype(self, literal):
        if literal == "*":
            return "uml:LiteralUnlimitedNatural"
        else:
            return "uml:LiteralInteger"

    def toET(self):
        "convert this class into an ElementTree object"
        if self.link == None or not self.aggregation in ["shared", "composite"]:
            raise UMLLinkException()

        end1eid = randomeid()
        end2eid = randomeid()

        pe =  ET.Element('packagedElement', attrib={
            'xmi:type': "uml:Association",
            'xmi:id': self.eid,
            'memberEnd': "%s %s" % (end1eid, end2eid)
            }) 

        annotations = ET.SubElement(pe, 'eAnnotations', attrib={
            'xmi:type': "ecore:EAnnotation",
            'xmi:id': randomeid(),
            'source': 'org.eclipse.papyrus'
            })

        details = ET.SubElement(annotations, 'details', attrib={
            'xmi:type': "ecore:EStringToStringMapEntry",
            'xmi:id': randomeid(),
            'key': "nature",
            'value': "UML_Nature"
            })

        ownedEnd1 = ET.SubElement(pe, 'ownedEnd', attrib={
            'xmi:type': "uml:Property",
            'xmi:id': end1eid,
            'name': self.link[0].name.lower(),
            'type': self.link[0].eid,
            'aggregation': self.aggregation,
            'association': self.eid
            })

        ownedEnd2 = ET.SubElement(pe, 'ownedEnd', attrib={
            'xmi:type': "uml:Property",
            'xmi:id': end2eid,
            'name': self.link[1].name.lower(),
            'type': self.link[1].eid,
            'association': self.eid
            })

        lowerMultiplicity = upperMultiplicity = None
        try:
            lowerMultiplicity, upperMultiplicity = [x for x in self.multiplicity.split('.') if x != '']
        except:
            pass

        if lowerMultiplicity != None:
            lower = ET.SubElement(ownedEnd2, 'lowerValue', attrib={
            'xmi:type': self.__literaltype(lowerMultiplicity),
            'xmi:id': randomeid(),
            'value': lowerMultiplicity
            })

        if upperMultiplicity != None:
            upper = ET.SubElement(ownedEnd2, 'upperValue', attrib={
            'xmi:type': self.__literaltype(upperMultiplicity),
            'xmi:id': randomeid(),
            'value': upperMultiplicity
            })

        return pe

    def toNotation(self):
        "convert this class into an ElementTree object for the notation XML"

        v = ET.Element('edges', attrib={
            'xmi:type': "notation:Connector",
            'xmi:id': randomeid(),
            'type': "Association_Edge",
            'source': self.link[0].shapeeid, #ref to the shape element
            'target': self.link[1].shapeeid  #ref to the shape element
            })

        c = ET.SubElement(v, 'children', attrib={
            'xmi:type': "notation:DecorationNode",
            'xmi:id': randomeid(),
            'type': "Association_StereotypeLabel"
            })
        l = ET.SubElement(c, 'layoutConstraint', attrib={
            'xmi:type': "notation:Location",
            'xmi:id': randomeid(),
            'y': "-20"
            })
        
        c = ET.SubElement(v, 'children', attrib={
            'xmi:type': "notation:DecorationNode",
            'xmi:id': randomeid(),
            'type': "Association_NameLabel"
            })
        l = ET.SubElement(c, 'layoutConstraint', attrib={
            'xmi:type': "notation:Location",
            'xmi:id': randomeid(),
            'y': "20"
            })

        c = ET.SubElement(v, 'children', attrib={
            'xmi:type': "notation:DecorationNode",
            'xmi:id': randomeid(),
            'type': "Association_TargetRoleLabel"
            })
        l = ET.SubElement(c, 'layoutConstraint', attrib={
            'xmi:type': "notation:Location",
            'xmi:id': randomeid(),
            'y': "-20"
            })

        c = ET.SubElement(v, 'children', attrib={
            'xmi:type': "notation:DecorationNode",
            'xmi:id': randomeid(),
            'type': "Association_SourceRoleLabel"
            })
        l = ET.SubElement(c, 'layoutConstraint', attrib={
            'xmi:type': "notation:Location",
            'xmi:id': randomeid(),
            'y': "20"
            })

        c = ET.SubElement(v, 'children', attrib={
            'xmi:type': "notation:DecorationNode",
            'xmi:id': randomeid(),
            'type': "Association_SourceMultiplicityLabel"
            })
        l = ET.SubElement(c, 'layoutConstraint', attrib={
            'xmi:type': "notation:Location",
            'xmi:id': randomeid(),
            'y': "20"
            })

        c = ET.SubElement(v, 'children', attrib={
            'xmi:type': "notation:DecorationNode",
            'xmi:id': randomeid(),
            'type': "Association_TargetMultiplicityLabel"
            })
        l = ET.SubElement(c, 'layoutConstraint', attrib={
            'xmi:type': "notation:Location",
            'xmi:id': randomeid(),
            'y': "-20"
            })

        s = ET.SubElement(v, 'styles', attrib={
            'xmi:type': "notation:FontStyle",
            'xmi:id': randomeid(),
            })
        
        e = ET.SubElement(v, 'element', attrib={
            'xmi:type': "uml:Association",
            'href': "model.uml#%s" % self.eid
            })

        b = ET.SubElement(v, 'bendpoints', attrib={
            'xmi:type': "notation:RelativeBendpoints",
            'xmi:id': randomeid(),
            })

        a = ET.SubElement(v, 'sourceAnchor', attrib={
            'xmi:type': "notation:IdentityAnchor",
            'xmi:id': randomeid(),
            })

        a = ET.SubElement(v, 'targetAnchor', attrib={
            'xmi:type': "notation:IdentityAnchor",
            'xmi:id': randomeid(),
            })

        return v


class UMLModel(UMLElement):
    def __init__(self):
        UMLElement.__init__(self, "")

        self.model = ET.Element('uml:Model', attrib={
            'xmi:version': "20131001",
            'xmi:id': self.eid,
            'name': "NSD",
            'xmlns:xmi': "http://www.omg.org/spec/XMI/20131001",
            'xmlns:ecore': "http://www.eclipse.org/emf/2002/Ecore",
            'xmlns:uml': "http://www.eclipse.org/uml2/5.0.0/UML"
            })

        # notation
        self.notation = ET.Element('notation:Diagram', attrib={
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

        e = ET.SubElement(self.notation, 'element', attrib={
                'xmi:type': "uml:Model",
                'href': "model.uml#%s" % self.eid
        })

        s = ET.SubElement(self.notation, 'styles', attrib={
                'xmi:type': "notation:StringValueStyle",
                'name': "diagram_compatibility_version",
                'stringValue': "1.2.0",
                'xmi:id': randomeid()
        })

        s = ET.SubElement(self.notation, 'styles', attrib={
                'xmi:type': "notation:DiagramStyle",
                'xmi:id': randomeid()
        })

        s = ET.SubElement(self.notation, 'styles', attrib={
                'xmi:type': "style:PapyrusViewStyle",
                'xmi:id': randomeid()
        })
        o = ET.SubElement(s, 'owner', attrib={
                'xmi:type': "uml:Model",
                'href': "model.uml#%s" % self.eid
        })

    def add(self, element):
        self.model.append(element.toET())
        self.notation.append(element.toNotation())

    def extend(self, elementlist):
        self.model.extend([e.toET() for e in elementlist])
        self.notation.extend([e.toNotation() for e in elementlist])

    def toET(self):
        return self.model

    def toNotation(self):
        return self.notation


if __name__ == "__main__":

    uml_Model = UMLModel()

    class1 = UMLClass("Classe1")
    class1.addDescription("IFA011.1.2.3")
    class2 = UMLClass("Classe2")
    class3 = UMLClass("Classe3")
    uml_Model.add(class1)
    uml_Model.add(class2)
    uml_Model.add(class3)

    asso1 = UMLAssociation("assoc1")
    asso1.addLink(class1, class2, "shared", "1..*")
    uml_Model.add(asso1)

    asso2 = UMLAssociation("assoc1")
    asso2.addLink(class2, class3, "composite", "0..*")
    uml_Model.add(asso2)

    print "writing model"
    f = open('model.uml', 'w')
    f.write(ET.tostring(uml_Model.toET(), encoding='UTF-8'))
    f.close()

    print "writing notation"
    f = open('model.notation', 'w')
    f.write(ET.tostring(uml_Model.toNotation(), encoding='UTF-8'))
    f.close()


