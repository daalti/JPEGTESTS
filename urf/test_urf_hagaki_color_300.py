import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52178024 Simple print job of Urf Hagaki Color 300 from *Hagaki_Color_300.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Hagaki_Color_300.urf=3c4f888289f5d7c02fba626cc9e87fc2bd5aa45701a7a1829de96efb473575e9
    +name:test_urf_hagaki_color_300_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_hagaki_color_300_page
        +guid:0e1100a6-a116-42d3-807c-22971a332c4a
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF & MediaSizeSupported=jpn_hagaki_100x148mm
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_hagaki_color_300_page(setup_teardown, printjob, outputsaver, tray, udw, reset_tray):
    default = tray.get_default_source()
    if tray.is_size_supported('jpn_hagaki_100x148mm', default):
        tray.configure_tray(default, 'jpn_hagaki_100x148mm', 'stationery')
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('3c4f888289f5d7c02fba626cc9e87fc2bd5aa45701a7a1829de96efb473575e9')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc() 
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()

    logging.info("URF Hagaki Color 300 page - Print job completed successfully")
