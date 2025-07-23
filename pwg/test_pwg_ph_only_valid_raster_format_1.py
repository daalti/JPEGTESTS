import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only valid raster format-1 page from *PwgPhOnly-ValidRasterFormat-1.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-ValidRasterFormat-1.pwg=9aa53ec78858441d7becdc848adc595240164d5e5169ca6d18112a612b1efdd9
    +name:test_pwg_ph_only_valid_raster_format_1_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_valid_raster_format_1_page
        +guid:1a220bdd-5ad1-4d74-bd31-0c6ad3e7df31
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_valid_raster_format_1_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9aa53ec78858441d7becdc848adc595240164d5e5169ca6d18112a612b1efdd9')
    outputsaver.save_output()

    logging.info("PWG Ph Only Valid Raster Foramt-1 - Print job completed successfully")
