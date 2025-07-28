import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52178029 Simple print job of Urf Oufuku Color 600 Page from *Oufuku_Color_600.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Oufuku_Color_600.urf=a915f17b8b95065a52565954cdd315218d3ad706924ca0bdd01ccb595317f9bd
    +name:test_urf_oufuku_color_600_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_oufuku_color_600_page
        +guid:c1bca215-5888-4608-8cb5-9534dd350def
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=jpn_oufuku_148x200mm
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_oufuku_color_600_page(setup_teardown, printjob, outputsaver, tray, udw, reset_tray):
    default = tray.get_default_source()
    if tray.is_size_supported('jpn_oufuku_148x200mm', default):
        tray.configure_tray(default, 'jpn_oufuku_148x200mm', 'stationery')
        
    elif tray.is_size_supported("com.hp.ext.mediaSize.jpn_oufuku_148x200mm.rotated", default):
        tray.configure_tray(default, "com.hp.ext.mediaSize.jpn_oufuku_148x200mm.rotated", "stationery")
        
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('a915f17b8b95065a52565954cdd315218d3ad706924ca0bdd01ccb595317f9bd')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc() 
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()

    logging.info("URF Oufuku Color 600 Page - Print job completed successfully")
