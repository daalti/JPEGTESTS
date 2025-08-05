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
    +external_files:printfile20.urf=e03d1764573e4f0961887b8c887e18b10e318896aeb8524c35fc32729cca9649
    +test_classification:System
    +name:test_pdl_apvt_dft2_urf_mixedheader_gray_RGB_letter_nomedia_speci_file20
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_urf_mixedheader_gray_RGB_letter_nomedia_speci_file20
        +guid:6bd80702-1ab9-4bae-9a93-ce014dd3cc09
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=Canon & Certifications=AirPrint
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_urf_mixedheader_gray_RGB_letter_nomedia_speci_file20(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_urf_mixedheader_gray_RGB_letter_nomedia_speci_file20.test', 'e03d1764573e4f0961887b8c887e18b10e318896aeb8524c35fc32729cca9649')
    outputsaver.save_output()