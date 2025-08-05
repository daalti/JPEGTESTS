import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18912
    +timeout:180
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printfile1.jpg=a9fcd77a13a7a4d6f46e5aa0a3867e249ea9501a95344ce9cec577c6789624f1
    +test_classification:System
    +name:test_pdl_apvt_dft2_jpeg_600dpi_RGB_letter_nomedia_speci_fit_file5
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_jpeg_600dpi_RGB_letter_nomedia_speci_fit_file5
        +guid:c886bcc2-a773-4ad3-b4d5-e2eb7d960406
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=JPEG & PrintProtocols=IPP & EngineFirmwareFamily=Canon & Certifications=AirPrint
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_jpeg_600dpi_RGB_letter_nomedia_speci_fit_file5(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_jpeg_600dpi_RGB_letter_nomedia_speci_fit_file5.test', 'a9fcd77a13a7a4d6f46e5aa0a3867e249ea9501a95344ce9cec577c6789624f1')
    outputsaver.save_output()