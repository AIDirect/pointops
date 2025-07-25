import os
from distutils.sysconfig import get_config_vars
from setuptools import setup

from torch.utils.cpp_extension import BuildExtension, CUDAExtension, CppExtension
import torch

(opt,) = get_config_vars("OPT")
os.environ["OPT"] = " ".join(
    flag for flag in opt.split() if flag != "-Wstrict-prototypes"
)

if torch.cuda.is_available():
    ext_modules = [
        CUDAExtension(
            name="pointops_cuda",
            sources=[
                "src/pointops_api.cpp",
                "src/knnquery/knnquery_cuda.cpp",
                "src/knnquery/knnquery_cuda_kernel.cu",
                "src/sampling/sampling_cuda.cpp",
                "src/sampling/sampling_cuda_kernel.cu",
                "src/grouping/grouping_cuda.cpp",
                "src/grouping/grouping_cuda_kernel.cu",
                "src/interpolation/interpolation_cuda.cpp",
                "src/interpolation/interpolation_cuda_kernel.cu",
                "src/subtraction/subtraction_cuda.cpp",
                "src/subtraction/subtraction_cuda_kernel.cu",
                "src/aggregation/aggregation_cuda.cpp",
                "src/aggregation/aggregation_cuda_kernel.cu",
            ],
            extra_compile_args={"cxx": ["-g"], "nvcc": ["-O2"]},
        )
    ]
else:
    ext_modules = [
        CppExtension(
            name="pointops_cpu",
            sources=[
                "src/pointops_api_cpu.cpp",
                "src/knnquery/knnquery_cpu.cpp",
                "src/sampling/sampling_cpu.cpp",
                "src/grouping/grouping_cpu.cpp",
                "src/interpolation/interpolation_cpu.cpp",
                "src/subtraction/subtraction_cpu.cpp",
                "src/aggregation/aggregation_cpu.cpp",
            ],
            extra_compile_args={"cxx": ["-g"]},
        )
    ]

setup(
    name="pointops",
    author="Hengshuang Zhao",
    ext_modules=ext_modules,
    cmdclass={"build_ext": BuildExtension},
)
