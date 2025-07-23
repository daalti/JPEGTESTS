import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg letter 600x8 color four page no duplex from *letter-600x8-color-4p-Nodup.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:letter-600x8-color-4p-NOdup.pwg=76ff895686c9302d166a9e19b9d17ff281a384a4560cdf41d43c7a026a905c0c
    +name:test_pwg_letter_600x8_color_four_page_no_duplex
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_letter_600x8_color_four_page_no_duplex
        +guid:b067b3f4-d782-4af2-bdbf-8634722b321b
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
def test_pwg_letter_600x8_color_four_page_no_duplex(setup_teardown, printjob,udw,outputsaver):
    outputsaver.validate_crc_tiff(udw)

    printjob.print_verify('76ff895686c9302d166a9e19b9d17ff281a384a4560cdf41d43c7a026a905c0c')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

    logging.info("PWG Letter 600x8 Color Four Page No Duplex - Print job completed successfully!")
