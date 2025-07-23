import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only valid raster format-3 page from *PwgPhOnly-ValidRasterFormat-3.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-ValidRasterFormat-3.pwg=5a668918f267a0b9bd150cce07aa4b35a8e042a97f590deaa8828ef41c90d39e
    +name:test_pwg_ph_only_valid_raster_format_3_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_valid_raster_format_3_page
        +guid:a47ea4e2-391a-4142-ba34-e03bd7919cd0
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_valid_raster_format_3_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5a668918f267a0b9bd150cce07aa4b35a8e042a97f590deaa8828ef41c90d39e')
    outputsaver.save_output()

    logging.info("PWG Ph Only Valid Raster Foramt-3 - Print job completed successfully")
