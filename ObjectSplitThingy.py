import c4d
from c4d import gui
from c4d import utils

def main():
    obj = GetAllObjects()
    obj = list(filter(lambda x: any(tag.GetType() == c4d.Tpolygonselection for tag in x.GetTags()), obj))
    for x in obj:
        STags = list(filter(lambda tag: tag.GetType() == c4d.Tpolygonselection, x.GetTags()))
        TTags = list(filter(lambda tag: tag.GetType() == c4d.Ttexture, x.GetTags()))
        par = c4d.BaseObject(c4d.Onull)
        par.SetName(x.GetName())
        doc.InsertObject(par)
        count = 0
        for tagIndex in range(len(STags)): #-1
            tag = STags[tagIndex]
            matName = list(filter(lambda x: x[c4d.TEXTURETAG_RESTRICTION] == tag[c4d.ID_BASELIST_NAME], TTags))[0]
            mat = matName.GetMaterial()
            print tagIndex
            newop = split(x, tagIndex, par)
            materialTag = c4d.BaseTag(c4d.Ttexture)
            materialTag.SetMaterial(mat)
            newop.InsertTag(materialTag)
            

        par.SetAbsRot(x.GetAbsRot())
        par.SetAbsScale(x.GetAbsScale())
        par.SetAbsPos(x.GetAbsPos())
        for t in range(len(STags)):
            x.KillTag(c4d.Tpolygonselection, 0)
            
        x.Remove()
        doc.InsertObject(x,parent=par)
        c4d.EventAdd()

def split(obj, index, par):
    poly = obj.GetTag(c4d.Tpolygonselection, index)
    polyselection = obj.GetPolygonS()
    polyselection.DeselectAll()
    tagselection = poly.GetBaseSelect()
    tagselection.CopyTo(polyselection)
    maxpolies = obj.GetPolygonCount()
    newop = c4d.BaseObject(c4d.Opolygon)
    
    occindex = []
    count = 0


    for i in xrange(maxpolies):
        if polyselection.IsSelected(i):
            newop = AddPoly(obj, newop, obj.GetPolygon(i), count, occindex)
            count += 1
    doc.InsertObject(newop, parent = par)
    doc.AddUndo(c4d.UNDOTYPE_NEW, newop)
    
    utils.SendModelingCommand(command=c4d.MCOMMAND_DELETE, list=[obj],
                              mode=c4d.MODELINGCOMMANDMODE_POLYGONSELECTION,
                              doc=doc)
    return newop

def AddPoly(op,newop,poly,count,occindex,):

    pointcount = newop.GetPointCount()
    index = (poly.a, poly.b, poly.c, poly.d)
    newindex = []

    for nr in index:
        if nr not in occindex:
            occindex.append(nr)
            length = len(occindex)
            newop.ResizeObject(length, count + 1)
            newop.SetPoint(length - 1, op.GetPoint(nr))
            newindex.append(pointcount)
            pointcount += 1
        else:
            newop.ResizeObject(pointcount, count + 1)
            newindex.append(occindex.index(nr))


    newop.SetPolygon(count, c4d.CPolygon(newindex[0], newindex[1],
                     newindex[2], newindex[3]))
    newop.Message(c4d.MSG_UPDATE)
    return newop

    doc.EndUndo()
    c4d.EventAdd()


def GetAllObjects():
    mat = doc.GetFirstMaterial()
    objects = []
    index = 0
    while mat != None:
        matA = mat[c4d.ID_MATERIALASSIGNMENTS]
        for o in range(0, matA.GetObjectCount()):
            obj = matA.ObjectFromIndex(doc, o).GetObject()
            if not(obj in objects):
                objects.append(obj)
                index = index + 1
        mat = mat.GetNext()

    return objects

if __name__ == '__main__':
    main()
