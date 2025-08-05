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
    +external_files:printfile31.pdf=150ea87988dabc7bc568a29125d06f585746b162f2cb08fb1fd4b3a917e62219
    +test_classification:System
    +name:test_pdl_apvt_dft2_dox_pdf_duplex_600dpi_RGB_normal_auto_file26
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_dox_pdf_duplex_600dpi_RGB_normal_auto_file26
        +guid:eed5ee24-3dbb-46de-bb11-6b07dc9651b7
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PDF & PrintProtocols=IPP & EngineFirmwareFamily=DoX & Certifications=AirPrint & MediaMargin=296

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_dox_pdf_duplex_600dpi_RGB_normal_auto_file26(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.ipp_print_using_attribute_file('dft2_dox_pdf_duplex_600dpi_RGB_normal_auto_file26.test', '150ea87988dabc7bc568a29125d06f585746b162f2cb08fb1fd4b3a917e62219')
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    # tray.reset_trays()

    logging.info("Print job completed successfully")