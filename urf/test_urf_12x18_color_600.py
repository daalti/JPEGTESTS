import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf 12x18_Color_360 page from *12x18_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:12x18_Color_600.urf=abeb87954b7d0d84d5696707f05e6cb3d7c61e612b7d4e0ad88ecba7dc83d30e
    +name:test_urf_12x18_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_12x18_color_600_page
        +guid:6beaac08-8f57-40a6-9799-102449ebfac3
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_12x18_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_arch-b_12x18in', default):
        tray.configure_tray(default, 'na_arch-b_12x18in', 'stationery')

    printjob.print_verify('abeb87954b7d0d84d5696707f05e6cb3d7c61e612b7d4e0ad88ecba7dc83d30e')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF 12x18 Color 600 page - Print job completed successfully")
