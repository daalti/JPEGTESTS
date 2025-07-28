import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf 16K Mono from *16K_Mono.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:16K_Mono.urf=24454394fcb1eaf094acd91fff8401198ebab717390560ff30cd12878c420877
    +name:test_urf_16k_mono_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_16k_mono_page
        +guid:c6ab02c4-4136-484a-b7ee-dad03d85836e
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=roc_16k_7.75x10.75in

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_16k_mono_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('roc_16k_7.75x10.75in', default):
        tray.configure_tray(default, 'roc_16k_7.75x10.75in', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')
        
    printjob.print_verify('24454394fcb1eaf094acd91fff8401198ebab717390560ff30cd12878c420877')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF 16K Mono page - Print job completed successfully")
