import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print valid raster format-6 from *PwgCloudPrint-ValidRasterFormat-6.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-ValidRasterFormat-6.pwg=5a668918f267a0b9bd150cce07aa4b35a8e042a97f590deaa8828ef41c90d39e
    +name:test_pwg_cloud_print_valid_raster_format_6_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_valid_raster_format_6_page
        +guid:a245cdfa-cd51-4914-8511-bae49c1e7e13
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_valid_raster_format_6_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('5a668918f267a0b9bd150cce07aa4b35a8e042a97f590deaa8828ef41c90d39e')
    outputsaver.save_output()

    logging.info("PWG Cloud Print Valid Raster Format-6 Page- Print job completed successfully")
