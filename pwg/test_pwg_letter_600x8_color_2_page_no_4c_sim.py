import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg letter 600x8 color two page no 4C sim from *letter-600x8-color-2pNO4c-sim.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:letter-600x8-color-2pNO4c-sim.pwg=63ac052df55d1e361b86d1aa21a06d21300d0c7c60792ff9c62198ec876a14c2
    +name:test_pwg_letter_600x8_color_two_page_no_4c_sim
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_letter_600x8_color_two_page_no_4c_sim
        +guid:a0e685e1-7e80-4738-9838-fab917418ca0
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
    +overrides:
        +Home:
            +is_manual:False
            +timeout:360
            +test:
                +dut:
                    +type:Engine

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_letter_600x8_color_two_page_no_4c_sim(setup_teardown, printjob,udw,outputsaver):
    outputsaver.validate_crc_tiff(udw)

    printjob.print_verify('63ac052df55d1e361b86d1aa21a06d21300d0c7c60792ff9c62198ec876a14c2')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    logging.info("PWG Letter 600x8 Color Two No4C Sim Page  - Print job completed successfully")
