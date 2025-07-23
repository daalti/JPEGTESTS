import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg cloud print valid raster format-14 from *PwgCloudPrint-ValidRasterFormat-14.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-12138
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgCloudPrint-ValidRasterFormat-14.pwg=025049c3f5ed5bf7914b36257e6b74a13939a0305585d017abf7dbe3f7144521
    +name:test_pwg_cloud_print_valid_raster_format_14_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_cloud_print_valid_raster_format_14_page
        +guid:4b2b6a3f-e7b1-41bd-b331-7552fcda54b5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_cloud_print_valid_raster_format_14_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('025049c3f5ed5bf7914b36257e6b74a13939a0305585d017abf7dbe3f7144521')
    outputsaver.save_output()

    logging.info("PWG Cloud Print Valid Raster Format-14 Page- Print job completed successfully")
