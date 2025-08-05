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
    +external_files:printfile71.urf=788e530288283507775b9f323fc6acf9f418f8c5fc8a27523ffcd0b4931b3d75
    +test_classification:System
    +name:test_pdl_apvt_dft2_dox_urf_DeviceRGB_RGB_Duplex_letter_auto_file71
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pdl_apvt_dft2_dox_urf_DeviceRGB_RGB_Duplex_letter_auto_file71
        +guid:8e721563-4e01-42aa-a011-d319e8f50747
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=URF & PrintProtocols=IPP & EngineFirmwareFamily=DoX & Duplexer=True & Certifications=AirPrint & MediaInputInstalled=Automatic

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pdl_apvt_dft2_dox_urf_DeviceRGB_RGB_Duplex_letter_auto_file71(setup_teardown, printjob, outputsaver):
    printjob.ipp_print_using_attribute_file('dft2_dox_urf_DeviceRGB_RGB_Duplex_letter_auto_file71.test', '788e530288283507775b9f323fc6acf9f418f8c5fc8a27523ffcd0b4931b3d75')
    outputsaver.save_output()