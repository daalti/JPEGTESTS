import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print valid raster format-7 from *PwgCloudPrint-ValidRasterFormat-7.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-ValidRasterFormat-7.pwg=acd1927984e9ed031fc4dac26cbd29112725a05e235b263aa31abdb2465c488c
    +name:test_pwg_cloud_print_valid_raster_format_7_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_valid_raster_format_7_page
        +guid:eab68004-540b-4ba9-b893-0b8ba7b0f1c9
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_valid_raster_format_7_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('acd1927984e9ed031fc4dac26cbd29112725a05e235b263aa31abdb2465c488c')
    outputsaver.save_output()

    logging.info("PWG Cloud Print Valid Raster Format-7 Page- Print job completed successfully")
