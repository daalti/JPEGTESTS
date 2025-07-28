import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Tabloid 600 Color Page from *Tabloid_mono_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Tabloid_Mono_600.urf=ebc34fb5d2dc851b9a5fc928ac5747c5a71449449efc3b161fcaa1c1a15d5480
    +name:test_urf_tabloid_600_mono_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_tabloid_600_mono_page
        +guid:89344676-0980-4227-acce-416ae68aa8bf
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_tabloid_600_mono_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_arch-b_12x18in', default):
        tray.configure_tray(default, 'na_arch-b_12x18in', 'stationery')
    elif tray.is_size_supported('na_letter_8.5x11in', default):
        tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')

    printjob.print_verify('ebc34fb5d2dc851b9a5fc928ac5747c5a71449449efc3b161fcaa1c1a15d5480')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Tabloid 600 Color Page - Print job completed successfully")
