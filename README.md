# Palette packing implementation using Python

During the first semester of my [MSc Advanced Computer Science](https://www.keele.ac.uk/pgtcourses/advancedcomputersciencemsc/) degree, I took a module called System Design and Programming.

Outcomes of this module included:

- Developed an understanding of the requirements gathering process
- Introduced to systems design concepts such as use cases/sequence diagrams/class diagrams
- Created basic UML diagrams
- Introduced to programming fundamentals using Python

For the Python aspect of the module, we were tasked with producing a palette packing program. This document details the requirements and objectives of the program. In the repository, you will find the files used to run the program as well as the full program (given in Python 2.7 and Python 3).

- [Specification](#specification)
- [Usage](#usage)
- [Example](#example)

## Specification

You will be given the following files:

**`products.csv`**

Code | Pack Qty | Length | Width | Description
---- | -------- | ------ | ----- | -------------------
AA1  | 100      | 220    | 120   | Sliced White Single
AA2  | 100      | 440    | 440   | Sliced White x4
BA1  | 100      | 200    | 200   | Bap White x4
BA5  | 100      | 800    | 800   | Bap White x32
BB1  | 100      | 200    | 200   | Bap Brown x8
PM1  | 100      | 300    | 300   | Pizza Margherita

**`order.csv`**

Code | Order Qty | Warehouse
---- | --------- | ---------
AA1  | 60        | W1
AA2  | 60        | W1
BA1  | 60        | W1
BA5  | 60        | W1
BB1  | 60        | W1
PM1  | 60        | W1

--------------------------------------------------------------------------------

**Produce a program that will read the order file and produce files that detail the packing strategy according to the following requirements .**

- After packaging, product packs (which may have more than one physical product) are placed onto standard height palettes which accomodate the `full pack height` (in a single layer - palettes can accomodate content upto `200mm height`, all packs are exactly this height)

- Product packs vary however, in both length and width.

- Palettes are assembled into `stacks` with `7 palettes per stack`

- These `stacks` are loaded into standardised vans for delivery, which can accomodate `6 palette stacks`

## Usage

In order to run the program on your own machine, Python 2.7 or Python 3 needs to be installed.<br>
Downloading the repository to your own machine and running `packing_program.py` will produce the required files.<br>

The result should be the following:

1. Separate palette files e.g `palette_stack_1.csv` upto how many were required, this details the contents of each palette
2. Full order file e.g. `full_order.csv` showing each product along with its quantity, palette number and stack number
3. Analysis file e.g. `analysis.txt` showing how much length/width was used for each palette individually and collectively

## Example

Input files

**`products.csv`**

Code | Pack Qty | Length | Width | Description
---- | -------- | ------ | ----- | -------------------
AA1  | 100      | 220    | 120   | Sliced White Single
AA2  | 100      | 440    | 440   | Sliced White x4
BA1  | 100      | 200    | 200   | Bap White x4
BA5  | 100      | 800    | 800   | Bap White x32
BB1  | 100      | 200    | 200   | Bap Brown x8
PM1  | 100      | 300    | 300   | Pizza Margherita

-------------------------------------------------------------

**`order.csv`**

Code | Order Qty | Warehouse
---- | --------- | ---------
AA1  | 60        | W1
AA2  | 60        | W1
BA1  | 60        | W1
BA5  | 60        | W1
BB1  | 60        | W1
PM1  | 60        | W1

-------------------------------------------------------------


**Running `packing_program.py` will produce the following.**

-------------------------------------------------------------------------

**Separate palette files**

**`palette_stack_1.csv`**

Palette Number | Product Code | Product Quantity
-------------- | ------------ | ----------------
1              | AA1          | 9
2              | AA1          | 9
3              | AA1          | 9
4              | AA1          | 9
5              | AA1          | 9
6              | AA1          | 9
7              | AA2          | 4

-------------------------------------------------------------


**`palette_stack_2.csv`**

Palette Number | Product Code | Product Quantity
-------------- | ------------ | ----------------
1              | AA2          | 4
2              | AA2          | 4
3              | AA2          | 4
4              | AA2          | 4
5              | AA2          | 4
6              | AA2          | 4
7              | AA2          | 4

-------------------------------------------------------------

**`palette_stack_3.csv`**

Palette Number | Product Code | Product Quantity
-------------- | ------------ | ----------------
1              | AA2          | 4
2              | AA2          | 4
3              | AA2          | 4
4              | AA2          | 4
5              | AA2          | 4
6              | AA2          | 4
7              | BA1          | 3
8              | AA2          | 3

-------------------------------------------------------------

**`palette_stack_4.csv`**

Palette Number | Product Code | Product Quantity
-------------- | ------------ | ----------------
1              | BA1          | 2
2              | AA2          | 3
3              | BA1          | 6
4              | BA1          | 6
5              | BA1          | 6
6              | BA1          | 6
7              | BA1          | 6
8              | BA1          | 6

-------------------------------------------------------------

**`palette_stack_5.csv`**

Palette Number | Product Code | Product Quantity
-------------- | ------------ | ----------------
1              | BA1          | 6
2              | BA1          | 6
3              | BA1          | 6
4              | BA5          | 2
5              | BA1          | 4
6              | BA5          | 6
7              | BA5          | 3
8              | BA5          | 3

-------------------------------------------------------------

**`palette_stack_6.csv`**

Palette Number | Product Code | Product Quantity
-------------- | ------------ | ----------------
1              | BA5          | 3
2              | BA5          | 3
3              | BA5          | 3
4              | BA5          | 3
5              | BA5          | 3
6              | BA5          | 3
7              | BA5          | 3

--------------------------------------------------------------------------------

**Full order file**

**`full_order.csv`**

Stack Number | Palette Number | Product Code | Product Quantity
------------ | -------------- | ------------ | ----------------
1            | 1              | AA1          | 9
1            | 2              | AA1          | 9
1            | 3              | AA1          | 9
1            | 4              | AA1          | 9
1            | 5              | AA1          | 9
1            | 6              | AA1          | 9
1            | 7              | AA2          | 4
2            | 1              | AA2          | 4
2            | 2              | AA2          | 4
2            | 3              | AA2          | 4
2            | 4              | AA2          | 4
2            | 5              | AA2          | 4
2            | 6              | AA2          | 4
2            | 7              | AA2          | 4
3            | 1              | AA2          | 4
3            | 2              | AA2          | 4
3            | 3              | AA2          | 4
3            | 4              | AA2          | 4
3            | 5              | AA2          | 4
3            | 6              | AA2          | 4
3            | 7              | BA1          | 3
3            | 7              | AA2          | 3
4            | 1              | BA1          | 2
4            | 1              | AA2          | 3
4            | 2              | BA1          | 6
4            | 3              | BA1          | 6
4            | 4              | BA1          | 6
4            | 5              | BA1          | 6
4            | 6              | BA1          | 6
4            | 7              | BA1          | 6
5            | 1              | BA1          | 6
5            | 2              | BA1          | 6
5            | 3              | BA1          | 6
5            | 4              | BA5          | 2
5            | 4              | BA1          | 4
5            | 5              | BA5          | 6
5            | 6              | BA5          | 3
5            | 7              | BA5          | 3
6            | 1              | BA5          | 3
6            | 2              | BA5          | 3
6            | 3              | BA5          | 3
6            | 4              | BA5          | 3
6            | 5              | BA5          | 3
6            | 6              | BA5          | 3
6            | 7              | BA5          | 3

--------------------------------------------------------------------------------

**Analysis file**

**`analysis.txt`**

Total order length used is 86.6183333333%<br>
Total order width used is 81.27%

Palette stack 1 used 97.43% of the total length<br>
Palette stack 1 used 88.57% of the total width

Palette stack 2 used 88.0% of the total length<br>
Palette stack 2 used 80.0% of the total width

Palette stack 3 used 89.14% of the total length<br>
Palette stack 3 used 84.29% of the total width

Palette stack 4 used 63.71% of the total length<br>
Palette stack 4 used 99.05% of the total width

Palette stack 5 used 91.43% of the total length<br>
Palette stack 5 used 85.71% of the total width

Palette stack 6 used 90.0% of the total length<br>
Palette stack 6 used 50.0% of the total width

-------------------------------------------------------------

**NOTE**

This was my my first experience of programming (outside of self taught HTML/CSS/Javascript), therefore does not represent my current skill level.

Since the time of this project, I have improved massively and gained much more experience (and hours programming).

Other repositories will give a better reflection of where I am currently at. I'm aware that the program is highly inefficient and would have been much better if it utilised an object oriented approach, however at the time this was beyond my capabilities. I preceded to complete the program using a procedural approach (since it was the only way I knew how).
