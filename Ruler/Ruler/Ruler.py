#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        
        sketchTexts = sketch.sketchTexts
        
        lines = sketch.sketchCurves.sketchLines


        horizontalAlignment = adsk.core.HorizontalAlignments.CenterHorizontalAlignment
        verticalAlignment = adsk.core.VerticalAlignments.MiddleVerticalAlignment
            

        # set to True to make a scale that runs the other way
        rightToLeft = False

        #dimensions in cm, hilariously
        bottomY = 0
        topYmm = .3
        topY5mm = .5
        topYcm = 0.7
        textHeightcm = 0.5
        textHeight10cm = 0.8
        xMax = 600 # in printed units, not sketch dims, so in mm
        for x in range(xMax):

            if rightToLeft:
                xcm = -x/10
            else:
                xcm = x/10

            if x % 10 == 0:
                #line and text

                if x%100 == 0:
                    textHeight = textHeight10cm
                else:
                    textHeight = textHeightcm

                sketchTextInput = sketchTexts.createInput2(repr(x), textHeight)
                sketchTextInput.fontName = "DIN Condensed"

                cornerPt = adsk.core.Point3D.create(xcm, topYcm, 0.0)
                diagonalPt = adsk.core.Point3D.create(xcm+1.0, topYcm+textHeight, 0.0)
                sketchTextInput.setAsMultiLine(cornerPt, diagonalPt, horizontalAlignment, verticalAlignment)

                # givingrotation to frame about right bottom corner of frame
                angle = 3.14*0.5
                multilineDef = sketchTextInput.definition
                multilineDef.rotate(angle, adsk.fusion.TextBoxKeyPoints.MiddleLeftTextBoxKeyPoint)

                sketchText = sketchTexts.add(sketchTextInput)

                # TODO - maybe explode the text here ? Have to be done one by one if you do it later.
            
                lines.addByTwoPoints(adsk.core.Point3D.create(xcm,0,0), adsk.core.Point3D.create(xcm,topYcm,0))

            elif x % 5 == 0:
                #medium line
                lines.addByTwoPoints(adsk.core.Point3D.create(xcm,0,0), adsk.core.Point3D.create(xcm,topY5mm,0))
            else:
                #short line
                lines.addByTwoPoints(adsk.core.Point3D.create(xcm,0,0), adsk.core.Point3D.create(xcm,topYmm,0))


        if False:
            cornerPt = adsk.core.Point3D.create(5.0, -10.0, 0.0)
            diagonalPt = adsk.core.Point3D.create(-10.0, 10.0, 0.0)
            
            horizontalAlignment = adsk.core.HorizontalAlignments.CenterHorizontalAlignment
            verticalAlignment = adsk.core.VerticalAlignments.BottomVerticalAlignment
            
            #create the text input
            sketchTextInput = sketchTexts.createInput2('Multiline Text', 15)

            # make input valid for multiline text type
            sketchTextInput.setAsMultiLine(cornerPt, diagonalPt, horizontalAlignment, verticalAlignment)

            # get the MultiLineTextDefinition
            multilineDef = sketchTextInput.definition
            
            # givingrotation to frame about right bottom corner of frame
            angle = 3.14*0.25
            multilineDef.rotate(angle, adsk.fusion.TextBoxKeyPoints.BottomRightTextBoxKeyPoint)

            # create the SketchText object
            sketchText = sketchTexts.add(sketchTextInput)
            
            verticalAlignment1 = adsk.core.VerticalAlignments.MiddleVerticalAlignment

            # get the MultiLineTextDefinition
            multilineDef1 = sketchText.definition

            #Edit WorkFlow
            # Change the vertical alignment and sapcing of text
            multilineDef1.verticalAlignment = verticalAlignment1

            # Get the frame edges
            textFrameEdges = multilineDef1.rectangleLines

            # Create the extrusion
            extrudes = rootComp.features.extrudeFeatures
            extInput = extrudes.createInput(sketchText, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            distance = adsk.core.ValueInput.createByReal(0.8)
            extInput.setDistanceExtent(False, distance)
            extInput.isSolid = True
            
            ext = extrudes.add(extInput)
            
            m = sketch.sketchTexts.count
            n = sketch.profiles.count
            ui.messageBox("sketchTexts.count:  %i  \nprofiles .count: %i" % (m, n))
            #sketch = sketches.item(0)
            #sketchText = sketch.sketchTexts.item(0)
            #sketchText.text = 'new text'

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
