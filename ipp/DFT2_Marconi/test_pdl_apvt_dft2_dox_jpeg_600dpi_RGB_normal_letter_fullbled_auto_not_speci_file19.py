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
    +external_files:printfile1.jpg=a9fcd77a13a7a4d6f46e5aa0a3867e249ea9501a95344ce9cec577c6789624f1
    +test_classification:System
    +name:test_pdl_apvt_dft2_dox_jpeg_600dpi_RGB_normal_letter_fullbled_auto_not_speci_file19
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_dox_jpeg_600dpi_RGB_normal_letter_fullbled_auto_not_speci_file19
        +guid:15d4cb05-59ba-49c3-93f4-90aff29a7415
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=JPEG & PrintProtocols=IPP & EngineFirmwareFamily=DoX & Certifications=AirPrint & MediaMargin=0

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_dox_jpeg_600dpi_RGB_normal_letter_fullbled_auto_not_speci_file19(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_dox_jpeg_600dpi_RGB_normal_letter_fullbled_auto_not_speci_file19.test', 'a9fcd77a13a7a4d6f46e5aa0a3867e249ea9501a95344ce9cec577c6789624f1')
    outputsaver.save_output()
