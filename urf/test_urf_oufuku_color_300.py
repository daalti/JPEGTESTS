import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Urf Oufuku Color 300 Page from *Oufuku_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Oufuku_Color_300.urf=f744f31f05b1b2e6737867f0a3a8d70d076c077d9d8dde6a8f5e6de2ce07ac1f
    +name:test_urf_oufuku_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_oufuku_color_300_page
        +guid:9dd33c9e-1b4c-498c-b8aa-3993d376c4c6
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=jpn_oufuku_148x200mm

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_oufuku_color_300_page(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    default_size = tray.get_default_size(default)

    if tray.is_size_supported('jpn_oufuku_148x200mm', default):
        tray.configure_tray(default, 'jpn_oufuku_148x200mm', 'stationery')
    
    elif tray.is_size_supported("com.hp.ext.mediaSize.jpn_oufuku_148x200mm.rotated", default):
        tray.configure_tray(default, "com.hp.ext.mediaSize.jpn_oufuku_148x200mm.rotated", "stationery")
        
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')

    printjob.print_verify('f744f31f05b1b2e6737867f0a3a8d70d076c077d9d8dde6a8f5e6de2ce07ac1f')
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("URF Oufuku Color 300 Page - Print job completed successfully")
