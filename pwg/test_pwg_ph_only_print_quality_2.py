import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only print quality-2 page from *PwgPhOnly-PrintQuality-2.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-PrintQuality-2.pwg=4c06265cab20f7cc7f04accb477da0801d3e4d5d041117e9c21c58cb50806d26
    +name:test_pwg_ph_only_print_quality_2_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_print_quality_2_page
        +guid:08705fca-50bf-48e1-969b-7dbdb484c21a
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
def test_pwg_ph_only_print_quality_2_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4c06265cab20f7cc7f04accb477da0801d3e4d5d041117e9c21c58cb50806d26')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')

    logging.info("PWG Ph Only Print Quality-2 - Print job completed successfully")
