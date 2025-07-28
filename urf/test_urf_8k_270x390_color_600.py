import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf 8k_270x390 Color 600 page from *8k_270x390_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:8k_270x390_Color_600.urf=7086d2086dd4ecab1cb3756e2855b68aa6ef0e32796e515d0e60683096b09163
    +name:test_urf_8k_270x390_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_8k_270x390_color_600_page
        +guid:fd05dbf5-738c-4762-8c13-c97082ecae90
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_8k_270x390_color_600_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('om_8k_270x390mm', default):
        tray.configure_tray(default, 'om_8k_270x390mm', 'stationery')

    printjob.print_verify('7086d2086dd4ecab1cb3756e2855b68aa6ef0e32796e515d0e60683096b09163')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF 8k_270x390 Color 600 page - Print job completed successfully")
