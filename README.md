# afl-test-viz
*A project on visualizing tests generated in AFL during fuzzing.*

Current Release: [v1.0](https://github.com/AftabHussain/afl-test-viz/releases/tag/v1.0)

## Overview
In this work, we provide a way to visualize tests that are generated during fuzzing by AFL, at the byte-level. The visualization helps us see which bytes of the testcase AFL is performing mutations upon. 

## Components

1. **Testcase byte code generator** - This component captures the byte stream representation of tests generated by AFL through mutation and saves them in a single file (`tests_generated`) as hex code. This file is generated in the AFL output folder. Each line of this file corresponds to the byte representation of a single test case. It is implemented as a patch in AFL (`afl-fuzz.c`). The patch is provided below which is added in the `common_fuzz_stuff` function, right before the line where `write_to_testcase` is invoked.:

```
  u8* fn = alloc_printf("%s/tests_generated", out_dir);
  FILE* f = fopen(fn, "a");

  ck_free(fn);

  // Write the test cases in bytes.
  for (int i=0; i<len; i++) {
    fprintf(f, "%02x ", out_buf[i]);
  }
  
  fprintf(f,"\n");
  fclose(f);
```

This patch has been added to a forked version of AFL [here](https://github.com/AftabHussain/AFL/commit/6524a627a0bd13544d393e0215cdf98668eaaec4).

2. **Testcase image generator** -  This component reads the file generated by the byte code generator, and generates an image file (in `png` format) for each test case. In an image, each box represents a byte of a test case. The colors of the boxes are obtained from the hex value of each byte of the input test in the following way: if a byte is, say, `7c`, then the hex color code is `#7c0000`. The implementation is in `viz_tests.py`, provided in the `code` folder.

## Sample image representation of a testcase
![sample-test-image](https://github.com/AftabHussain/afl-test-viz/blob/main/figs/test-bytes.png)

## Usage
Instructions to fuzz libxml2 using the visualization tool are provided below.

### Environment Setup

**The visualization tool**

In any directory, clone the repository:

```git clone --recursive git@github.com:AftabHussain/afl-test-viz.git```

Build and install AFL, patched with the tool’s Test Input
Color Representation Generator component, as shown below:

```cd afl-test-viz/code/AFL-mut-viz/AFL && make -j32 && make install```

**libxml2**

Build the test subject (libxml2) with AFL’s
compiler (```afl-gcc```), which prepares libxml2 binaries as fuzzing targets. 

Get libxml2 as follows in a folder outside ```afl-test-viz``` directory:

```git clone https://github.com/GNOME/libxml2.git && cd libxml2 && git checkout 1fbcf40```

Configure and build libxml2:

```cd libxml2 && export CC=afl-gcc && ./autogen.sh && make -j32```

### Generate Color Representations of Test Inputs

Invoke the first part of the visualization tool, the augmented AFL fuzzer, which pro-
duces hex color representations of test inputs generated while fuzzing the
test subject. Here, we fuzz ```xmllint``` binary from the libxml2 library. 

Enter the libxml2 folder, create an input folder (input), and place in it any XML file
as a test input:

```cd libxml2 && mkdir input && cp [path_to_xml_file] input/```

Then start fuzzing:

```export AFL_SKIP_CPUFREQ=1 && export LD_LIBRARY_PATH=./.libs/ && afl-fuzz -i input/ -o output/ -- ./.libs/xmllint -o /dev/null @@```

Terminate fuzzing anytime using Ctrl+C – on termination,
all results are saved in the output folder, output. ```tests_generated``` contains color representations of all the tests created
by the fuzzer.

### Generate Images from Color Representations of Test Inputs

Process the color dump file (```tests_generated```). Place this file along with the Image Generation program
(```code/viz_tests.py```) in a separate directory:

```
mkdir process color rep
cp libxml2/output/tests generated process_color_rep
cp afl test viz/code/viz tests.py process_color_rep
```

Generate the images:

```cd process_color_rep/ && python viz_tests.py```

PNG images for all tests that are represented in
the color dump file are now in ```process_color_rep``` directory:

```
ls | xargs -n 1
.
.
.
file_000005564.png
file_000005565.png
file_000005566.png
file_000005567.png
file_000005568.png
file_000005569.png
file_000005570.png
file_000005571.png
file_000005572.png
.
.
```

The naming of the input files corresponds to the order in which their corresponding test inputs were generated during
fuzzing. To produce a time-lapse video of the images, we use [Simple Screen Recorder](https://www.maartenbaert.be/simplescreenrecorder/), 
which can be invoked by the command
```simplescreenrecorder``` on the terminal. (You may start recording using it, and toggle over multiple images on Image Viewer 
by holding the left/right arrow key to capture mutation transitions.)

