import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf 16k Color from *16K_Color.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:16K_Color.urf=24454394fcb1eaf094acd91fff8401198ebab717390560ff30cd12878c420877
    +name:test_urf_16k_color_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_16k_color_page
        +guid:c4f8ca8d-1ddd-4ef1-83c9-3ae5f55fcec5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=roc_16k_7.75x10.75in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_16k_color_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('roc_16k_7.75x10.75in', default):
        tray.configure_tray(default, 'roc_16k_7.75x10.75in', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')
        
    printjob.print_verify('24454394fcb1eaf094acd91fff8401198ebab717390560ff30cd12878c420877')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF 16k Color page - Print job completed successfully")
