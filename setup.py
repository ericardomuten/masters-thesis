import setuptools

setuptools.setup(     
     name="masters_thesis_tools",     
     version="0.0.1",
     python_requires=">=3.10",
     install_requires=[
          'gurobipy==11.0.3',
      ],
     packages=["qaoa_tools", "qrr_tools"],
)