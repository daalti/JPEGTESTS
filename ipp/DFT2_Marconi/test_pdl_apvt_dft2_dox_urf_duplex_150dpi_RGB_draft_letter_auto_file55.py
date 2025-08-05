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
    +external_files:printfile55.urf=86c3b078be42caacf7f830435b0f2aaf24403b3d9db92ee936a35607c868a1a2
    +test_classification:System
    +name:test_pdl_apvt_dft2_dox_urf_duplex_150dpi_RGB_draft_letter_auto_file55
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_dox_urf_duplex_150dpi_RGB_draft_letter_auto_file55
        +guid:09034928-17ce-426f-a7c9-87f4b819b947
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=DoX & Duplexer=True & Certifications=AirPrint & MediaInputInstalled=Automatic

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_dox_urf_duplex_150dpi_RGB_draft_letter_auto_file55(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.ipp_print_using_attribute_file('dft2_dox_urf_duplex_150dpi_RGB_draft_letter_auto_file55.test', '86c3b078be42caacf7f830435b0f2aaf24403b3d9db92ee936a35607c868a1a2')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    # tray.reset_trays()

    logging.info("Print job completed successfully")
