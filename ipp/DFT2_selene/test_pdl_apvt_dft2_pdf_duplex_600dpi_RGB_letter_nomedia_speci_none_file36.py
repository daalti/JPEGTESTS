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
    +external_files:printfile37.pdf=b845606ab651f776ced2da15dca0499fe59f13459c7028764052ebc35cd43118
    +test_classification:System
    +name:test_pdl_apvt_dft2_pdf_duplex_600dpi_RGB_letter_nomedia_speci_file36
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PDF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_pdf_duplex_600dpi_RGB_letter_nomedia_speci_file36
        +guid:c32d17eb-0d84-4912-9216-92b0ba5877ff
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PDF & PrintProtocols=IPP & EngineFirmwareFamily=Canon & Certifications=AirPrint
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_pdf_duplex_600dpi_RGB_letter_nomedia_speci_file36(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_pdf_duplex_600dpi_RGB_letter_nomedia_speci_file37.test', 'b845606ab651f776ced2da15dca0499fe59f13459c7028764052ebc35cd43118')
    outputsaver.save_output()