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
    +name:test_pdl_apvt_dft2_dox_pdf_duplex_600dpi_normal_letter_fullbled_auto_file32
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_dox_pdf_duplex_600dpi_normal_letter_fullbled_auto_file32
        +guid:22d7eaf8-983c-4eaa-b44c-2968352666d8
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PDF & PrintProtocols=IPP & EngineFirmwareFamily=DoX & Certifications=AirPrint & MediaMargin=296

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_dox_pdf_duplex_600dpi_normal_letter_fullbled_auto_file32(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_dox_pdf_duplex_600dpi_normal_letter_fullbled_auto_file32.test', '150ea87988dabc7bc568a29125d06f585746b162f2cb08fb1fd4b3a917e62219')
    outputsaver.save_output()