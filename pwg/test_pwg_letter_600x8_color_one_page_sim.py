import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg letter 600X8 color one page from *letter-600x8-color-1p-sim.pwg
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:letter-600x8-color-1p-sim.pwg=acd1927984e9ed031fc4dac26cbd29112725a05e235b263aa31abdb2465c488c
    +name:test_pwg_letter_600X8_color_one_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_letter_600X8_color_one_page
        +guid:403d57f9-b570-4588-8643-da6181da05f6
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_letter_600X8_color_one_page(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('acd1927984e9ed031fc4dac26cbd29112725a05e235b263aa31abdb2465c488c')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    logging.info("PWG letter 600X8 color one page completed successfully")
