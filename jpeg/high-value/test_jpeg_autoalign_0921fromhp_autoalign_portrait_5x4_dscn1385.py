import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simple print job of jpeg file of autoalign 0921fromhp autoalign portrait 5x4 dscn1385
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:autoAlign_0921fromHP_AutoAlign_Portrait_5x4_DSCN1385.JPG=44ffc42c2d40cc0e77340abccd78e6de628f0de5bbea5e7ded8137605a70ed7e
    +test_classification:System
    +name:test_jpeg_autoalign_0921fromhp_autoalign_portrait_5x4_dscn1385
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_autoalign_0921fromhp_autoalign_portrait_5x4_dscn1385
        +guid:a407bdf6-a3cc-404c-9a7d-677215c4b71d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_autoalign_0921fromhp_autoalign_portrait_5x4_dscn1385(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    else:
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('44ffc42c2d40cc0e77340abccd78e6de628f0de5bbea5e7ded8137605a70ed7e')
    outputsaver.save_output()

    logging.info("Jpeg autoAlign 0921fromHP AutoAlign Portrait 5x4 DSCN1385 file")
