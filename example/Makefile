
# Copyright (c) 2020, Stanislav Zhelnio
# SPDX-License-Identifier: MIT

####################################################
# common targets

FILE_PNG = $(shell seq -f "%02g.png" 0 24) # 00.png..24.png
FILE_GIF = schoolRISCV.gif
TEMP_XML = temp.xml

all: venv $(FILE_PNG) $(FILE_GIF)

clean:
	rm -f $(TEMP_XML)
	rm -f $(FILE_PNG)
	rm -rf venv

# create python venv
venv:
	python3 -m venv venv
	. venv/bin/activate; \
	pip install pip --upgrade; \
	pip install git+https://github.com/zhelnio/drawio-layer#egg=drawio-layer

DRAWIO_SRC = schoolRISCV.drawio
DRAWIO_BIN = drawio
D_LAYER_PY = . venv/bin/activate && drawio-layer

# run draw.io gui
gui:
	$(DRAWIO_BIN) $(DRAWIO_SRC)

# create gif from png
$(FILE_GIF): $(FILE_PNG)
	convert -delay 150 -loop 0 $(FILE_PNG) $@

####################################################
# layer by layer image generation

LAYERS_00_0 = 0_border_wide 0_cpuState
LAYERS_00_1 = $(LAYERS_00_0) 0_DataMemory
LAYERS_01_0 = $(LAYERS_00_0) 1_ADDI_addr_shift_BLUE
LAYERS_02_0 = $(LAYERS_00_0) 1_ADDI_addr_shift
LAYERS_02_1 = $(LAYERS_02_0) 1_ADDI_instr 2_ADDI_decode_rs1_BLUE 2_ADDI_instr_rs1_BLUE
LAYERS_03_0 = $(LAYERS_02_0) 2_ADDI_decode_rs1
LAYERS_03_1 = $(LAYERS_03_0) 3_ADDI_instr_imm_BLUE 3_ADDI_decode_immI_BLUE
LAYERS_04_0 = $(LAYERS_03_0) 3_ADDI_decode_immI
LAYERS_04_1 = $(LAYERS_04_0) 4_ADDI_instr_opcode_BLUE 4_ADDI_ALU_BLUE 5_ADDI_stub_aluSrc_mux_BLUE
LAYERS_05_0 = $(LAYERS_04_0) 5_ADDI_stub_aluSrc_mux 4_ADDI_ALU
LAYERS_05_1 = $(LAYERS_05_0) 6_ADDI_decode_rd_BLUE 6_ADDI_instr_rd_BLUE
LAYERS_06_0 = $(LAYERS_05_0) 6_ADDI_decode_rd
LAYERS_06_1 = $(LAYERS_06_0) 4_ADDI_instr_opcode_BLUE 7_ADDI_regfile_write_BLUE 8_ADDI_stub_wdSrc_mux_BLUE
LAYERS_07_0 = $(LAYERS_06_0) 7_ADDI_regfile_write 8_ADDI_stub_wdSrc_mux
LAYERS_07_1 = $(LAYERS_07_0) 9_ADDI_pcPlus4_BLUE 10_ADDI_stub_pcSrc_mux_BLUE 9_ADDI_instr
LAYERS_08_0 = $(LAYERS_07_0) 9_ADDI_pcPlus4 10_ADDI_stub_pcSrc_mux
LAYERS_08_1 = $(LAYERS_08_0) 10_ADDI_instr_imm
LAYERS_09_1 = $(LAYERS_08_0) 11_ADD_instr
LAYERS_10_1 = $(LAYERS_08_0) 11_ADD_instr_rs_BLUE 11_ADD_decode_rs2_BLUE
LAYERS_11_0 = $(filter-out 5_ADDI_stub_aluSrc_mux, $(LAYERS_08_0)) 11_ADD_decode_rs2
LAYERS_11_1 = $(LAYERS_11_0) 12_ADD_aluSrc_mux_BLUE 12_ADD_instr_opcode_BLUE
LAYERS_12_0 = $(LAYERS_11_0) 12_ADD_aluSrc_mux
LAYERS_12_1 = $(LAYERS_12_0) 11_ADD_instr
LAYERS_13_0 = $(filter-out 8_ADDI_stub_wdSrc_mux, $(LAYERS_12_0))
LAYERS_13_1 = $(LAYERS_13_0) 13_LUI_immU_and_wdSrc_mux_BLUE 13_LUI_instr
LAYERS_14_0 = $(LAYERS_13_0) 13_LUI_immU_and_wdSrc_mux
LAYERS_14_1 = $(LAYERS_14_0) 14_BEQ_immB_and_pcBranch_BLUE 14_BEQ_instr_imm_BLUE
LAYERS_15_0 = $(filter-out 10_ADDI_stub_pcSrc_mux, $(LAYERS_14_0)) 14_BEQ_immB_and_pcBranch
LAYERS_15_1 = $(LAYERS_15_0) 15_BEQ_pcSrc_mux_BLUE 15_BEQ_instr_opcode_BLUE
LAYERS_16_0 = $(LAYERS_15_0) 15_BEQ_pcSrc_mux
LAYERS_16_1 = $(LAYERS_16_0) 16_BEQ_aluZero_and_branch_BLUE 17_BEQ_stub_condZero_BLUE 15_BEQ_instr_opcode_BLUE
LAYERS_17_0 = $(LAYERS_16_0) 16_BEQ_aluZero_and_branch 17_BEQ_stub_condZero
LAYERS_17_1 = $(LAYERS_17_0) 17_BEQ_instr
LAYERS_18_1 = $(LAYERS_17_0) 18_BNE_instr
LAYERS_19_0 = $(filter-out 17_BEQ_stub_condZero, $(LAYERS_17_0))
LAYERS_19_1 = $(LAYERS_19_0) 18_BNE_condZero_BLUE 18_BNE_instr_opcode_BLUE
LAYERS_20_0 = $(LAYERS_19_0) 18_BNE_condZero
LAYERS_20_1 = $(LAYERS_20_0) 19_CU_aluSrc_aluControl_BLUE
LAYERS_21_0 = $(LAYERS_20_0) 19_CU_aluSrc_aluControl
LAYERS_21_1 = $(LAYERS_21_0) 20_CU_decode_cmd_BLUE
LAYERS_22_1 = $(LAYERS_21_0) 20_CU_decode_cmd

$(TEMP_XML): $(DRAWIO_SRC)
	rm -f $(TEMP_XML)
	$(DRAWIO_BIN) --export --uncompressed --output $@ $(DRAWIO_SRC)

DRAWIO_OPT_PNG = --export --page-index 0 $(TEMP_XML)
DLAYER_OPT_PNG = $(TEMP_XML) --page-index 0 --action-type show_only

00.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_00_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

01.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_01_0)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

02.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_02_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

03.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_03_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

04.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_04_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

05.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_05_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

06.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_06_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

07.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_07_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

08.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_08_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

09.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_09_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

10.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_10_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

11.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_11_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

12.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_12_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

13.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_13_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

14.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_14_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

15.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_15_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

16.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_16_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

17.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_17_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

18.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_18_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

19.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_19_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

20.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_20_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

21.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_21_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

22.png: $(TEMP_XML)
	$(D_LAYER_PY) $(DLAYER_OPT_PNG) --name $(LAYERS_22_1)
	$(DRAWIO_BIN) $(DRAWIO_OPT_PNG) --output $@

# small delay for gif
23.png:
	cp 22.png $@

24.png:
	cp 22.png $@
