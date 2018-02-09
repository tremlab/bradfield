# Write	a	"virtual	computer"	function	that	takes	as	input	a	reference	to	main	memory	(an	array	of	20bytes),	executes	the	stored	program	by	fetching	and	decoding	each	instruction	until	it	reacheshalt,	then	returns.	This	function	shouldn't	return	anything,	but	should	have	the	side-effect	of mutating	"main	memory"

# values in hexidecimal as string.



# counter - will only be incremented by 1
reg_pc = 0

#  2 data registers.  Info will be stored as an array of len - 2.
# [0] holds the smaller, modulo after dividing the 'whole' number by 256.
# [1] holds the int value of diving the 'whole' number by 256 (always round down).
#  ****** BOTH are stored as hexidecimal STRINGS ******

# input, also where output is stored
reg_a = [0,0]
# input only
reg_b = [0,0]



#  ***********************************
#  factored away the complex steps of extracting and updating data on the reg's.
#  lots of type and formatting stuff, unintersting to the underlying math that needs to be done.

def get_dec_reg_a():
    """takes the 2 str hex values saved in reg and parses them into their intended decimal int value.
    """
    return int(reg_a[0], 16) + (int(reg_a[1], 16)  * 256)


def get_dec_reg_b():
    return int(reg_b[0], 16) + (int(reg_b[1], 16)  * 256)


def set_hex_reg_a(dec_num):
    """takes a decimal int, splits it into 2 components (remainder after / 256, value of / 256), and the converts each of those to hex int, and finally turns each into a string and stores them in the reg.
    """
    # the built in hex() adds a "0x" to all its outputs, which interferes with how I'm handling the strings/values in this file.
    hex_0 = str(hex(int(dec_num % 256))).strip("0x")
    hex_1 = str(hex(int(dec_num / 256))).strip("0x")
    reg_a[0] = hex_0
    reg_a[1] = hex_1


def set_hex_reg_b(dec_num):
    hex_0 = str(hex(int(dec_num % 256))).strip("0x")
    hex_1 = str(hex(int(dec_num / 256))).strip("0x")
    reg_b[0] = hex_0
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

    new_sum = val1 + val2

    if reg1 == "01":
        set_hex_reg_a(new_sum)
    else:
        set_hex_reg_b(new_sum)


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

    print(int(main_mem[14], 16) + (int(main_mem[15], 16)  * 256))


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
        "04",  # 6
        "01",  # 7
        "02",  # 8
        "02",  # 9
        "01",  # 10
        "0e",  # 11
        "FF",  # 12
        "00",  # 13
        "00",  # 14
        "00",  # 15
        "00",  # 16
        "10",  # 17
        "a1",  # 18
        "14",  # 19
    ]

    main()


        # load_word	$a	(10h)	  #	Load	input	1	into	register	a
        # load_word	$b	(12h)	  #	Load	input	2	into	registerb
        # add	$a	$b	              #	Add	the	two	registers,	store	the	result	in	register	a
        # store_word	$a	(0Eh)	  #	Store	thevalue	in	register	a	to	the output device
        # halt
