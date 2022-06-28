#!/usr/bin/env python3
import acts
from pathlib import Path

u = acts.UnitConstants
gdc = acts.examples.GenericDetector.Config()
detector = acts.examples.GenericDetector()
trackingGeometry, contextDecorators = detector.finalize(gdc, None)

field = acts.ConstantBField(acts.Vector3(0, 0, 2 * u.T))
from acts.examples.simulation.fatras import runFatras
runFatras(trackingGeometry, field, Path.cwd()).run()
