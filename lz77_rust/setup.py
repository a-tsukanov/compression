from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(
    name='lz77_rust',
    version='0.1.0',
    rust_extensions=[
        RustExtension('lz77_rust.lz77_rust', 'Cargo.toml', binding=Binding.PyO3),
    ],
    packages=['lz77_rust'],
    zip_safe=False,
)
