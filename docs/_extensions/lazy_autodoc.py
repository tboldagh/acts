import re
from typing import Dict, Any, List, Tuple
from pathlib import Path
import os

from sphinx.application import Sphinx


__version__ = "0.1.0"


def run() -> None:
    doc_dir = Path(__file__).parent.parent
    api_index_target = doc_dir / "api/api.md"

    roles = [
        "class",
        "struct",
        "type",
        #  "func",
        "enum",
    ]

    role_names = {
        "class": "Classes",
        "struct": "Structs",
        "type": "Types",
        "enum": "Enums",
        "func": "Functions",
    }

    directives = {
        "class": "doxygenclass",
        "struct": "doxygenstruct",
        "type": "doxygentypedef",
        "func": "doxygenfunction",
        "enum": "doxygenenum",
    }

    role_instances = {k: set() for k in roles}

    role_instances["type"] |= {
        "Acts::ActsScalar",
        "Acts::ActsVector",
        "Acts::ActsMatrix",
        "Acts::ActsSquareMatrix",
        "Acts::SquareMatrix2",
        "Acts::SquareMatrix3",
        "Acts::SquareMatrix4",
        "Acts::BoundMatrix",
        "Acts::BoundSquareMatrix",
        "Acts::Vector2",
        "Acts::Vector3",
        "Acts::Vector4",
        "Acts::BoundVector",
        "Acts::BoundTrackParameters",
        "Acts::Transform2",
        "Acts::Transform3",
        "Acts::AngleAxis3",
        "Acts::RotationMatrix2",
        "Acts::RotationMatrix3",
        "Acts::Translation2",
        "Acts::Translation3",
        "Acts::GeometryContext",
        "Acts::FreeVector",
        "Acts::FreeMatrix",
        "Acts::SurfaceVector",
        "Acts::Intersection3D",
        "Acts::OrientedSurface",
        "Acts::OrientedSurfaces",
        "Acts::BoundToFreeMatrix",
        "Acts::FreeToBoundMatrix",
        "Acts::FreeSquareMatrix",
        "Acts::FreeToPathMatrix",
    }

    role_instances["struct"] |= {
        "Acts::DenseStepperPropagatorOptions",
        "Acts::Experimental::DetectorNavigator::State",
        "Acts::Geant4PhysicalVolumeSelectors::AllSelector",
        "Acts::Geant4PhysicalVolumeSelectors::NameSelector",
    }

    role_instances["class"] |= {
        "Acts::BinningData",
        "Acts::Direction",
        "Acts::ConstrainedStep",
        "Acts::IAxis",
        "Acts::SeedFilter",
        "Acts::BoundaryCheck",
        "Acts::ConeVolumeBounds",
        "Acts::CuboidVolumeBounds",
        "Acts::CylinderVolumeBounds",
        "Acts::CutoutCylinderVolumeBounds",
        "Acts::GenericCuboidVolumeBounds",
        "Acts::TrapezoidVolumeBounds",
        "Acts::GeometryObject",
        "Acts::TrackContainer",
        "Acts::ConeLayer",
        "Acts::CylinderLayer",
        "Acts::IdentifiedDetectorElement",
        "Acts::DiscLayer",
        "Acts::PlaneLayer",
        "Acts::NullBField",
        "Acts::DiscBounds",
        "Acts::PlanarBounds",
        "Acts::AbstractVolume",
        "Acts::AnnulusBounds",
        "Acts::DiamondBounds",
        "Acts::ConvexPolygonBounds",
        "Acts::ConvexPolygonBoundsBase",
        "Acts::Logging::LevelOutputDecorator",
        "Acts::Logging::NamedOutputDecorator",
        "Acts::Logging::ThreadOutputDecorator",
        "Acts::Logging::TimedOutputDecorator",
        "Acts::Logging::DefaultFilterPolicy",
        "Acts::Logging::DefaultPrintPolicy",
    }

    role_instances["func"] = {
        "Acts::CylinderVolumeBuilder::logger",
        "Acts::getDefaultLogger",
        "Acts::getDummyLogger",
        "Acts::makeDefaultBetheHeitlerApprox",
        "Acts::convertDD4hepDetector",
    }

    role_instances["enum"] = {
        "Acts::BinningValue",
        "Acts::BinningType",
        "Acts::BinningValue",
        "Acts::BoundIndices",
        "Acts::FreeIndices",
        "Acts::MagneticFieldError",
    }

    role_ex = re.compile(r"[{:](" + "|".join(roles) + r")[}:]`(.+?)`")

    def process_roles(file: Path) -> List[Tuple[str, str]]:
        text = file.read_text()
        return [m.groups() for m in role_ex.finditer(text)]

    for dirpath, _, filenames in os.walk(doc_dir):
        dirpath = Path(dirpath)
        for file in filenames:
            file = dirpath / file
            if file.suffix not in (".rst", ".md"):
                continue
            for role, arg in process_roles(file):
                role_instances[role].add(arg)

    # add members to their parents

    api_preamble = """
    """

    with api_index_target.open("w") as fh:
        fh.write("# API Reference\n\n")
        fh.write(api_preamble)
        for role, instances in sorted(role_instances.items(), key=lambda x: x[0]):
            fh.write(f"## {role_names[role]}\n")
            for instance in sorted(instances):
                fh.write(
                    f"""
:::{{{directives[role]}}} {instance}
:::
"""
                )
            fh.write("\n")


def setup(app: Sphinx) -> Dict[str, Any]:
    run()

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
