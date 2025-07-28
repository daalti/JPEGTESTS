import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Custom 762x1480 PJLWrap Tray1 urf from *Custom_762x1480_PJLWrap_Tray1.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Custom_762x1480_PJLWrap_Tray2.urf=d5cfc4e96b956af45490a1235296dc0b951e16178b93cdfea303278ed00b31ac
    +name:test_urf_custom_762x1480_pjl_wrap_tray1_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_custom_762x1480_pjl_wrap_tray1_page
        +guid:495d81cd-a871-4123-b9f8-bc8ef1ab1575
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_custom_762x1480_pjl_wrap_tray1_page(setup_teardown, printjob, outputsaver, tray,udw):

    default = tray.get_default_source()
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    else:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('d5cfc4e96b956af45490a1235296dc0b951e16178b93cdfea303278ed00b31ac', 'FAILED')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Custom 762x1480 PJLWrap Tray1 page - Print job completed successfully")
