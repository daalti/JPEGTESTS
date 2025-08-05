import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18912
    +timeout:3000
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printfile7.jpg=951b4d586d30e957de71338f6e9697bcd8cb0385137f6b513412a9891e9446d4
    +test_classification:System
    +name:test_pdl_apvt_dft3_jpeg_600dpi_RGB_normal_nomedia_speci_auto_file8
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft3_jpeg_600dpi_RGB_normal_nomedia_speci_auto_file8
        +guid:d4e00704-528f-4173-a1bc-3e27eff727a3
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=JPEG & PrintProtocols=IPP & Certifications=AirPrint

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft3_jpeg_600dpi_RGB_normal_nomedia_speci_auto_file8(setup_teardown, printjob, outputsaver,udw):
    # Setting udw command for crc to true for generating pdl crc after print job done
    outputsaver.validate_crc_tiff(udw)
    printjob.ipp_print_using_attribute_file('dft3_jpeg_600dpi_RGB_normal_nomedia_speci_auto_file8.test', '951b4d586d30e957de71338f6e9697bcd8cb0385137f6b513412a9891e9446d4',timeout=3000)
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

