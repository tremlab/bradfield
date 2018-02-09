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
        val1 = int(reg_a[0]) + int(reg_a[1])
    else:
        val1 = int(reg_b[0]) + int(reg_b[1])

    if reg2 == "01":
        val2 = int(reg_a[0]) + int(reg_a[1])
    else:
        val2 = int(reg_b[0]) + int(reg_b[1])

    new_sum = val1 + val2

    if reg1 == "01":
        reg_a = str(new_sum)
    else:
        reg_b = str(new_sum)


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
        main_mem[int(loc, 16)] = reg_a
    else:
        main_mem[int(loc, 16)] = reg_b


def halt():
    global main_mem

    print(main_mem[14])




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
        "03",  # 16
        "01",  # 17
        "05",  # 18
        "10",  # 19
    ]
    status = True

    while(status):
        status = cycle()

        # load_word	$a	(10h)	  #	Load	input	1	into	register	a
        # load_word	$b	(12h)	  #	Load	input	2	into	registerb
        # add	$a	$b	              #	Add	the	two	registers,	store	the	result	in	register	a
        # store_word	$a	(0Eh)	  #	Store	thevalue	in	register	a	to	the output device
        # halt
