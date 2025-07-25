import pytest
import logging
from dunetuf.print.output.intents import Intents

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print HPGL2 job with margins set as oversize and verify CRC
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-191744
    +timeout:120
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:a3_margins_oversize_hpgl2.prn=fe1040fdc23775cb90bb56833789b5160dd96b6ef12529b8d24599a3f83aeaf5
    +test_classification:System
    +name:test_hpgl2_margins_oversize
    +test:
        +title:test_hpgl2_margins_oversize
        +guid:c6ce35b5-6304-4985-974f-d1553cf8d827
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=HPGL2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_hpgl2_margins_oversize(setup_teardown, printjob, outputverifier):
    
    logging.info('Running test_hpgl2_margins_oversize')

    outputverifier.outputsaver.operation_mode('CRC')
    printjob.print_verify('fe1040fdc23775cb90bb56833789b5160dd96b6ef12529b8d24599a3f83aeaf5', 'SUCCESS', 300, 1)
    logging.info("a3_margins_oversize_hpgl2.prn - Print job completed successfully")

    ### VERIFY
    if outputverifier.outputsaver.configuration.productname == "jupiter":
        expected_crc = ["0x3505cc40"]
        expected_margin = 70
    else:
        expected_crc = ["0x5dddffed"]
        expected_margin = 118


    # Read and verify that obtained checksums are the expected ones
    outputverifier.save_and_parse_output()
    outputverifier.outputsaver.verify_output_crc(expected_crc)
    logging.info("a3_margins_oversize_hpgl2.prn - Checksum(s) verified successfully")

    # Verify margins
    outputverifier.verify_top_margin(Intents.printintent, expected_margin)
    outputverifier.verify_bottom_margin(Intents.printintent, expected_margin)
    outputverifier.verify_left_margin(Intents.printintent, expected_margin)
    outputverifier.verify_right_margin(Intents.printintent, expected_margin)

    # Verify page size
    outputverifier.verify_page_width(Intents.printintent, 9922 + expected_margin * 2)
    outputverifier.verify_page_height(Intents.printintent, 7016 + expected_margin * 2)

    logging.info("a3_margins_oversize_hpgl2.prn - Dimensions verified successfully")