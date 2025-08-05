import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18912
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printfile63.urf=359894316e094a3c0b5a208f27f194e9ef70eff5350b8e7f4dd5364a147f478a
    +test_classification:System
    +name:test_pdl_apvt_dft2_dox_urf_Gray_DeviceRGB_duplex_Duplex_letter_auto_file63
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_dox_urf_Gray_DeviceRGB_duplex_Duplex_letter_auto_file63
        +guid:25836447-916f-4c96-a54b-bf03c9a245f1
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=DoX & Duplexer=True & Certifications=AirPrint & MediaInputInstalled=Automatic

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_dox_urf_Gray_DeviceRGB_duplex_Duplex_letter_auto_file63(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.ipp_print_using_attribute_file('dft2_dox_urf_Gray_DeviceRGB_duplex_Duplex_letter_auto_file63.test', '359894316e094a3c0b5a208f27f194e9ef70eff5350b8e7f4dd5364a147f478a')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    # tray.reset_trays()

    logging.info("Print job completed successfully")