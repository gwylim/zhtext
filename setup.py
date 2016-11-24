from setuptools import setup

setup(name='zhtext',
      version='0.1',
      description='Chinese text processing tools',
      url='http://github.com/gwylim/zhtext',
      author='Gwylim Ashley',
      author_email='gwylim.a@gmail.com',
      license='MIT',
      packages=['zhtext'],
      scripts=['bin/zhsegment'],
      zip_safe=False,
      data_files=[('zhtext/data', ['zhtext/data/cedict_1_0_ts_utf-8_mdbg.txt'])])
