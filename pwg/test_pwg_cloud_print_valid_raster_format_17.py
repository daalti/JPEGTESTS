import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print valid raster format-17 from *PwgCloudPrint-ValidRasterFormat-17.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-ValidRasterFormat-17.pwg=7d2697f8462c3f412fa0fd82b2476b683792079f551029f6ee4d2277ac4b8601
    +name:test_pwg_cloud_print_valid_raster_format_17_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_valid_raster_format_17_page
        +guid:1e49b066-799e-4bdc-a827-30de611b42df
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_valid_raster_format_17_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7d2697f8462c3f412fa0fd82b2476b683792079f551029f6ee4d2277ac4b8601')
    outputsaver.save_output()

    logging.info("PWG Cloud Print Valid Raster Format-17 Page- Print job completed successfully")
