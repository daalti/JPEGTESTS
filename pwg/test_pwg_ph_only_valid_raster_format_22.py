import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only valid raster format-22 page from *PwgPhOnly-ValidRasterFormat-22.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-ValidRasterFormat-22.pwg=acd1927984e9ed031fc4dac26cbd29112725a05e235b263aa31abdb2465c488c
    +name:test_pwg_ph_only_valid_raster_format_22_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_valid_raster_format_22_page
        +guid:0ceba664-fae6-49d7-84a2-a4b146ea46d7
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
def test_pwg_ph_only_valid_raster_format_22_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('acd1927984e9ed031fc4dac26cbd29112725a05e235b263aa31abdb2465c488c')
    outputsaver.save_output()

    logging.info("PWG Ph Only Valid Raster Foramt-22 - Print job completed successfully")
