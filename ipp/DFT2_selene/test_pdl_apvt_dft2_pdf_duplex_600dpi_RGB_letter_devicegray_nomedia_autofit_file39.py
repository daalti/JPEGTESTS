import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18912
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printfile31.pdf=150ea87988dabc7bc568a29125d06f585746b162f2cb08fb1fd4b3a917e62219
    +test_classification:System
    +name:test_pdl_apvt_dft2_pdf_duplex_600dpi_RGB_letter_devicegray_nomedia_nospeci_autofit_file39
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_pdf_duplex_600dpi_RGB_letter_devicegray_nomedia_nospeci_autofit_file39
        +guid:af4b0dfc-0d6d-43c5-9c58-b237581d455e
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PDF & PrintProtocols=IPP & EngineFirmwareFamily=Canon & PrintResolution=Print600 & Certifications=AirPrint
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_pdf_duplex_600dpi_RGB_letter_devicegray_nomedia_nospeci_autofit_file39(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('test_pdl_apvt_dft2_pdf_duplex_600dpi_RGB_letter_devicegray_nomedia_nospeci_autofit_file39.test', '150ea87988dabc7bc568a29125d06f585746b162f2cb08fb1fd4b3a917e62219')
    outputsaver.save_output()