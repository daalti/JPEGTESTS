import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print-valid raster format-2 page from *PwgCloudPrint-ValidRasterFormat-2.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-ValidRasterFormat-2.pwg=378e3b9575c76d1176cca9d752b3bb8fda19a208cc663a2da8dd191824bb00a9
    +name:test_pwg_cloud_print_valid_raster_format_2_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_valid_raster_format_2_page
        +guid:ecdcf5cf-c98f-48e8-975a-1d342bfc669c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_valid_raster_format_2_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('378e3b9575c76d1176cca9d752b3bb8fda19a208cc663a2da8dd191824bb00a9')
    outputsaver.save_output()

    logging.info("PWG Cloud Print-Valid Raster Format-2completed successfully")
