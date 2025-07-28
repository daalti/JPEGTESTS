import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Letter Color 300 from *Letter_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Letter_Color_300.urf=67968234d44ae42f5fae849e371af60db261f21280cbcd19bcb291fd0bfb4a77
    +name:test_urf_letter_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_letter_color_300_page
        +guid:f03b53e0-eecf-4c81-99f4-9b0d8853836c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_letter_color_300_page(setup_teardown, printjob, outputsaver, tray):
    printjob.print_verify('67968234d44ae42f5fae849e371af60db261f21280cbcd19bcb291fd0bfb4a77')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Letter Color 300 Page - Print job completed successfully")
