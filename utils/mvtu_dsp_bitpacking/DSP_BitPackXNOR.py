import copy

def main():
	seperator = "==========================================================="
	# Read MVTU to be converted
	file = open( "Matrix_Vector_Activa_2.vhd", "r" )
	lines = file.readlines()
	file.close()
	fileout = open("Matrix_Vector_Activa_2_out.vhd", "w+")

	lines_out = copy.deepcopy(lines)

	sig_assignments = []
    # Set original signal group name to reroute through DSPs
	org_sigs = ["weights3_m_weights_V_q0"]
    # Set PE count and SIMD of the MVTU
	PE_count = 4
	SIMD_count = 32
	dsp_id = 0
	dsp_ptr = 0
	dsp_max = 48
	AB_concat = []
	C = []
	P = []

	inst_dsp_comp = []
	inst_ABCP = []

	i = 1

	while True and PE_count > 1:
        # Set original signal group name to reroute through DSPs
		org_sigs.append("weights3_m_weights_V_" + str(i) + "_q0")
		i += 1
		if i == PE_count:
			break


	for org_sig in org_sigs:
		for line_1 in lines:
			if line_1.find(org_sig)!= -1 and line_1.find("STD_LOGIC_VECTOR") == -1:
				line_1_s = line_1.strip()
				line_sig1 = line_1_s.split(" <= ")
				AB_concat.append("AB_concat_" + str(dsp_id) + "(" + str(dsp_ptr) + " downto " + str(dsp_ptr) + ") <= " + line_sig1[0] + ";")
				for line_2 in lines:
					if line_2.find(line_sig1[0]) != -1 and line_2.find("STD_LOGIC_VECTOR") == -1  and line_2.strip() != line_1_s:
						line_2_s = line_2.strip()
						line_sig2 = line_2_s.split(" <= ")
						line_sig2_ifmap = line_sig2[1].replace(";","").replace(")","").replace("(","").split(" xor ")
						for tmp_sig in line_sig2_ifmap:
							if tmp_sig != line_sig1[0]:
								C.append("C_" + str(dsp_id) + "(" + str(dsp_ptr) + " downto " + str(dsp_ptr) + ") <= " + tmp_sig + ";")
						for lout in lines_out:
							if lout == line_2:
								lines_out.remove(lout)
								break
						break
				for line_3 in lines:
					if line_3.find(line_sig2[0]) != -1 and line_3.find("STD_LOGIC_VECTOR") == -1  and line_3.strip() != line_2_s:
						line_3_s = line_3.strip()
						line_sig3 = line_3_s.split(" <= ")
						for lout in lines_out:
							if lout == line_3:
								lines_out.remove(lout)
								break
						break
				for line_4 in lines:
					if line_4.find(line_sig3[0]) != -1 and line_4.find("STD_LOGIC_VECTOR") == -1  and line_4.strip() != line_3_s :
						line_4_s = line_4.strip()
						line_sig4 = line_4_s.split(" <= ")
						for lout in lines_out:
							if lout == line_4:
								lines_out.remove(lout)
								break
						P.append(line_sig4[0] + " <= P_" + str(dsp_id) + "(" + str(dsp_ptr) + " downto " + str(dsp_ptr) + ");")
						dsp_ptr += 1
						if dsp_ptr == dsp_max:
							inst_dsp_comp, inst_ABCP = inst_newdsp(dsp_id, inst_dsp_comp, inst_ABCP)
							dsp_id += 1
							dsp_ptr = 0
						
	# for the last DSP
	inst_dsp_comp, inst_ABCP = inst_newdsp(dsp_id, inst_dsp_comp, inst_ABCP)

	print(seperator)
	print("SIGNALS Created")
	print(seperator)
	for i in inst_ABCP:
		print(i)

	print(seperator)
	print("DSPs Instantiated")
	print(seperator)
	for i in inst_dsp_comp:
		print(i)

	print(seperator)
	print("Assignments and re-wiring through DSPs")
	print(seperator)
	for i in AB_concat:
		print(i)
	for i in C:
		print(i)
	for i in P:
		print(i)

	for i in lines_out:
		if i.find("use IEEE.numeric_std.all;") != -1:
			fileout.write(i)
			fileout.write("library xil_defaultlib;" + "\n")
		elif i.find("end component;") != -1:
			fileout.write(i)
			for j in inst_ABCP:
				fileout.write(j + "\n")
		elif i.find(": component") != -1:
			for j in inst_dsp_comp:
				fileout.write(j + "\n")
			for j in AB_concat:
				fileout.write(j + "\n")
			for j in C:
				fileout.write(j + "\n")
			for j in P:
				fileout.write(j + "\n")
			fileout.write(i)
		else:
			fileout.write(i)


	fileout.close()

def inst_newdsp(dsp_id, inst_dsp_comp, inst_ABCP):
	inst_dsp_comp.append("DSP48E1_PE" + str(dsp_id) + ": entity xil_defaultlib.DSP48E1_MOD")
	inst_dsp_comp.append("port map(")
	inst_dsp_comp.append("clk => '1',")
	inst_dsp_comp.append("A => AB_concat_" + str(dsp_id) + "(47 downto 18),")
	inst_dsp_comp.append("B => AB_concat_" + str(dsp_id) + "(17 downto 0),")
	inst_dsp_comp.append("C => C_" + str(dsp_id) + ",")
	inst_dsp_comp.append("P => P_" + str(dsp_id))
	inst_dsp_comp.append(");")

	inst_ABCP.append("signal AB_concat_" + str(dsp_id) + " : STD_LOGIC_VECTOR (47 downto 0);")
	inst_ABCP.append("signal C_" + str(dsp_id) + " : STD_LOGIC_VECTOR (47 downto 0);")
	inst_ABCP.append("signal P_" + str(dsp_id) + " : STD_LOGIC_VECTOR (47 downto 0);")

	return inst_dsp_comp, inst_ABCP

main()
