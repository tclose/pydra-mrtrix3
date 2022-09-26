import attr
import typing as ty
from pydra import ShellCommandTask
from pydra.engine.specs import Path, File, SpecInfo, ShellOutSpec
from .base import MRTrix3BaseSpec


MRConvertInputSpec = SpecInfo(
    name="MRConvertInputs",
    fields=[
        (
            "in_file",
            attr.ib(
                type=ty.Union[
                    Path, str
                ],  # union with str until https://github.com/nipype/pydra/issues/579 is resolved
                metadata={
                    "argstr": "{in_file}",
                    "position": 1,
                    "help_string": "input image",
                    "mandatory": True,
                },
            ),
        ),
        (
            "out_file",
            attr.ib(
                type=ty.Union[Path, str],
                metadata={
                    "position": -1,
                    "argstr": "",
                    "help_string": "output image",
                    "output_file_template": "{in_file}_converted",
                },
            ),
        ),
        (
            "coord",
            attr.ib(
                type=ty.List[float],
                metadata={
                    "sep": " ",
                    "argstr": "-coord",
                    "help_string": "extract data at the specific coordinatest",
                },
            ),
        ),
        (
            "vox",
            attr.ib(
                type=ty.List[float],
                metadata={
                    "sep": ",",
                    "argstr": "-vox",
                    "help_string": "change the voxel dimensions",
                },
            ),
        ),
        (
            "axes",
            attr.ib(
                type=ty.List[int],
                metadata={
                    "sep": ",",
                    "argstr": "-axes",
                    "help_string": "specify the axes that will be used",
                },
            ),
        ),
        (
            "scaling",
            attr.ib(
                type=ty.List[float],
                metadata={
                    "sep": ",",
                    "argstr": "-scaling",
                    "help_string": "specify the data scaling parameter",
                },
            ),
        ),
        (
            "export_grad",
            attr.ib(
                type=str,
                metadata={
                    "argstr": "-export_grad_mrtrix {export_grad}",
                    "help_string": "export gradient files in mrtrix3 format",
                },
            ),
        ),
        (
            "export_json",
            attr.ib(
                type=str,
                metadata={
                    "argstr": "-json_export {export_json}",
                    "help_string": "export image headet to JSON file",
                },
            ),
        ),
    ],
    bases=(MRTrix3BaseSpec,),
)

MRConvertOutputSpec = SpecInfo(
    name="MRConvertOutputs",
    fields=[
        (
            "out_bfile",
            attr.ib(
                type=File,
                metadata={
                    "help_string": "output .b gradient file in mrtrix3 format",
                    "output_file_template": "{export_grad}",
                },
            ),
        ),
        (
            "out_json",
            attr.ib(
                type=File,
                metadata={
                    "help_string": "output JSON file of image header",
                    "output_file_template": "{export_json}",
                },
            ),
        ),
    ],
    bases=(ShellOutSpec,),
)


class MRConvert(ShellCommandTask):
    """
    Example
    ------

    Convert NIfTI file with FSL-style gradient encoding files to
    MRtrix Image Format with MRtrix-style gradient encoding files

    >>> task = MRConvert()
    >>> task.inputs.in_file = "test_dwi.nii.gz"
    >>> task.inputs.grad_fsl = ["test.bvec", "test.bval"]
    >>> task.inputs.export_grad = "test.b"
    >>> task.inputs.out_file = "test.mif"
    >>> task.cmdline
    'mrconvert test_dwi.nii.gz -fslgrad test.bvec test.bval -export_grad_mrtrix test.b test.mif'

    Select the first volume from a diffusion-weighted dataset

    >>> task = MRConvert()
    >>> task.inputs.in_file = "test_dwi.nii.gz"
    >>> task.inputs.out_file = "test_vol.nii.gz"
    >>> task.inputs.coord = [3, 0]
    >>> task.cmdline
    'mrconvert test_dwi.nii.gz -coord 3 0 test_vol.nii.gz'

    Extend a 3D image to 4D by adding a singular dimension

    >>> task = MRConvert()
    >>> task.inputs.in_file = "test.nii.gz"
    >>> task.inputs.out_file = "test_set.nii.gz"
    >>> task.inputs.axes = [0, 1, 2, -1]
    >>> task.cmdline
    'mrconvert test.nii.gz -axes 0,1,2,-1 test_set.nii.gz'

    """

    input_spec = MRConvertInputSpec
    output_spec = MRConvertOutputSpec
    executable = "mrconvert"
