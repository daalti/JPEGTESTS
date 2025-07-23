import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg hs_letter_color_one_page *Hs_LTR_Color_1pg.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:Hs_LTR_Color_1pg.pwg=6ca956aa09ba67fc5cbf45117681e76bf5022d8bd825e558b85615805ecf3b44
    +name:test_pwg_hs_letter_color_one_page
    +test:
        +title:test_pwg_hs_letter_color_one_page
        +guid:a4efc8be-9239-41dd-adbc-ab33108d5a69
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_hs_letter_color_one_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6ca956aa09ba67fc5cbf45117681e76bf5022d8bd825e558b85615805ecf3b44')
    outputsaver.save_output()
