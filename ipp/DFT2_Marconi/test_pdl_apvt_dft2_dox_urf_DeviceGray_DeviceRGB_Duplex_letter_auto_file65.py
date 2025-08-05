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
    +external_files:printfile65.urf=5f935e756d3177e8fd511f343f7b14d936556fc2d1e8784d763f344336aafe0f
    +test_classification:System
    +name:test_pdl_apvt_dft2_dox_urf_DeviceGray_DeviceRGB_Duplex_letter_auto_file65
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_dox_urf_DeviceGray_DeviceRGB_Duplex_letter_auto_file65
        +guid:6376b891-2baf-4c70-96e5-086a27e73989
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=DoX & Duplexer=True & Certifications=AirPrint & MediaInputInstalled=Automatic

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_dox_urf_DeviceGray_DeviceRGB_Duplex_letter_auto_file65(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.ipp_print_using_attribute_file('dft2_dox_urf_DeviceGray_DeviceRGB_Duplex_letter_auto_file65.test', '5f935e756d3177e8fd511f343f7b14d936556fc2d1e8784d763f344336aafe0f')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    # tray.reset_trays()

    logging.info("Print job completed successfully")
