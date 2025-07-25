import pytest
import logging
from dunetuf.print.output.intents import Intents

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print HPGL2 job with margin layout set as clipinside but without margins defined to simulate Print from USB/9100
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-191956
    +timeout:120
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:test_margins_clipinside_300_dpi.hpg=f329a69721defb75754c6e0117717f31d0e8f8340ec75dcedbb74715fd9a8d8b
    +test_classification:System
    +name:test_hpgl2_9100_usb_margins_clipinside_300_dpi
    +test:
        +title:test_hpgl2_9100_usb_margins_clipinside_300_dpi
        +guid:2a89eef5-1450-4187-8d1d-1f65ddf1cf25
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=HPGL2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$test
"""

def test_hpgl2_9100_usb_margins_clipinside_300_dpi(setup_teardown, printjob, outputverifier):
    
    logging.info('Running test_hpgl2_9100_usb_margins_clipinside_300_dpi')

    outputverifier.outputsaver.operation_mode('CRC')
    printjob.print_verify('f329a69721defb75754c6e0117717f31d0e8f8340ec75dcedbb74715fd9a8d8b', 'SUCCESS', 300, 1)
    logging.info("test_margins_clipinside_300_dpi.hpg - Print job completed successfully")

    ### VERIFY
    if outputverifier.outputsaver.configuration.productname == "jupiter":
        expected_crc = ["0x54cade3"]
        expected_margin = 35
    else:
        expected_crc = ["0x6981c237"]
        expected_margin = 59


    # Read and verify that obtained checksums are the expected ones
    outputverifier.save_and_parse_output()
    outputverifier.outputsaver.verify_output_crc(expected_crc)
    logging.info("test_margins_clipinside_300_dpi.hpg - Checksum(s) verified successfully")

    # Verify margins
    outputverifier.verify_top_margin(Intents.printintent, expected_margin)
    outputverifier.verify_bottom_margin(Intents.printintent, expected_margin)
    outputverifier.verify_left_margin(Intents.printintent, expected_margin)
    outputverifier.verify_right_margin(Intents.printintent, expected_margin)

    # Verify page size
    outputverifier.verify_page_width(Intents.printintent, 2481)
    outputverifier.verify_page_height(Intents.printintent, 3508)

    logging.info("test_margins_clipinside_300_dpi.hpg - Dimensions verified successfully")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print HPGL2 job with margin layout set as oversize but without margins defined to simulate Print from USB/9100
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-191956
    +timeout:120
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:test_margins_oversize_300_dpi.hpg=8bc905f582da6e73004884b81da26ebfa29f44b81c5d148aeb03498180c1a074
    +test_classification:System
    +name:test_hpgl2_9100_usb_margins_oversize_300_dpi
    +test:
        +title:test_hpgl2_9100_usb_margins_oversize_300_dpi
        +guid:2ab6f61a-16e8-443d-b0cd-49ae7adeaac2
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=HPGL2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$test
"""

def test_hpgl2_9100_usb_margins_oversize_300_dpi(setup_teardown, printjob, outputverifier):
    
    logging.info('Running test_hpgl2_9100_usb_margins_oversize_300_dpi')

    outputverifier.outputsaver.operation_mode('CRC')
    printjob.print_verify('8bc905f582da6e73004884b81da26ebfa29f44b81c5d148aeb03498180c1a074', 'SUCCESS', 300, 1)
    logging.info("test_margins_oversize_300_dpi.hpg - Print job completed successfully")

    ### VERIFY
    if outputverifier.outputsaver.configuration.productname == "jupiter":
        expected_crc = ["0x517ffff8"]
        expected_margin = 35
    else:
        expected_crc = ["0x6981c237"]
        expected_margin = 59


    # Read and verify that obtained checksums are the expected ones
    outputverifier.save_and_parse_output()
    outputverifier.outputsaver.verify_output_crc(expected_crc)
    logging.info("test_margins_oversize_300_dpi.hpg - Checksum(s) verified successfully")

    # Verify margins
    outputverifier.verify_top_margin(Intents.printintent, expected_margin)
    outputverifier.verify_bottom_margin(Intents.printintent, expected_margin)
    outputverifier.verify_left_margin(Intents.printintent, expected_margin)
    outputverifier.verify_right_margin(Intents.printintent, expected_margin)

    # Verify page size
    outputverifier.verify_page_width(Intents.printintent, 2481 + expected_margin * 2)
    outputverifier.verify_page_height(Intents.printintent, 3508 + expected_margin * 2)

    logging.info("test_margins_oversize_300_dpi.hpg - Dimensions verified successfully")