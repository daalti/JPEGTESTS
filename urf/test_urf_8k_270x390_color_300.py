import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf 8k_270x390 Color 300 page from *8k_270x390_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:8k_270x390_Color_300.urf=fb0c516176512a33ca11734be94840db5d9097685216ce69e09f7104a85dbcfd
    +name:test_urf_8k_270x390_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_8k_270x390_color_300_page
        +guid:17b1b4af-a9da-4184-a42f-002e8e3d5ac0
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_8k_270x390_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('om_8k_270x390mm', default):
        tray.configure_tray(default, 'om_8k_270x390mm', 'stationery')

    printjob.print_verify('fb0c516176512a33ca11734be94840db5d9097685216ce69e09f7104a85dbcfd')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF 8k_270x390 Color 300 page - Print job completed successfully")
