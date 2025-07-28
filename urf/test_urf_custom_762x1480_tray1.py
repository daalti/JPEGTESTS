import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Custom 762x1480 Tray1 urf from *Custom_762x1480_Tray1.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Custom_762x1480_Tray1.urf=c5947b5a60b829d5589d6cb7ccecbb4eb0d2baee024ecd9d48b1f2dc6ede551e
    +name:test_urf_custom_762x1480_tray1_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_custom_762x1480_tray1_page
        +guid:c951b74c-8809-4544-9d1f-b9a98a4e1d90
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_custom_762x1480_tray1_page(setup_teardown, printjob, outputsaver, tray):
    # TODO: Check for custom media size support and load if supported
    default = tray.get_default_source()
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    else:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('c5947b5a60b829d5589d6cb7ccecbb4eb0d2baee024ecd9d48b1f2dc6ede551e')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Custom 762x1480 Tray1 page - Print job completed successfully")
