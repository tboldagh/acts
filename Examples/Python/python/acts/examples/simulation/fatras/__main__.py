#!/usr/bin/env python3
gdc = acts.examples.GenericDetector.Config()
detector = acts.examples.GenericDetector()
trackingGeometry, contextDecorators = detector.finalize(gdc, None)

field = acts.ConstantBField(acts.Vector3(0, 0, 2 * u.T))

runFatras(trackingGeometry, field, Path.cwd()).run()
