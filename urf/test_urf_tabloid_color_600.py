import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Tabloid Color 600 Page from *Tabloid_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Tabloid_Color_600.urf=2299852d4b44f1895ae485b1cc1ccb645e52b3e3acd234b8f90f1589d8eaeb18
    +name:test_urf_tabloid_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_tabloid_color_600_page
        +guid:3ab52843-6474-49c0-9361-425af5d7de5c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_tabloid_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_arch-b_12x18in', default):
        tray.configure_tray(default, 'na_arch-b_12x18in', 'stationery')
    elif tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    printjob.print_verify('2299852d4b44f1895ae485b1cc1ccb645e52b3e3acd234b8f90f1589d8eaeb18')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Tabloid Color 600 Page - Print job completed successfully")
