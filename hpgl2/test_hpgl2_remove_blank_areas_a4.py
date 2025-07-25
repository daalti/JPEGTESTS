import pytest
import logging
from dunetuf.print.output.intents import Intents

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print HPGL2 job with remove blank areas option and verify CRC
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-191746
    +timeout:120
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:RemoveBlankAreas_A4.prn=61dc742badda5ee1c47295e49430cb7ca91632b96fbb812a72de3eb024fbccb6
    +test_classification:System
    +name:test_hpgl2_remove_blank_areas_a4
    +test:
        +title:test_hpgl2_remove_blank_areas_a4
        +guid:d4a673b6-5119-4084-8007-a78fd2161cd6
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=HPGL2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_hpgl2_remove_blank_areas_a4(setup_teardown, printjob, outputverifier):
    
    logging.info('Running test_hpgl2_remove_blank_areas_a4')

    outputverifier.outputsaver.operation_mode('CRC')
    printjob.print_verify('61dc742badda5ee1c47295e49430cb7ca91632b96fbb812a72de3eb024fbccb6', 'SUCCESS', 300, 1)
    logging.info("RemoveBlankAreas_A4.prn - Print job completed successfully")

    ### VERIFY
    if outputverifier.outputsaver.configuration.productname == "jupiter":
        expected_crc = ["0x4ac00c32"]
    else:
        expected_crc = ["0x8f39bf53"]
    
    # Read and verify that obtained checksums are the expected ones
    outputverifier.save_and_parse_output()
    outputverifier.outputsaver.verify_output_crc(expected_crc)
    logging.info("RemoveBlankAreas_A4.prn - Checksum(s) verified successfully")

    # Verify margins
    outputverifier.verify_top_margin(Intents.printintent, 119)
    outputverifier.verify_bottom_margin(Intents.printintent, 119)
    outputverifier.verify_left_margin(Intents.printintent, 119)
    outputverifier.verify_right_margin(Intents.printintent, 119)

    # Verify page size
    outputverifier.verify_page_width(Intents.printintent, 2800)
    outputverifier.verify_page_height(Intents.printintent, 2865)

    logging.info("RemoveBlankAreas_A4.prn - Dimensions verified successfully")