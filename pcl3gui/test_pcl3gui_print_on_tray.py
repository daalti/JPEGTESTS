import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job on tray PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:LFPSWQAA-4560
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printOntray.pcl=810d550f6192b94db7340887f7497f228c506acd279dc4aaa2ce7d2230e2c4cb
    +name:test_pcl3gui_print_on_tray
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3gui_print_on_tray
        +guid:8860bdf0-363f-11ec-9771-7f10620afc20
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI&DeviceClass=MFP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3gui_print_on_tray(setup_teardown, printjob, outputsaver, tray, udw):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    printjob.print_verify('810d550f6192b94db7340887f7497f228c506acd279dc4aaa2ce7d2230e2c4cb','SUCCESS', 120, 1)
    outputsaver.save_output()
    
    # CRC check
    outputsaver.operation_mode('TIFF')
    outputsaver.validate_crc_tiff(udw)
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputsaver.operation_mode('NONE')
    
    tray.reset_trays()
    logging.info("PCL3GUI print on tray successfully")
