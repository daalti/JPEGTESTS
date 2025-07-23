import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg onepage letter srgb 8-300dpi page from *onepage-letter-srgb-8-300dpi.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:300
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:onepage-letter-srgb-8-300dpi.pwg=f13e0dac5b5b98707bbca2ec91d6ddb4da6afa114c40f63905d24dfc1cffe07e
    +name:test_pwg_onepage_letter_srgb_8_300dpi
    +test:
        +title:test_pwg_onepage_letter_srgb_8_300dpi
        +guid:8ea226c5-5886-4a08-b385-e06e8739f938
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_onepage_letter_srgb_8_300dpi(setup_teardown, printjob, outputsaver):
    printjob.print_verify('f13e0dac5b5b98707bbca2ec91d6ddb4da6afa114c40f63905d24dfc1cffe07e', timeout=300)
    outputsaver.save_output()

    logging.info("PWG one page letter srgb 8-300dpi - Print job completed successfully")
