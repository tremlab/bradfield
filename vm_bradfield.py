# Write	a	"virtual	computer"	function	that	takes	as	input	a	reference	to	main	memory	(an	array	of	20bytes),	executes	the	stored	program	by	fetching	and	decoding	each	instruction	until	it	reacheshalt,	then	returns.	This	function	shouldn't	return	anything,	but	should	have	the	side-effect	of mutating	"main	memory"

# values in hexidecimal



# counter
reg_pc = 0
# input, also where output is stored
reg_a = [0,0]
# input only
reg_b = [0,0]


def add_regs(reg1, reg2):
    global reg_a
    global reg_b

    if reg1 == "01":
        val1 = int(reg_a[0], 16) + (int(reg_a[1], 16)  * 256)
    else:
        val1 = int(reg_b[0], 16) + (int(reg_a[1], 16)  * 256)

    if reg2 == "01":
        val2 = int(reg_a[0], 16) + (int(reg_b[1], 16)  * 256)
    else:
        val2 = int(reg_b[0], 16) + (int(reg_b[1], 16)  * 256)

    new_sum = val1 + val2
    hex_0 = str(hex(int(new_sum % 256))).strip("0x")
    hex_1 = str(hex(int(new_sum / 256))).strip("0x")

    if reg1 == "01":
        reg_a[0] = hex_0
        reg_a[1] = hex_1
    else:
        reg_b[0] = hex_0
        reg_b[1] = hex_1


def sub_regs():
    pass


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
        pass
    elif instr == "FF":
        print("stopping")
        halt()
        return False

    reg_pc += 1

    return True



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
        "a1",  # 18
        "14",  # 19
    ]
    status = True

    while(status):
        status = cycle()

        # load_word	$a	(10h)	  #	Load	input	1	into	register	a
        # load_word	$b	(12h)	  #	Load	input	2	into	registerb
        # add	$a	$b	              #	Add	the	two	registers,	store	the	result	in	register	a
        # store_word	$a	(0Eh)	  #	Store	thevalue	in	register	a	to	the output device
        # halt
