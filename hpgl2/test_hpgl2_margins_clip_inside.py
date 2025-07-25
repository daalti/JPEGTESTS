import pytest
import logging
from dunetuf.print.output.intents import Intents

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print HPGL2 job with margins set as clip inside and verify CRC
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-191744
    +timeout:120
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:a3_margins_clipinside_hpgl2.prn=f21d571f555691fbebc8e72272ffedfa2135e0375e4cfa5e151e803569f0267f
    +test_classification:System
    +name:test_hpgl2_margins_clip_inside
    +test:
        +title:test_hpgl2_margins_clip_inside
        +guid:ec73d75e-d0a4-42b6-90c4-ae041cbcf970
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=HPGL2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_hpgl2_margins_clip_inside(setup_teardown, printjob, outputverifier):
    
    logging.info('Running test_hpgl2_margins_clip_inside')

    outputverifier.outputsaver.operation_mode('CRC')
    printjob.print_verify('f21d571f555691fbebc8e72272ffedfa2135e0375e4cfa5e151e803569f0267f', 'SUCCESS', 300, 1)
    logging.info("a3_margins_clipinside_hpgl2.prn - Print job completed successfully")

    ### VERIFY
    if outputverifier.outputsaver.configuration.productname == "jupiter":
        expected_crc = ["0xe0648dca"]
        expected_margin = 71
    else:
        expected_crc = ["0x5dddffed"]
        expected_margin = 118

    # Read and verify that obtained checksums are the expected ones
    outputverifier.save_and_parse_output()
    outputverifier.outputsaver.verify_output_crc(expected_crc)
    logging.info("a3_margins_clipinside_hpgl2.prn - Checksum(s) verified successfully")

    # Verify margins
    outputverifier.verify_top_margin(Intents.printintent, expected_margin)
    outputverifier.verify_bottom_margin(Intents.printintent, expected_margin)
    outputverifier.verify_left_margin(Intents.printintent, expected_margin)
    outputverifier.verify_right_margin(Intents.printintent, expected_margin)

    # Verify page size
    outputverifier.verify_page_width(Intents.printintent, 9922)
    outputverifier.verify_page_height(Intents.printintent, 7016)
    
    logging.info("a3_margins_clipinside_hpgl2.prn - Dimensions verified successfully")