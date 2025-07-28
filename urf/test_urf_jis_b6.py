import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52178025 Simple print job of Urf JIS B6 from *JIS_B6.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:JIS_B6.urf=626d7d9d260895152c22a4fd7f02c8be6140ecb23e056e85161d4c43b165679e
    +name:test_urf_jis_b6_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_jis_b6_page
        +guid:966444d7-0928-414c-b257-babb3334b1d9
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=jis_b6_128x182mm
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_jis_b6_page(setup_teardown, printjob, outputsaver, tray, udw, reset_tray):
    default = tray.get_default_source()
    if tray.is_size_supported('jis_b6_128x182mm', default):
        tray.configure_tray(default, 'jis_b6_128x182mm', 'stationery')
    elif tray.is_size_supported('custom', default):
        tray.configure_tray(default, 'custom', 'stationery')
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('626d7d9d260895152c22a4fd7f02c8be6140ecb23e056e85161d4c43b165679e')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc() 
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()

    logging.info("URF JIS B6 Page - Print job completed successfully")
