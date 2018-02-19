# Write	a	"virtual	computer"	function	that	takes	as	input	a	reference	to	main	memory	(an	array	of	20bytes),	executes	the	stored	program	by	fetching	and	decoding	each	instruction	until	it	reacheshalt,	then	returns.	This	function	shouldn't	return	anything,	but	should	have	the	side-effect	of mutating	"main	memory"

# values in hexidecimal as string.

# counter - will only be incremented by 1
reg_pc = 0

#  2 data registers.  Info will be stored as an array of len - 2.
# [0] holds the smaller, modulo after dividing the 'whole' number by 256.
# [1] holds the int value of diving the 'whole' number by 256 (always round down).
#  ****** BOTH are stored as hexidecimal STRINGS ******

reg_a = [0,0]
reg_b = [0,0]


#  ***********************************
#  factored away the complex steps of extracting and updating data on the reg's.
#  lots of type and formatting stuff, unintersting to the underlying math that needs to be done.

def get_dec_reg_a():
    """takes the 2 str hex values saved in reg_a and parses them into their intended decimal int value.
    """
    #  how is negative reflected in this two-part bigger nubmer?????
    # I think logically either both parts are positove, or both are negative. ?
    hex_0 = int(reg_a[0], 16) # converts 2 char string to hex type num for python
    dec_0 = -(hex_0 & 0x80) | (hex_0 & 0x7f) # checks if negative two's complement

    hex_1 = int(reg_a[1], 16)
    dec_1 = -(hex_1 & 0x80) | (hex_1 & 0x7f)
    return dec_0 + (dec_1 * 256)


def get_dec_reg_b():
    hex_0 = int(reg_b[0], 16) # converts 2 char string to hex type num for python
    dec_0 = -(hex_0 & 0x80) | (hex_0 & 0x7f)

    hex_1 = int(reg_b[1], 16)
    dec_1 = -(hex_1 & 0x80) | (hex_1 & 0x7f)
    return dec_0 + (dec_1 * 256)


def set_hex_reg_a(dec_num):
    """takes a decimal int, splits it into 2 components (remainder after / 256, value of / 256), and the converts each of those to hex int, and finally turns each into a string and stores them in the reg.
    """
    # two's complement????

    dec_0 = dec_num % 256
    hex_0 = hex(dec_0 & -(2**8-1))
    # dec_print = -(hex_0 & 0x80) | (hex_0 & 0x7f)
    print("set hex", hex_0)
    reg_a[0] = hex_0

    # DRY!!!!!!!!  :(
    dec_1 = int(dec_num / 256) # no floats, round down
    hex_1 = hex(dec_1 & -(2**8-1))
    reg_a[1] = hex_1

# #  input needs to be formatted by: s8(int(g, 16))  turns str hex into usable num
# def s8(value):
#     """will translate 8 bit hex into decimal, INCLUDING an evaluation if negative, using two's complement. input cannot be string, must have "0x" preceding hex digits.
#     """
#     return -(value & 0x80) | (value & 0x7f)﻿


def set_hex_reg_b(dec_num):
    hex_0 = str(hex(int(dec_num % 256))).strip("0x")

    if len(hex_0) == 1:
        hex_0 = "0" + hex_0
    if hex_0 == "":
        print("whaaat?")
    reg_b[0] = hex_0

    # DRY!!!!!!!!  :(
    hex_1 = str(hex(int(dec_num / 256))).strip("0x")
    if len(hex_1) == 1:
        hex_1 = "0" + hex_1
    if hex_1 == "":
        print("whaaat?")
    reg_b[1] = hex_1
#  ***********************************


def add_regs(reg1, reg2):
    global reg_a
    global reg_b

    if reg1 == "01":
        val1 = get_dec_reg_a()
    else:
        val1 = get_dec_reg_b()

    if reg2 == "01":
        val2 = get_dec_reg_a()
    else:
        val2 = get_dec_reg_b()

    print(val1, val2)
    new_sum = val1 + val2

    if reg1 == "01":
        set_hex_reg_a(new_sum)
    else:
        set_hex_reg_b(new_sum)

    print(new_sum)
    print(reg_a)
    print(reg_b)


def sub_regs(reg1, reg2):
    global reg_a
    global reg_b

    if reg1 == "01":
        val1 = get_dec_reg_a()
    else:
        val1 = get_dec_reg_b()

    if reg2 == "01":
        val2 = get_dec_reg_a()
    else:
        val2 = get_dec_reg_b()

    diff = val1 - val2

    if reg1 == "01":
        set_hex_reg_a(diff)
    else:
        set_hex_reg_b(diff)

    print(diff)


def load(reg, loc):
    global reg_a
    global reg_b
    global main_mem

    if reg == "01":
        reg_a[0] = main_mem[int(loc, 16)]
        reg_a[1] = main_mem[int(loc, 16) + 1]
    else:
        reg_b[0] = main_mem[int(loc, 16)]
        reg_b[1] = main_mem[int(loc, 16) + 1]


def store(reg, loc):
    global reg_a
    global reg_b
    global main_mem

    if reg == "01":
        main_mem[int(loc, 16)] = reg_a[0]
        main_mem[int(loc, 16) + 1] = reg_a[1]
    else:
        main_mem[int(loc, 16)] = reg_b


def halt():
    global main_mem

    hex_0 = int(main_mem[0], 16) # converts 2 char string to hex type num for python
    dec_0 = -(hex_0 & 0x80) | (hex_0 & 0x7f)

    hex_1 = int(main_mem[1], 16)
    dec_1 = -(hex_1 & 0x80) | (hex_1 & 0x7f)
    print(dec_0 + (dec_1 * 256))


def cycle():
    global reg_pc
    global main_mem

    indx =  reg_pc * 3
    instr = main_mem[indx]

    if instr == "01":
        print("loading")
        load(main_mem[indx+1], main_mem[indx+2])
    elif instr == "02":
        print("storing")
        store(main_mem[indx+1], main_mem[indx+2])
    elif instr == "03":
        print("adding")
        add_regs(main_mem[indx+1], main_mem[indx+2])
    elif instr == "04":
        print("subtracting")
        sub_regs(main_mem[indx+1], main_mem[indx+2])
    elif instr == "FF":
        print("stopping")
        halt()
        return False

    reg_pc += 1

    return True


def main():
    status = True

    while(status):
        status = cycle()

if __name__ == '__main__':

    main_mem = [
        "01", # 0
        "01", # 1
        "10",  # 2
        "01",  # 3
        "02",  # 4
        "12",  # 5
        "03",  # 6
        "01",  # 7
        "02",  # 8
        "02",  # 9
        "01",  # 10
        "0e",  # 11
        "FF",  # 12
        "00",  # 13
        "00",  # 14
        "00",  # 15
        "01",  # 16
        "00",  # 17
        "00",  # 18
        "FF",  # 19
    ]

    # main()


        # load_word	$a	(10h)	  #	Load	input	1	into	register	a
        # load_word	$b	(12h)	  #	Load	input	2	into	registerb
        # add	$a	$b	              #	Add	the	two	registers,	store	the	result	in	register	a
        # store_word	$a	(0Eh)	  #	Store	thevalue	in	register	a	to	the output device
        # halt
